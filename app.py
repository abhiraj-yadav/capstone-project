from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Cohere client using the API key
print("KEY:", os.getenv("COHERE_API_KEY"))
co = cohere.Client(os.getenv("COHERE_API_KEY"))

@app.route('/api/enhance', methods=['POST'])
def enhance_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({ 'error': 'No text provided' }), 400

    original_text = data['text']
    prompt = f"Improve the grammar and clarity of the following text:\n\n{original_text}"
    try:
        response = co.chat(
            model="command-r-plus",
            message=prompt  # singular!
        )
        improved_text = response.text.strip()
        return jsonify({ 'enhanced_text': improved_text })
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)