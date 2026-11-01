"""Release contract checks: bundle shape, reconciliations, forecast holdout and static assets."""
import json, re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'site/dist/data.json').read_text())
assert d['meta']['synthetic'] is True
assert d['meta']['raw_rows']==d['meta']['accepted_rows']+d['meta']['rejected_rows']
assert sum(r['revenue_cents'] for r in d['daily'])==d['meta']['accepted_revenue_cents']
assert all(c['status']!='FAIL' for c in d['checks'])
assert len(d['forecast']['future'])==28
assert d['forecast']['future'][0]['date']>d['meta']['end']
assert all(0<=r['lower']<=r['units']<=r['upper'] for r in d['forecast']['future'])
assert d['forecast']['selected']==min(d['forecast']['validation_wape'],key=d['forecast']['validation_wape'].get)
for name in ['index.html','app.js','style.css']:
    text=(root/'site/dist'/name).read_text(encoding='utf-8')
    assert not re.search(r'(sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN .*PRIVATE KEY)',text)
assert 'http-equiv="Content-Security-Policy"' in (root/'site/dist/index.html').read_text(encoding='utf-8')
print('Release contract checks: PASS')
