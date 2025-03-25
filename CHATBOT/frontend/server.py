from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class ChatHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read content length
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            request_json = json.loads(post_data.decode('utf-8'))
            response = {"message": f"Received: {request_json}"}

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"ChattyBot Server Running!")

# Start the server
PORT = 8000
server = HTTPServer(("0.0.0.0", PORT), ChatHandler)
print(f"Server running on http://localhost:{PORT}")
server.serve_forever()
