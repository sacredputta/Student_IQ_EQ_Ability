from flask import Flask, render_template, request, jsonify
from app import calculate_total_score

app = Flask(__name__)

# Route 1: Serve the Frontend UI
@app.route('/')
def home():
    return render_template('index.html')

# Route 2: The API Endpoint to process data
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        # Get input from the frontend request
        transcript = data.get('transcript', '')
        duration = data.get('duration', 0)
        
        # Basic Validation
        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400
            
        # Convert duration to float (in case it comes as a string)
        try:
            duration = float(duration)
        except ValueError:
            return jsonify({"error": "Invalid duration format"}), 400

        # CALL THE LOGIC FUNCTION
        # This uses the calculate_total_score function we wrote in logic.py
        results = calculate_total_score(transcript, duration)
        
        # Return the structured JSON response
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Debug mode is on so you can see errors in the console
    app.run(debug=True)