import streamlit as st
import requests
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API details
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
HEADERS = {
    "Content-Type": "application/json",
    "x-goog-api-key": API_KEY
}

# Build Gemini prompt
def build_prompt(resume, job_desc):
    return f"""
You are a professional career advisor. Given a resume and a job description, do the following:

1. Extract and list the key skills from the resume.
2. Compare them with the job description and give a match score out of 100%.
3. Suggest three improvements to make the resume better suited for the job.

Resume:
{resume}

Job Description:
{job_desc}
"""

# Extract text from uploaded PDF
def extract_pdf_text(uploaded_file):
    text = ""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")
        return ""

# Streamlit UI
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI Resume Analyzer with Gemini")
st.markdown("Upload your resume and job description (PDF or text) to get AI-powered feedback using **Google Gemini 2.0 Flash**.")

# Upload section
st.markdown("### 📎 Upload PDF Files")
resume_pdf = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
jd_pdf = st.file_uploader("📝 Upload Job Description (PDF)", type=["pdf"])

# Extract text
resume_text = extract_pdf_text(resume_pdf) if resume_pdf else ""
jd_text = extract_pdf_text(jd_pdf) if jd_pdf else ""

# Fallback to text input if needed
st.markdown("---")
st.markdown("### ✍️ Or Paste Manually")

if not resume_text:
    resume_text = st.text_area("Paste your resume text here", height=250)

if not jd_text:
    jd_text = st.text_area("Paste the job description here", height=250)

# Analyze button
if st.button("🔍 Analyze Resume"):
    if not resume_text or not jd_text:
        st.warning("Please provide both resume and job description (via upload or text).")
    else:
        with st.spinner("Analyzing with Gemini 2.0 Flash..."):
            try:
                prompt = build_prompt(resume_text, jd_text)
                response = requests.post(API_URL, headers=HEADERS, json={
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ]
                })

                if response.status_code == 200:
                    result = response.json()
                    output = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ Analysis complete!")

                    # Sectioned display
                    st.markdown("### 🧠 Gemini's Resume Analysis")
                    st.markdown("---")

                    parts = output.split("3. Suggested Resume Improvements:")
                    if len(parts) != 2:
                        parts = output.split("3. Suggested Improvements for the Resume:")

                    if len(parts) == 2:
                        top_section, suggestions = parts
                        skills_score = top_section.strip().split("2. Resume-Job Description Match Score:")

                        if len(skills_score) == 2:
                            skills, score = skills_score
                            st.markdown("#### 🛠️ Extracted Key Skills")
                            st.markdown(f"<div style='padding-left:15px'>{skills.strip()}</div>", unsafe_allow_html=True)

                            st.markdown("#### 📈 Match Score")
                            st.markdown(f"<div style='padding-left:15px'>{score.strip()}</div>", unsafe_allow_html=True)

                        st.markdown("#### ✨ Suggestions for Improvement")
                        st.markdown(f"<div style='padding-left:15px'>{suggestions.strip()}</div>", unsafe_allow_html=True)

                    else:
                        st.markdown("### 📄 Gemini Output")
                        st.write(output)

                else:
                    st.error(f"❌ API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
