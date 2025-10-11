import os
import json
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TEMPORARY_GEMINI_KEY = "AIzaSyA0DA0yjJRTT4Zx1VBgfIygkbE5E7n4z1g" 

try:
    client = genai.Client(api_key=TEMPORARY_GEMINI_KEY) 
except Exception as e:
    print(f"ERROR: Failed to initialize Gemini Client. Details: {e}")
    client = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/studybuddy', methods=['POST'])
def handle_request():
    if not client:
        return jsonify({"error": "AI client not initialized. Check API key."}), 500

    data = request.json
    action = data.get('action')
    content = data.get('content')

    if not content or not action:
        return jsonify({"error": "Missing content or action in request."}), 400

    schema = None
    prompt = ""
    mime_type = "text/plain"
    model = 'gemini-2.5-flash'

    if action == 'explain':
        prompt = f"Explain the following complex concept in simple, easy-to-understand terms suitable for a high school student. Use analogies where appropriate: {content}"
    
    elif action == 'summarize':
        prompt = f"Provide a concise, bulleted summary of the 5 most important points from the following study notes: {content}"

    elif action == 'quiz':
        prompt = f"Generate a short, 3-question multiple-choice quiz based ONLY on this text. Return the output as a JSON object ONLY, with questions, four options (A, B, C, D), and the single correct answer letter (e.g., 'A'). Text: {content}"
        
        mime_type = "application/json"
        
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
        
        return jsonify({"result": response.text}), 200
            
    except Exception as e:
        return jsonify({"error": f"AI Generation Failed: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)