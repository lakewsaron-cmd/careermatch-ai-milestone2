# CareerMatch AI — Milestone II

A public-deployment-ready **classroom demo** with a Profile Agent, Job Search Agent, and Match Agent.

**Important:** The five saved job listings are **fictional demonstration listings**, not open vacancies. This is not a live job search and it will not apply on anyone's behalf.

## What works

- Profile Agent uses a real PDF extraction tool (PyMuPDF) or accepts manually entered skills.
- Job Search Agent reads a real local CSV file and filters fictional listings by job type and location.
- Match Agent ranks by required-skill overlap, identifies skills not listed in the resume, and explains results.
- Optional Gemini tool explains the strongest match using only extracted skills/degree and demo job data; a valid Gemini API key is required.
- Strict **maximum 4 tool-call guard**, visible execution trace, and safety/human-review consent gate.
- 12 automated evaluation cases × 3 runs = 36 offline checks. Includes adversarial text and oversized input cases.

## Run locally

1. Install Python 3.10+.
2. From this folder run `python -m pip install -r requirements.txt`.
3. Run `streamlit run app.py` and open the URL displayed in the terminal.
4. Enter `Python, SQL, Excel` in manual skills, or upload a text-based PDF resume, check the consent box, and click **Find matching roles**.
5. Expand the execution trace and download the JSON evidence after the run.

Optional Gemini: Set the environment variable `GEMINI_API_KEY` or configure the key in Streamlit Community Cloud app **Secrets** as `GEMINI_API_KEY = "..."`. Never put the real key in source code or GitHub. If no key is configured, leave Gemini disabled and the whole offline workflow still works.

## Publish to a genuinely public URL (required by instructor)

1. Create a GitHub repository, for example `careermatch-ai-milestone2`.
2. Upload the **contents of this folder** to the repository root, including `.streamlit/config.toml`, `app.py`, `pipeline.py`, `sample_jobs.csv`, and `requirements.txt`. Do **not** upload any resume or actual `secrets.toml`.
3. Visit https://share.streamlit.io, sign in with GitHub, and choose **Create app**. Select the repository and `app.py` as the entrypoint, then deploy.
4. Make the app **public** in its sharing settings. Verify it works in an incognito/private browser window **without a login**. Copy the actual `https://...streamlit.app` URL into your assignment submission.
5. To enable Gemini, add `GEMINI_API_KEY` using the host's app Secrets settings. Verify the API call with your key, check any usage limits/costs, and run the public demo again.
6. Leave Streamlit sharing settings and project permissions configured so the link stays open during class. Be aware free hosting services may sleep or restart.

A public link has **not** been created by this package. Deployment requires your GitHub/Streamlit account.

## Run the evaluation and actual resume trace

```
python evaluate.py
python -m pytest -q tests
python demo.py --resume /path/to/your-resume.pdf --output evidence/my_resume_trace.json
```

The sample evidence folder includes an execution trace created from the user's actual supplied resume, with personal contact information excluded. **The uploaded resume itself is not bundled**. The evaluation's 36 runs are offline, not Gemini calls. The offline model is deterministic; pass@1 and pass^3 are both 100% because all 12 specified cases passed each of 3 runs after a fix to oversized input validation.

## Governance / security

- **Data read:** Uploaded PDF (in memory), recognized skills/degree, chosen preferences, saved fictional CSV listings. App does not intentionally persist resumes or contact information. Hosting systems may still produce standard logs.
- **Data written:** A run trace can be downloaded by the user; local evaluation scripts create evidence JSON files. The public app does not save uploads to disk.
- **Gemini sent:** Recognized skill names, degree string, and fictional posting details only; no name, email, phone, or raw resume content.
- **Human gate:** Consent checkbox before starting; separate Gemini enablement toggle before any external request. Users review matches and decide whether to apply.
- **Caps:** 2MB/5-page PDF limit, 1,000-character manual input, 100-character search fields, maximum 4 tool calls, Gemini max 240 output tokens per call and 20-second HTTP timeout. These are per-run safety limits, not account-wide daily quotas.
- **Threats/limits:** Prompt injection is ignored as instructions, but any LLM output still needs user review; no actual job verification, live API or privacy/security assessment is claimed.
- **Responsible maintainer:** Saron Lakew.

## Files

- `app.py`: Streamlit interface and human gate.
- `pipeline.py`: agents, tools, guard, Gemini integration.
- `sample_jobs.csv`: fictional sample internships and jobs.
- `evaluate.py`, `tests/`: 12-case x3-run evaluation plus unit tests.
- `evidence/evaluation_results.json`: actual recorded offline results.
- `evidence/real_resume_trace.json`: actual PDF parsing, retrieval and ranking trace (contact details omitted).
- `MILESTONE_II_REPORT.docx`: draft deliverable with governance note and evaluation summary; insert your real public link after publishing.

## Honest verification scope

Python pipeline and tests have run in the build environment. This environment does not have Streamlit installed and no Gemini API key was supplied, so **public hosted UX and live Gemini requests have not been verified**. Perform those two checks after deployment. Do not represent the offline test results as live Gemini performance.
