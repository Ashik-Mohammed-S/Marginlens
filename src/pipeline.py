"""Deterministic synthetic retail mart, reconciliation and forecast evaluation.

Run: python src/pipeline.py. Python 3.12+, standard library only.
SQL transformations execute in SQLite; optional dbt/DuckDB model is supplied separately.
"""
from __future__ import annotations
import csv, hashlib, json, math, random, sqlite3, statistics
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261102

def generate():
    rng = random.Random(SEED)
    stores = [dict(store_id=f'S{i:02}', store=f'{city} Market', region=region)
              for i, (city, region) in enumerate([('Boston','East'),('Atlanta','East'),('Chicago','Central'),('Dallas','Central'),('Seattle','West'),('Denver','West')],1)]
    products = [dict(product_id=f'P{i:02}', product=name, category=cat, list_cents=price, cost_cents=cost)
                for i,(name,cat,price,cost) in enumerate([
                ('Daily shampoo','Personal care',1299,720),('Body wash','Personal care',899,460),
                ('Face cleanser','Personal care',1599,880),('Hand soap','Home essentials',599,290),
                ('Laundry liquid','Home essentials',1899,1120),('Paper towels','Home essentials',1199,670),
                ('Trail mix','Pantry',799,420),('Coffee blend','Pantry',1499,860),('Oat cereal','Pantry',699,370)],1)]
    contracts=[]
    for s in stores:
        for p in products:
            contracts.append(dict(contract_id=f'C{s["store_id"]}{p["product_id"]}',store_id=s['store_id'],product_id=p['product_id'],valid_from='2025-01-01',valid_to='2026-11-01',agreed_cents=p['list_cents']-50))
    contracts.append(dict(contract_id='C-OVERLAP',store_id='S02',product_id='P02',valid_from='2026-09-01',valid_to='2026-10-01',agreed_cents=799))
    # Deliberate uncovered contract interval, isolated to one store/product.
    for c in contracts:
        if c['store_id']=='S06' and c['product_id']=='P09': c['valid_to']='2026-09-01'
    rows=[]; day=date(2025,1,1); end=date(2026,11,1); n=0
    while day<end:
        for si,s in enumerate(stores):
            for pi,p in enumerate(products):
                season=1+0.16*math.sin(day.timetuple().tm_yday*2*math.pi/365.25)
                weekend=1.3 if day.weekday()>=5 else 1
                trend=1+(day-date(2025,1,1)).days*0.00018
                qty=max(1,round((3+(pi%3)+si*.35)*season*weekend*trend+rng.gauss(0,1.2)))
                agreed=p['list_cents']-50; actual=agreed
                if day>=date(2026,9,1) and s['region']=='West' and p['category']=='Personal care': actual-=100
                if rng.random()<.018: actual-=150
                cost=p['cost_cents']+(65 if day>=date(2026,9,1) and p['category']=='Home essentials' else 0)
                n+=1
                row=dict(transaction_id=f'T{n:07}',line_id=1,date=day.isoformat(),store_id=s['store_id'],product_id=p['product_id'],event_type='SALE',quantity=qty,list_cents=p['list_cents'],discount_cents=qty*(p['list_cents']-actual),unit_cost_cents=cost,original_transaction_id='',authorized_override=int(actual<agreed and rng.random()<.20))
                rows.append(row)
                if rng.random()<.025:
                    n+=1; ret={**row,'transaction_id':f'T{n:07}','event_type':'RETURN','quantity':-1,'discount_cents':-(p['list_cents']-actual),'original_transaction_id':row['transaction_id'],'authorized_override':0}; rows.append(ret)
        day+=timedelta(days=1)
    # Faults are deterministic and accompanied by an explicit catalog.
    recent=[r for r in rows if r['date'].startswith('2026-10') and r['event_type']=='SALE']
    for row in recent[::97]: row['unit_cost_cents']=None
    rows.append(dict(rows[-10]))
    bad=dict(rows[-20]); bad['transaction_id']='T-ORPHAN'; bad['store_id']='S99'; rows.append(bad)
    return stores,products,contracts,rows

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def enrich(rows,stores,products,contracts):
    seen=set();accepted=[];rejected=[]
    for r in rows:
        key=(r['transaction_id'],r['line_id']); reason=None
        if key in seen: reason='duplicate_key'
        elif r['store_id'] not in stores or r['product_id'] not in products: reason='unknown_dimension'
        seen.add(key)
        if reason: rejected.append({**r,'reject_reason':reason});continue
        matches=[c for c in contracts if c['store_id']==r['store_id'] and c['product_id']==r['product_id'] and c['valid_from']<=r['date']<c['valid_to']]
        revenue=r['quantity']*r['list_cents']-r['discount_cents']
        cost=None if r['unit_cost_cents'] is None else r['quantity']*r['unit_cost_cents']
        shortfall=None
        if r['event_type']=='SALE' and len(matches)==1 and not r['authorized_override']:
            shortfall=max(0,r['quantity']*matches[0]['agreed_cents']-revenue)
        accepted.append({**r,**{k:stores[r['store_id']][k] for k in ['store','region']},**{k:products[r['product_id']][k] for k in ['product','category']},'revenue_cents':revenue,'cogs_cents':cost,'profit_cents':None if cost is None else revenue-cost,'contract_matches':len(matches),'contract_id':matches[0]['contract_id'] if len(matches)==1 else None,'expected_cents':r['quantity']*matches[0]['agreed_cents'] if len(matches)==1 and r['event_type']=='SALE' else None,'shortfall_cents':shortfall})
    return accepted,rejected

