"""Run from any directory after pip install -r requirements.txt."""
import os
from pathlib import Path
from dbt.cli.main import dbtRunner
root=Path(__file__).resolve().parents[1]
os.chdir(root/'dbt')
os.environ['DBT_SEND_ANONYMOUS_USAGE_STATS']='false'
result=dbtRunner().invoke(['build','--profiles-dir','.'])
if not result.success:
    raise SystemExit(str(result.exception or 'dbt build failed'))
