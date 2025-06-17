import streamlit as st
import google.generativeai as genai
import re
from datetime import datetime

# Configure Gemini API
# Load API key
try:
    genai.configure(api_key='YOUR_GEMINI_API_KEY_HERE') #API Key
except KeyError:
    st.error("Gemini API Key Not Found.")
    st.stop() # Stop the app if no API key is found

# Initialize the generative model
# You can choose 'gemini-pro' for text-based tasks
# Using gemini-2.5-flash as specified, which is a good, fast choice
model = genai.GenerativeModel('gemini-2.5-flash')

# --------- Helper Functions --------- #

@st.cache_data(show_spinner=False) # Cache results for faster re-runs
def get_gemini_response(prompt_text):
    """Sends a prompt to Gemini and returns the generated text."""
    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        st.error(f"Error Communicating Wwith Gemini API: {e}")
        return None

def analyze_job_description_gemini(job_desc):
    """Uses Gemini to extract key skills from job description."""
    prompt = f"""From the following job description, identify and list up to 15 key technical and soft skills that are explicitly mentioned or strongly implied as requirements. List them as a comma-separated string, e.g., "Python, SQL, Data Analysis, Communication, Project Management".
    
    Job Description:
    {job_desc}
    
    Skills:"""
    response_text = get_gemini_response(prompt)
    if response_text:
        # Clean up response: remove newlines, extra spaces, and split by comma
        skills_list = [skill.strip().title() for skill in response_text.replace('\n', '').split(',') if skill.strip()]
        return list(set(skills_list))[:15] # Return unique skills, limited to 15
    return []

def generate_resume_suggestions_gemini(required_skills, current_resume, current_skills, job_title, years_experience):
    """Uses Gemini to generate resume suggestions."""
    job_skills_str = ', '.join(required_skills)
    user_skills_str = ', '.join([s.strip() for s in current_skills.split(',') if s.strip()])

    # Prompt for Professional Summary (unchanged)
    summary_prompt = f"""You are a career coach. Based on the following information, generate a concise (3-4 sentences) professional summary for a resume. Focus on achievements, relevant skills, and the target job role.

    Job Title applying for: {job_title}
    Years of Experience: {years_experience}
    Required Skills for the Job: {job_skills_str}
    Your current skills: {user_skills_str}
    Your current resume summary (if provided, use for context but don't just copy): {current_resume if current_resume else 'N/A'}

    Professional Summary:"""
    professional_summary = get_gemini_response(summary_prompt)

    # Prompt for Skills to Highlight and Keywords (unchanged)
    skills_keywords_prompt = f"""You are a resume expert. Based on the job's required skills and the user's current skills, suggest skills to highlight on a resume and additional keywords to include.
    
    Required Skills for the Job: {job_skills_str}
    Your Current Skills (comma-separated): {user_skills_str}

    Format your response with two sections:
    1. Skills to Emphasize (comma-separated list of skills you possess that are required for the job, or general advice if no direct matches)
    2. Keywords to Add (comma-separated list of unique skills from required_skills not in current_skills, plus any other relevant keywords for the job title)
    """
    skills_keywords_response = get_gemini_response(skills_keywords_prompt)

    # --- DIAGNOSTIC STEP: Print the raw response from Gemini (Keep this!) ---
    if skills_keywords_response:
        st.sidebar.subheader("Raw Gemini Response (Skills/Keywords Debug):")
        st.sidebar.text(skills_keywords_response)
    else:
        st.sidebar.info("No raw Gemini response received for skills/keywords (possible API error).")
    # --- END DIAGNOSTIC STEP ---


    # Initialize with default/fallback messages
    skills_to_highlight = "Focus on transferable skills and those directly matching the job description."
    keywords = "Include relevant industry terms and action verbs."

    if skills_keywords_response:
        # skills_match: Captures content after "1. **Skills to Emphasize**:" non-greedily,
        # stopping *precisely* before the "2. **Keywords to Add**:" header.
        # Added re.IGNORECASE for "to/To" in Keywords To Add.
        skills_match = re.search(
            r'1\.\s*[-*]?\s*\*\*Skills to Emphasize\*\*:\s*(.*?)(?=\n*\s*2\.\s*[-*]?\s*\*\*Keywords to Add\*\*|\Z)',
            skills_keywords_response, re.DOTALL
        )
        
        # keywords_match: Account for "2.", optional leading bullet, bolding, and colon
        keywords_match = re.search(
            r'2\.\s*[-*]?\s*\*\*Keywords to Add\*\*:\s*(.*)',
            skills_keywords_response, re.DOTALL
        )

    return {
        'professional_summary': professional_summary if professional_summary else "Could not generate summary.",
        'skills_to_highlight': skills_to_highlight,
        'keywords': keywords
    }