def forecast_values(history,kind,horizon=28):
    if len(history)<28: raise ValueError('At least 28 days required')
    if kind=='seasonal': return [history[-7+i%7] for i in range(horizon)]
    # Four-week weekday mean, scaled by a bounded recent level change.
    ratio=sum(history[-14:])/max(sum(history[-28:-14]),1)
    ratio=min(1.15,max(.85,ratio))
    return [max(0,statistics.mean(history[-28+i%7::7])*ratio) for i in range(horizon)]

def forecast_report(rows):
    daily=defaultdict(int)
    for r in rows:
        if r['event_type']=='SALE': daily[r['date']]+=r['quantity']
    dates=sorted(daily); values=[daily[d] for d in dates]
    # Select on three validation folds, reserve final 28 days as untouched test.
    scores={}; residuals={}
    for kind in ['seasonal','weekday_trend']:
        errors=[];actual=[]
        for end in [len(values)-112,len(values)-84,len(values)-56]:
            pred=forecast_values(values[:end],kind)
            errors += [abs(a-p) for a,p in zip(values[end:end+28],pred)];actual+=values[end:end+28]
        scores[kind]=sum(errors)/sum(actual);residuals[kind]=sorted(errors)
    winner=min(scores,key=scores.get)
    test={}
    for kind in scores:
        pred=forecast_values(values[:-28],kind)
        test[kind]=sum(abs(a-p) for a,p in zip(values[-28:],pred))/sum(values[-28:])
    band=residuals[winner][math.ceil(.9*len(residuals[winner]))-1]
    pred=forecast_values(values,winner); start=date.fromisoformat(dates[-1])+timedelta(days=1)
    future=[dict(date=(start+timedelta(days=i)).isoformat(),units=round(p,1),lower=round(max(0,p-band),1),upper=round(p+band,1)) for i,p in enumerate(pred)]
    testpred=forecast_values(values[:-28],winner)
    coverage=sum(abs(a-p)<=band for a,p in zip(values[-28:],testpred))/28
    return dict(scope='All stores; gross sale units, excluding returns',selected=winner,validation_wape=scores,test_wape=test,test_start=dates[-28],test_end=dates[-1],interval='Empirical 90th-percentile absolute validation error; nominal 90%, not guaranteed coverage',test_interval_coverage=coverage,history=[dict(date=d,units=daily[d]) for d in dates[-56:]],future=future)

