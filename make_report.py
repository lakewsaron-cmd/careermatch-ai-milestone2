from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from pathlib import Path
import json
B=Path(__file__).resolve().parent
R=json.loads((B/'evidence/evaluation_results.json').read_text())
d=Document();sec=d.sections[0];sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.7)
sec.left_margin=Inches(.85);sec.right_margin=Inches(.85)
styles=d.styles;styles['Normal'].font.name='Aptos';styles['Normal'].font.size=Pt(10)
styles['Normal'].paragraph_format.space_after=Pt(5)
heading=d.add_paragraph();heading.style='Title';heading.add_run('CareerMatch AI — Milestone II')
p=d.add_paragraph('Saron Lakew  |  Individual Final Project  |  Publish Your Agent')
p.style='Subtitle'
d.add_heading('1. Public link and agent update',level=2)
d.add_paragraph('Public URL: NOT DEPLOYED YET — add the actual Streamlit link after publishing. This document is a working draft until the public URL and live app are checked.')
d.add_paragraph('I kept the same CareerMatch AI idea from Milestone I, but I connected three parts: a Profile Agent that reads a resume, a Job Search Agent that loads and filters saved job listings, and a Match Agent that compares skills and explains the results. The tool workflow has a four-call maximum so it cannot run forever. I also added optional Gemini explanations, but those still need a live API key test. All job listings are clearly labeled as fictional examples, not real openings.')
d.add_heading('Verified demo from my resume',level=2)
d.add_picture(str(B/'evidence/verified_offline_trace.png'),width=Inches(6.75))
d.add_paragraph('The screenshot above is a rendering of the actual offline run trace, not a screenshot of a live Streamlit deployment. The complete machine-readable trace is included in the project folder.')
d.add_page_break()
d.add_heading('2. Evaluation results',level=2)
d.add_paragraph('I ran 12 test cases three times each (36 total runs) against the offline agent. pass@1 means the first run passed. pass^3 means all three runs of the same case passed. The results below are for the Python workflow, not the Gemini API.')
t=d.add_table(rows=1,cols=4);t.style='Light Shading Accent 1';t.alignment=WD_TABLE_ALIGNMENT.CENTER
for i,x in enumerate(['Test','Case','pass@1','pass^3']):t.rows[0].cells[i].text=x
for row in R['cases']:
 cells=t.add_row().cells
 for i,x in enumerate((row['test_id'],row['case'],'Pass' if row['pass_at_1'] else 'Fail','Pass' if row['pass_pow_3'] else 'Fail')): cells[i].text=str(x)
d.add_paragraph(f"Overall: {R['pass_at_1']*100:.0f}% pass@1 and {R['pass_pow_3']*100:.0f}% pass^3 after the fix.")
d.add_heading('What failed and what I changed',level=3)
d.add_paragraph('During my first test, the unusually long skills input failed because the program silently cut it off. I changed it so the program rejects anything over 1,000 characters with a clear error message. After that, I reran the same 12 cases three times each and all passed. I also tested a prompt-injection style input asking for a secret key; the agent treated it as data and did not reveal a key. These tests do not guarantee that every possible input is safe.')
d.add_heading('3. Governance note',level=2)
d.add_paragraph('CareerMatch AI reads either a PDF resume or skills someone types in, along with their job type, career interest, and preferred location. The app only pulls out recognized skills and a degree label, and it compares those with a small CSV file of made-up job listings. The app does not save the uploaded resume to disk on purpose. Someone can download their own run results, and the test script saves evaluation results as JSON. If Gemini is turned on, it gets the extracted skills, degree label, and sample job details, not the full resume or contact information.')
d.add_paragraph('The human checkpoint is before the agents start: users have to check a box confirming that they understand these are sample jobs and that they will review the results themselves. There is also a separate switch for Gemini before anything is sent outside the app. The app never submits job applications, so the final choice stays with the user. I am responsible for the project and for fixing issues that come up. To limit costs and misuse, I cap the PDF size, manual input length, tool calls, and Gemini output length. For now, the biggest limitations are that the job data is only for a demo, the Streamlit website has not been published yet, and a real Gemini API call has not been tested.')
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
footer.add_run('CareerMatch AI • Classroom demonstration • Fictional job data')
d.save(B/'MILESTONE_II_REPORT.docx')
print('saved',B/'MILESTONE_II_REPORT.docx')
