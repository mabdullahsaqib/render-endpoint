from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def handle_post():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Log the received data to console
        logger.info(f"Received data: {data}")
        
        # Extract fields (optional validation)
        name = data.get('name', 'Not provided')
        email = data.get('email', 'Not provided')
        message = data.get('message', 'Not provided')
        
        # Log individual fields
        logger.info(f"Name: {name}, Email: {email}, Message: {message}")
        
        # Return success response
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"status": "error", "message": "Invalid request"}), 400

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Flask app is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
