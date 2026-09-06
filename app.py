import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

@app.route('/')
def index():
    return "SecOps-AI Cloud Run Auditor is Active."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
