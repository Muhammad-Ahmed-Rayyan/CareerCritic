import streamlit as st
from dotenv import load_dotenv

from utils.file_extract import extract_resume_text
from graph.workflow import build_graph

load_dotenv()

st.set_page_config(page_title="CareerCritic", page_icon="🧭", layout="centered")

st.title("🧭 CareerCritic")
st.caption("A multi-agent LangGraph workflow that reviews your resume against a job description.")

# Build the graph once per session
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

with st.form("input_form"):
    resume_file = st.file_uploader(
        "Upload your resume", type=["pdf", "docx", "txt"]
    )
    job_description = st.text_area(
        "Paste the job description", height=220,
        placeholder="Paste the full job posting here..."
    )
    submitted = st.form_submit_button("Analyze Fit")

if submitted:
    if not resume_file:
        st.error("Please upload a resume file.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        try:
            with st.spinner("Extracting resume text..."):
                resume_text = extract_resume_text(
                    resume_file.name, resume_file.read()
                )

            if not resume_text:
                st.error("Could not extract any text from the uploaded file.")
            else:
                with st.spinner("Running multi-agent analysis (Parser → JobFit → Critic → Writer)..."):
                    initial_state = {
                        "resume_text": resume_text,
                        "job_description": job_description,
                        "parsed_resume": None,
                        "fit_analysis": None,
                        "critique": None,
                        "final_report": None,
                        "retry_count": 0,
                    }
                    result = st.session_state.graph.invoke(initial_state)

                st.success("Analysis complete.")

                # Quick metrics row
                fit_score = result["fit_analysis"]["fit_score"]
                retries = result["retry_count"]
                col1, col2 = st.columns(2)
                col1.metric("Fit Score", f"{fit_score}/100")
                col2.metric("Critic Revisions", max(0, retries - 1))

                st.markdown("---")
                st.markdown(result["final_report"])

                with st.expander("View raw parsed resume (debug)"):
                    st.json(result["parsed_resume"])

        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Something went wrong: {e}")