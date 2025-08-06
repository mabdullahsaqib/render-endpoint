from http.server import BaseHTTPRequestHandler
import json
import sys


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get the content length to read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read the request body
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            if post_data:
                try:
                    json_data = json.loads(post_data.decode('utf-8'))
                    
                    # Log the received JSON to console
                    print(f"Received JSON: {json.dumps(json_data, indent=2)}", file=sys.stderr)
                    
                    # Validate that we have the expected fields (optional validation)
                    expected_fields = ['name', 'email', 'message']
                    received_fields = list(json_data.keys())
                    print(f"Expected fields: {expected_fields}", file=sys.stderr)
                    print(f"Received fields: {received_fields}", file=sys.stderr)
                    
                except json.JSONDecodeError as e:
                    # Handle invalid JSON
                    print(f"Invalid JSON received: {e}", file=sys.stderr)
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = json.dumps({"error": "Invalid JSON format"})
                    self.wfile.write(error_response.encode('utf-8'))
                    return
            else:
                # Handle empty request body
                print("Empty request body received", file=sys.stderr)
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = json.dumps({"error": "Empty request body"})
                self.wfile.write(error_response.encode('utf-8'))
                return
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Return success response
            response = json.dumps({"status": "ok"})
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            # Handle any other errors
            print(f"Error processing request: {e}", file=sys.stderr)
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({"error": "Internal server error"})
            self.wfile.write(error_response.encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
