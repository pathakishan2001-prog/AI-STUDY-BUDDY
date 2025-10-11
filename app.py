import os
import json # You'll need this to handle the raw JSON from the model
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- 1. Load Environment Variables ---
load_dotenv()

app = Flask(__name__)



TEMPORARY_GEMINI_KEY = "AIzaSyA0DA0yjJRTT4Zx1VBgfIygkbE5E7n4z1g" 

try:
    # Use the temporary key directly for the instructor
    client = genai.Client(api_key=TEMPORARY_GEMINI_KEY) 
except Exception as e:
    # Error handling remains the same
    print(f"ERROR: Failed to initialize Gemini Client. Details: {e}")
    client = None

# --- 3. Home Route (Loads the HTML Frontend) ---
@app.route('/')
def home():
    # Flask automatically looks for index.html inside the 'templates' folder
    return render_template('index.html')

# --- 4. API Route (Handles AI Requests) ---
@app.route('/api/studybuddy', methods=['POST'])
def handle_request():
    # Basic check to ensure the client is ready
    if not client:
        return jsonify({"error": "AI client not initialized. Check API key."}), 500

    data = request.json
    action = data.get('action')
    content = data.get('content')

    if not content or not action:
        return jsonify({"error": "Missing content or action in request."}), 400

    # --- Configuration Variables ---
    schema = None
    prompt = ""
    mime_type = "text/plain"
    model = 'gemini-2.5-flash'

    # --- Define Prompts and Configuration based on Action ---
    if action == 'explain':
        prompt = f"Explain the following complex concept in simple, easy-to-understand terms suitable for a high school student. Use analogies where appropriate: {content}"
    
    elif action == 'summarize':
        prompt = f"Provide a concise, bulleted summary of the 5 most important points from the following study notes: {content}"

    elif action == 'quiz':
        # The prompt forces the model to return ONLY the specified JSON structure
        prompt = f"Generate a short, 3-question multiple-choice quiz based ONLY on this text. Return the output as a JSON object ONLY, with questions, four options (A, B, C, D), and the single correct answer letter (e.g., 'A'). Text: {content}"
        
        mime_type = "application/json"
        
        # Define the strict JSON schema the model MUST follow
        schema = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "quiz": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "question": types.Schema(type=types.Type.STRING),
                            "options": types.Schema(
                                type=types.Type.OBJECT,
                                properties={"A": types.Schema(type=types.Type.STRING), "B": types.Schema(type=types.Type.STRING), "C": types.Schema(type=types.Type.STRING), "D": types.Schema(type=types.Type.STRING)}
                            ),
                            "correct_answer": types.Schema(type=types.Type.STRING, description="The letter of the correct option (A, B, C, or D).")
                        }
                    )
                )
            }
        )
    else:
        return jsonify({"error": "Invalid action specified."}), 400
    
    # --- Generate Content from Model ---
    config = types.GenerateContentConfig(
        temperature=0.4,
        response_mime_type=mime_type,
        response_schema=schema if schema else None
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config
        )
        
        # All responses are wrapped in a single JSON object for the frontend to handle
        # The content of the response is stored under the 'result' key.
        return jsonify({"result": response.text}), 200
            
    except Exception as e:
        # Catch any errors during the API call (e.g., rate limits, invalid prompts)
        return jsonify({"error": f"AI Generation Failed: {e}"}), 500

# --- 5. Run the Application ---
if __name__ == '__main__':
    # Running in debug mode allows for automatic code reloading
    app.run(debug=True)