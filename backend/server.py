from flask import Flask, request, jsonify
from flask_cors import CORS
from new_main import the_final
import os

app = Flask(__name__)
CORS(app)  

TEXT_FILE = "received_text.txt"  # File to store received text

@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Invalid input"}), 400

        text = data['text']
        print(text)
        the_final(text)
        return 
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)