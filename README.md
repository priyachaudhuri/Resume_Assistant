# 📄 Resume Assistant with Google Gemini API

Resume Assistant is a Streamlit-based AI-powered web app that helps you generate job-specific application materials, including tailored professional summaries, key skills, and cover letters, using the power of Google Gemini (Generative AI).

---

## 🚀 Features

- ✅ Extracts **key technical and soft skills** from any job description.
- ✍️ Generates a **custom professional summary** aligned with your resume and the role.
- 💼 Creates a **tailored cover letter** using your background and the job posting.
- ⚡ Built on the fast and efficient **`gemini-2.5-flash`** model.
- 🧠 Smart prompt design with editable cover letter template.
- 🖥️ Easy-to-use, responsive **Streamlit** interface.

---

## 🔧 Setup Instructions

1. **Install dependencies**:
   pip install streamlit google-generativeai
2. **Get your Gemini API key**:
   - Go to Google AI Studio and sign in.
   - Generate your API key.
3. Add your API key:
    - Open resume_assistant.py.
    - Search for the section labeled "#API Key".
    - Replace 'YOUR_GEMINI_API_KEY_HERE' with your actual key: genai.configure(api_key='YOUR_GEMINI_API_KEY_HERE') #API Key
---

## ▶️ Run the App
Launch the app locally using: streamlit run resume_assistant.py

This will open the app in your default browser.

---

## 📝 How to Use
1. Paste the job description into the input box.
2. Fill in your personal information — name, email, LinkedIn, etc.
3. Enter your skills and optionally provide a resume summary.
🛠️ Tip: The app includes pre-filled demo values (like "Jane Doe", a generic summary, and example skills) to help you explore functionality. Replace these with your own data for real use.
4. Click "🚀 Generate Application Materials".
5. Instantly receive: ✅ Key Skills 📝 Resume Summary ✉️ Cover Letter

---

## 💡 Customization
- To help users test the app without needing to enter everything from scratch, the following fields are pre-filled. Please add or update or remove these demo values before using the output professionally.
   - **Name: Jane Doe**
   - **Email: jd@xyz.com**
   - **Phone (optional): +1 (123) 456-0789**
   - **Latest Position Held: Business Analyst**
   - **Skills: SQL, Tableau, Excel, Word, PowerPoint**
   - **Resume Summary: A general data analyst profile**
- Want to adjust the tone, add specific examples, or align it with your industry? Go ahead and tailor the prompt to your needs. You can easily customize the cover letter template inside the generate_cover_letter_gemini() function in resume_assistant.py.

---
## ⚠️ Notes
- Be aware of API usage quotas and billing limits from Google.
- This app is optimized for gemini-2.5-flash — a fast and lightweight model.
- You may switch to gemini-pro if you prefer deeper responses (note potential cost differences).
---
## 👩‍💻 Author
**Priya Chaudhuri**

Feel free to reach out or contribute to the project!
