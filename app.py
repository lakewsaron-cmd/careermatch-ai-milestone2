"""Run: streamlit run app.py"""
import json, os
from pathlib import Path
import streamlit as st
from pipeline import run_pipeline, MAX_UPLOAD_BYTES

st.set_page_config(page_title='CareerMatch AI',page_icon='🎓',layout='wide')
st.title('🎓 CareerMatch AI')
st.caption('Milestone II • Profile Agent → Job Search Agent → Match Agent')
st.warning('CLASSROOM DEMO: Every job listing is fictional. No real openings, guaranteed qualifications, or application links are provided.')
st.info('Only a skills/degree summary is used for matching. Uploaded PDF text is processed in memory and not intentionally saved. If Gemini is enabled, only the skills/degree summary and sample job information are sent to Google.')

with st.sidebar:
    st.header('Safety and limits')
    st.write('Maximum 4 tool calls per request. Gemini is optional; requests can consume API quota.')
    st.write('A person must review each recommendation before applying. This demo never applies to jobs.')
    use_gemini=st.checkbox('Enable Gemini explanation',value=False)
    model=st.selectbox('Gemini model',['gemini-2.5-flash'])
    st.caption('For deployment, configure GEMINI_API_KEY in Streamlit Secrets. Never paste keys into the repo.')

resume=st.file_uploader('Upload a text-based PDF resume (optional, max 2 MB and 5 pages)',type='pdf')
manual=st.text_area('Or enter your skills',placeholder='Python, SQL, Excel, Power BI',max_chars=1000)
a,b=st.columns(2)
with a:
    kind=st.selectbox('Job type',['Internship','Full-Time','Both'])
    interest=st.text_input('Career interest',value='data',max_chars=100)
with b:
    location=st.text_input('Preferred location (remote always included)',value='Atlanta',max_chars=100)
    steps=st.slider('Max tool calls (stop condition)',1,4,4)
consent=st.checkbox('I understand these are fictional sample roles, I will review results myself, and Gemini (if enabled) receives a limited skill summary.')

if st.button('Find matching roles',type='primary'):
    if not consent:
        st.error('Please review and check the safety notice first.')
    elif resume is None and not manual.strip():
        st.error('Upload a resume or enter your skills.')
    elif resume is not None and resume.size > MAX_UPLOAD_BYTES:
        st.error('PDF exceeds the 2 MB limit.')
    else:
        key=''
        if use_gemini:
            try:key=st.secrets.get('GEMINI_API_KEY','')
            except Exception:key=os.getenv('GEMINI_API_KEY','')
            if not key: st.error('Gemini is not configured. Disable Gemini to use the complete offline workflow.')
        if not use_gemini or key:
            with st.spinner('Agents are running...'):
                output=run_pipeline(pdf_bytes=resume.getvalue() if resume else None,
                     manual_skills=manual,job_type=kind,interest=interest,location=location,
                     max_steps=steps,gemini_key=key,gemini_model=model)
            st.subheader('Run result')
            st.write(f"**{output['status']}** — {output['stop_reason']} ({output['mode']})")
            if output['profile']:
                st.write('Recognized skills: '+(', '.join(output['profile']['skills']) or 'None identified'))
            for job in output['results'][:5]:
                with st.container(border=True):
                    st.markdown(f"**{job['title']}** — {job['organization']}")
                    st.write(f"{job['skill_overlap_percent']}% listed-skill overlap (not a hiring probability)")
                    st.write('Matches: '+(', '.join(job['matched_skills']) or 'None'))
                    st.write('Not listed in resume: '+(', '.join(job['not_listed_in_resume']) or 'None'))
                    st.write(job.get('gemini_explanation',job['why']))
                    st.caption(job['source'])
            st.subheader('Execution trace')
            st.json(output['trace'])
            st.download_button('Download run trace',json.dumps(output,indent=2),file_name='careermatch_trace.json',mime='application/json')

with st.expander('How the agent works and who is responsible'):
    st.write('Profile Agent extracts skills; Job Search Agent loads saved fictional listings; Match Agent calculates overlap and may request an optional Gemini explanation. A human decides whether to apply. Demo maintainer: Saron Lakew.')
    st.write('No external job search or employer data is used in this version. Uploaded information is not written to local files by application code.')
