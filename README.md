🧠 AI-Powered Study Buddy- 

A minimalist web application built with Flask and the Gemini API to transform raw study notes into personalized learning tools instantly. This project was developed as a Capstone project to demonstrate core principles of Generative AI integration and structured data processing.

✨ Features- 

This Study Buddy provides essential tools for active recall and comprehension:

Explain Simply: Takes a complex topic and rewrites it in clear, simplified language, useful for quick conceptual understanding.

Summarize Notes: Condenses lengthy text into 3-5 concise, bulleted key takeaways, maximizing review efficiency.

Generate Quiz: Enforces the Gemini API to return a structured JSON object to create a functional, multiple-choice quiz based purely on the input material.

Component,Technology,Role
Backend Framework,Python 3 / Flask,Lightweight server to manage routing and API key handling.
AI Model,Gemini 2.5 Flash API,Generative model for content creation and structured JSON output.
Frontend,"HTML, CSS, JavaScript","Clean, minimalist interface for user interaction and dynamic quiz display."

🚀 Getting Started- 

Follow these steps to clone the repository, install dependencies, and run the application locally.

Prerequisites
Ensure you have the following installed on your system:

Python 3.9+

pip (Python package installer)

Git (for cloning the repository)

1. Clone the Repository
Open your terminal and clone the project:

git clone https://github.com/pathakishan2001-prog/AI-STUDY-BUDDY.git
cd AI-STUDY-BUDDY

2. Set Up the Environment
Create and activate a Python virtual environment:
# Create the virtual environment
python -m venv venv

# Activate the environment (PowerShell)
.\venv\Scripts\activate

3. Install Dependencies
Install all required libraries:
pip install flask google-genai python-dotenv

4. Run the Application
The API key has been hardcoded in app.py for immediate testing purposes. No separate .env file is required for this demonstration.

Start the Flask development server:
python app.py

Open your web browser and navigate to the local address:

http://127.0.0.1:5000

AI-STUDY-BUDDY/
├── app.py              # Flask backend, AI prompt logic, and temporary API key
├── .gitignore          # Excludes the development environment (.venv)
├── static/
│   └── style.css       # Basic styling for the frontend
└── templates/
    └── index.html      # The frontend HTML interface

👤 Author-
Ishan Pathak
