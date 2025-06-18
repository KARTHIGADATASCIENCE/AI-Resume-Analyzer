# 📄 AI Resume Analyzer (Gemini 2.0 Flash + Streamlit)

This app analyzes a resume against a job description using **Google Gemini 2.0 Flash**, and provides:

- 🛠️ Key skills extracted from the resume
- 📈 A match score out of 100%
- ✨ Personalized suggestions to improve your resume

---

## 🚀 Features

- Upload resume and job description as PDFs
- Automatically extract text from both files
- Clean, sectioned output using Google Gemini's LLM
- Optional fallback to manual text input
- Built with Streamlit + Gemini API + PyMuPDF

---

## 🔧 Tech Stack

- `streamlit` – UI
- `requests` – Gemini API call
- `pymupdf` – PDF reader
- `python-dotenv` – API key loading
- Powered by [Google AI Studio (Gemini)](https://makersuite.google.com/)



---

## 🔑 Environment Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/ai-resume-analyzer.git
   cd ai-resume-analyzer
2. create .env file paste your api key 
    GEMINI_API_KEY=your_actual_google_api_key_here

3. Install the dependencies:

    ```bash
     pip install -r requirements.txt
4. Run the app:
    ```bash
    streamlit run app.py
5. Sample Testing Files
    You can use the following files included in the repo to test:

    sample_resume.pdf

    sample_job_description.pdf

    They contain example resume and job description content for demo purposes.

##  Author
# Karthiga Alias Amali 
 - PG Data Science Student
- Aspiring Data Scientist | AI Project Builder | Streamlit Developer

## Credits
   - Google AI Studio (Gemini)
    - Streamlit
    - PyMuPDF


