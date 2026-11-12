"""Run a real PDF end-to-end for an execution-trace screenshot (resume not saved)."""
import argparse,json
from pathlib import Path
from pipeline import run_pipeline
p=argparse.ArgumentParser();p.add_argument('--resume',type=Path,required=True);p.add_argument('--output',type=Path,default=Path('evidence/real_resume_trace.json'))
a=p.parse_args()
r=run_pipeline(pdf_bytes=a.resume.read_bytes(),interest='data')
# Public trace: only skills, job titles and tool summaries; do not save raw contact data.
out={'status':r['status'],'stop_reason':r['stop_reason'],'profile':r['profile'],
     'trace':r['trace'],'matches':[{k:v for k,v in j.items() if k in ('title','skill_overlap_percent','matched_skills','source')} for j in r['results'][:3]]}
a.output.parent.mkdir(exist_ok=True,parents=True)
a.output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