def generate_cover_letter_gemini(job_title, company, name, email, phone, current_position, years_experience, current_skills, required_skills, linkedin_url):
    """Uses Gemini to generate a personalized cover letter."""
    
    required_skills_str = ', '.join(required_skills)
    current_skills_str = ', '.join([s.strip() for s in current_skills.split(',') if s.strip()])

    prompt = f"""You are a professional cover letter writer. Write a compelling cover letter for a job application. The letter should be professional, concise, and highlight the candidate's relevant experience and skills as they relate to the job description and company.

    Candidate Information:
    Name: {name}
    Email: {email}
    Phone: {phone}
    LinkedIn: {linkedin_url if linkedin_url else 'N/A'}
    Years of Experience: {years_experience}
    Latest Position: {current_position}
    Current Skills: {current_skills_str}

    Job Information:
    Job Title: {job_title}
    Company: {company}
    Key Skills required by Job Description: {required_skills_str}

    Cover Letter Structure:
    - Start with a strong opening expressing interest and mentioning where they saw the ad (assume LinkedIn or company website).
    - Briefly state their relevant experience and align it with the company's mission or values (if known, otherwise general enthusiasm for the field).
    - Pick 2-3 key skills or experiences from the candidate's background that directly match the 'Key Skills required by Job Description' and elaborate briefly on accomplishments using those skills. If specific examples from the original code are relevant (like "led over 40 engagements" or "improved operational efficiency by 60%"), try to incorporate them naturally if they align with the generated content.
    - Express enthusiasm for the specific company and role, mentioning their reputation if appropriate.
    - Conclude with a call to action to discuss further.
    - Here is the template: 
    I am writing to express my strong interest in the {job_title} position at {company}, advertised on [Platform where you saw the ad]. With {years_experience} years of experience in data analytics, automation, and business optimization, I am confident my technical skills, business insight, and leadership experience align well with {company}'s data-driven approach.
    Throughout my career, I've developed a proven ability to transform complex data into actionable insights, significantly optimizing business processes, and enhancing operational efficiency. I excel at leading cross-functional teams and effectively communicating complex technical information to diverse stakeholders.
    I am eager to leverage my analytical and leadership abilities to contribute to {company}'s continued success. Thank you for your time and consideration; I look forward to discussing this opportunity.
    
    Sincerely,
    {name}
    {email}
    {phone}

    Cover Letter:"""

    cover_letter = get_gemini_response(prompt)
    return cover_letter if cover_letter else "Could not generate cover letter."

# --------- Streamlit UI --------- #

st.set_page_config(page_title="Resume Assistant", page_icon="📄", layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
    }
    .section-header {
        font-size: 1.5rem;
        margin-top: 2rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        color: #2c3e50;
    }
    .result-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .skill-tag {
        background-color: #e1f5fe;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 5px;
        display: inline-block;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">📄 Resume Assistant</div>', unsafe_allow_html=True)
st.markdown("Paste A Job Description And Get A Tailored Professional Summary, Skills Suggestions, And A Cover Letter Using The **Gemini API**.")

# Inputs
st.markdown('<div class="section-header">🎯 Job Description</div>', unsafe_allow_html=True)
job_desc = st.text_area("Paste The Job Description Here", height=200)

st.markdown('<div class="section-header">👤 Your Information (Please Edit As Required)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    full_name = st.text_input("Full Name*", value="Jane Doe")
    email = st.text_input("Email*", value="jd@xyz.com")
    phone = st.text_input("Phone (optional)", value="+1 (123) 456-0789")
    job_title = st.text_input("Job Title You’re Applying For*", placeholder="Data Analyst")
with col2:
    company_name = st.text_input("Company Applying To*", placeholder="ABC Inc.")
    current_position = st.text_input("Latest Position Held", value="Business Analyst")
    years_experience = st.number_input("Years of Experience", 0, 50, placeholder=0)
    linkedin_url = st.text_input("LinkedIn URL", placeholder="https://www.linkedin.com/in/****/")

# IMPORTANT: Ensure this line is present to define current_resume
st.markdown("**Current Resume or Summary (optional):**")
current_resume = st.text_area("Your Resume Summary (Please Edit As Required)", height=120, value = 'A detail-oriented Data Analyst with a solid foundation in statistical analysis and data visualization. I bring proven experience in transforming complex datasets into actionable insights to support strategic decision-making and optimize business performance. Eager to leverage strong SQL, Python, and Tableau skills to contribute to data-driven growth.')
st.markdown("**Your Key Skills (comma-separated):**")
current_skills = st.text_area("Skills (Please Edit As Required)", value="SQL, Tableau, Excel, Word, PowerPoint", height=80)

# Button
st.markdown("---")
if st.button("🚀 Generate Application Materials"):
    if job_desc and full_name and email and job_title and company_name:
        with st.spinner("Analyzing and Generating... This May Take A Moment."):
            # Use Gemini-powered functions
            required_skills = analyze_job_description_gemini(job_desc)
            # Make sure current_resume is passed here
            resume_suggestions = generate_resume_suggestions_gemini(required_skills, current_resume, current_skills, job_title, years_experience)
            cover_letter = generate_cover_letter_gemini(
                job_title, company_name, full_name, email, phone, current_position,
                years_experience, current_skills, required_skills, linkedin_url
            )

            # Results
            st.markdown("### 🧠 Key Skills Detected")
            if required_skills:
                skills_html = ''.join(f'<span class="skill-tag">{skill}</span>' for skill in required_skills)
                st.markdown(f'<div class="result-box">{skills_html}</div>', unsafe_allow_html=True)
            else:
                st.info("No Key Skills Detected Or An Error Occurred During Skill Extraction.")

            st.markdown("### 📝 Resume Suggestions")
            st.markdown(f"<div class='result-box'><strong>Professional Summary:</strong><br>{resume_suggestions['professional_summary']}</div>", unsafe_allow_html=True)

            st.markdown("### ✉️ Cover Letter")
            st.markdown(f"<div class='result-box' style='white-space: pre-wrap'>{cover_letter}</div>", unsafe_allow_html=True)
    else:
        st.error("Please Fill In All Required Fields Marked With *.")

# Footer
st.markdown("---")
st.markdown("*Created With ❤️ Using Streamlit and Google Gemini API • Resume Assistant*")