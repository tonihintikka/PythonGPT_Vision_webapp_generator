import os
import http.server
import socketserver
import threading


def start_server(port=8000, directory='data'):
    os.chdir(directory)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving at http://localhost:{port}")
        httpd.serve_forever()


if __name__ == '__main__':
    # Start the server in a new thread
    server_thread = threading.Thread(target=start_server, args=(8000,))
    # This ensures the thread exits when the main program does
    server_thread.daemon = True
    server_thread.start()
