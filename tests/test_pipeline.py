import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from pipeline import enrich, forecast_values, generate

class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stores,cls.products,cls.contracts,cls.raw=generate()
        cls.mart,cls.bad=enrich(cls.raw,{s['store_id']:s for s in cls.stores},{p['product_id']:p for p in cls.products},cls.contracts)
    def test_reconciliation(self):
        amount=lambda rows:sum(r['quantity']*r['list_cents']-r['discount_cents'] for r in rows)
        self.assertEqual(amount(self.raw),sum(r['revenue_cents'] for r in self.mart)+amount(self.bad))
    def test_quarantine(self):
        self.assertEqual({r['reject_reason'] for r in self.bad},{'duplicate_key','unknown_dimension'})
        self.assertEqual(len(self.bad),2)
    def test_no_join_fanout(self):
        self.assertEqual(len(self.mart),len({(r['transaction_id'],r['line_id']) for r in self.mart}))
        ambiguous=[r for r in self.mart if r['contract_matches']>1]
        self.assertGreater(len(ambiguous),0)
        self.assertTrue(all(r['shortfall_cents'] is None and r['expected_cents'] is None for r in ambiguous))
    def test_missing_cost_not_zero(self):
        rows=[r for r in self.mart if r['unit_cost_cents'] is None]
        self.assertGreater(len(rows),0);self.assertTrue(all(r['profit_cents'] is None for r in rows))
    def test_returns_reverse_amounts(self):
        rows=[r for r in self.mart if r['event_type']=='RETURN']
        self.assertTrue(all(r['quantity']<0 and r['revenue_cents']<0 and r['cogs_cents']<0 for r in rows))
    def test_override_excluded(self):
        self.assertTrue(all(r['shortfall_cents'] is None for r in self.mart if r['authorized_override']))
    def test_exclusive_end(self):
        rows=[r for r in self.mart if r['store_id']=='S02' and r['product_id']=='P02' and r['date']=='2026-10-01']
        self.assertTrue(rows);self.assertTrue(all(r['contract_matches']==1 for r in rows))
    def test_forecast_constant(self):
        for kind in ['seasonal','weekday_trend']:self.assertEqual(forecast_values([10]*100,kind),[10]*28)
    def test_forecast_requires_history(self):
        with self.assertRaises(ValueError):forecast_values([1]*5,'seasonal')

if __name__=='__main__':unittest.main()