def build():
    stores,products,contracts,raw=generate()
    mart,rejected=enrich(raw,{s['store_id']:s for s in stores},{p['product_id']:p for p in products},contracts)
    data=ROOT/'data';data.mkdir(exist_ok=True)
    for name,rows in [('stores',stores),('products',products),('contracts',contracts),('sales_lines',raw),('mart_sales',mart),('rejected',rejected)]:write_csv(data/f'{name}.csv',rows)
    db=sqlite3.connect(data/'marginlens.sqlite')
    db.execute('DROP TABLE IF EXISTS mart_sales')
    keys=list(mart[0]); numeric={'line_id','quantity','list_cents','discount_cents','unit_cost_cents','authorized_override','revenue_cents','cogs_cents','profit_cents','contract_matches','expected_cents','shortfall_cents'}
    db.execute('CREATE TABLE mart_sales ('+','.join(k+(' INTEGER' if k in numeric else ' TEXT') for k in keys)+')')
    db.executemany('INSERT INTO mart_sales VALUES ('+','.join('?' for _ in keys)+')',[[r[k] for k in keys] for r in mart]);db.commit()
    db.executescript((ROOT/'sql/marts.sql').read_text());db.commit()
    db.row_factory=sqlite3.Row
    groups=[dict(r) for r in db.execute('SELECT * FROM daily_finance ORDER BY date,region,category')]
    write_csv(data/'daily_finance.csv',groups)
    raw_total=sum(r['quantity']*r['list_cents']-r['discount_cents'] for r in raw)
    reject_total=sum(r['quantity']*r['list_cents']-r['discount_cents'] for r in rejected)
    accepted_total=sum(r['revenue_cents'] for r in mart)
    checks=[dict(name='Raw revenue = accepted + quarantined',status='PASS' if raw_total==accepted_total+reject_total else 'FAIL',count=0,detail='Exact integer-cent reconciliation; rejected records remain auditable.'),dict(name='Mart grain is unique',status='PASS' if len(mart)==len({(r['transaction_id'],r['line_id']) for r in mart}) else 'FAIL',count=0,detail='One row per transaction and line.'),dict(name='Quarantined source rows',status='WARN',count=len(rejected),detail='One duplicate and one unknown-store record.'),dict(name='Missing cost',status='WARN',count=sum(r['cogs_cents'] is None for r in mart),detail='Gross profit suppressed for incomplete groups; known-cost profit shown separately.'),dict(name='Ambiguous contract matches',status='WARN',count=sum(r['contract_matches']>1 for r in mart),detail='Sale preserved once; expected price and shortfall remain unknown.'),dict(name='Unmatched contracts',status='WARN',count=sum(r['contract_matches']==0 for r in mart),detail='Revenue retained; contract coverage disclosed.'),dict(name='Historical snapshot',status='INFO',count=0,detail='Data ends 2026-10-31. This demo is not a live feed.' )]
    exceptions=[]
    for r in mart:
        reasons=[]
        if r['cogs_cents'] is None:reasons.append('Missing cost')
        if r['contract_matches']>1:reasons.append('Ambiguous contract')
        if r['contract_matches']==0:reasons.append('Missing contract')
        if (r['shortfall_cents'] or 0)>0:reasons.append('Price shortfall')
        if reasons:exceptions.append({k:r[k] for k in ['transaction_id','line_id','date','store','region','product','category','quantity','revenue_cents','expected_cents','shortfall_cents','contract_id']}|dict(reason='; '.join(reasons)))
    exceptions.sort(key=lambda r:(r['date'],r['shortfall_cents'] or 0),reverse=True)
    forecast=forecast_report(mart)
    fingerprint=hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()
    payload=dict(meta=dict(name='MarginLens',synthetic=True,seed=SEED,start='2025-01-01',end='2026-10-31',raw_rows=len(raw),accepted_rows=len(mart),rejected_rows=len(rejected),fingerprint=fingerprint,raw_revenue_cents=raw_total,accepted_revenue_cents=accepted_total,rejected_revenue_cents=reject_total),daily=groups,exceptions=exceptions,checks=checks,forecast=forecast)
    dist=ROOT/'site/dist';dist.mkdir(parents=True,exist_ok=True)
    (dist/'data.json').write_text(json.dumps(payload,separators=(',',':')),encoding='utf-8')
    report=ROOT/'reports';report.mkdir(exist_ok=True)
    (report/'validation.json').write_text(json.dumps(dict(meta=payload['meta'],checks=checks,forecast=forecast),indent=2),encoding='utf-8')
    db.close()
    print(json.dumps(dict(rows=len(mart),exceptions=len(exceptions),fingerprint=fingerprint,forecast=forecast['test_wape']),indent=2))
    return payload

if __name__=='__main__':build()
