import http.server
import socketserver
import threading

import http.server
import socketserver
import threading

class SimpleHTTPServer:
    """
    A simple HTTP server that serves files from the current directory and below.
    
    Attributes:
        port (int): The port number on which the HTTP server will listen.
        server (socketserver.TCPServer): The server instance.
        thread (threading.Thread): The thread on which the server runs.
    """
    
    def __init__(self, port=8080):
        """
        Initializes the SimpleHTTPServer instance with the given port.
        
        Args:
            port (int): The port number on which the HTTP server will listen. Defaults to 8080.
        """
        self.port = port
        self.server = socketserver.TCPServer(("localhost", self.port), http.server.SimpleHTTPRequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    def run(self):
        """
        Starts the HTTP server in a separate thread. This allows the server to run in the background,
        making it possible to perform other tasks in the foreground.
        """
        print(f"Starting server at port {self.port}")
        self.thread.start()  # Correction: Use self.thread.start() instead of self.thread.run()
        print(f"Server running at port {self.port}")

    def stop(self):
        """
        Stops the HTTP server and closes the server socket, freeing up the port and resources.
        It ensures a clean shutdown by properly shutting down the server thread.
        """
        self.server.shutdown()
        self.server.server_close()
        print("Server stopped.")
