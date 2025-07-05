# backend/app.py (backend main body)

from flask import Flask, request, jsonify #
from flask_cors import CORS
import cohere
import os
from dotenv import load_dotenv

# Load environment variables from .env (basically api key call karne ke liye)
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS (taki extension API call kar sake chrome par)

# Initialize Cohere client using the API key
co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
# Phele cohere: co = cohere.Client(api_key=os.getenv("COHERE_API_KEY")) use kara tha agar work nahi karega toh isse replace karke check kar sakte hai

@app.route('/api/enhance', methods=['POST'])
def enhance_text():
    """
    API endpoint that improves grammar and clarity of the given text.
    Expects JSON: { "text": "..." }
    Returns JSON: { "enhanced_text": "..." }
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({ 'error': 'No text provided' }), 400

    original_text = data['text']
    prompt = f"Improve the grammar and clarity of the following text:\n\n{original_text}"
    try:
        # Call Cohere chat endpoint (taki kya theek karna hai woh pata chal jai)  
        response = co.chat(
            model="command-a-03-2025", 
            messages=[{"role": "user", "content": prompt}]
        )
        improved_text = response.message.content[0].text.strip()
        return jsonify({ 'enhanced_text': improved_text })
    except Exception as e:
        # agar error aaia toh 
        return jsonify({ 'error': str(e) }), 500

if __name__ == '__main__':
    # Run the Flask app (default port 5000)
    app.run(host='127.0.0.1', port=5000, debug=True)