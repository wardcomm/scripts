#!/usr/bin/python
# import http.server as httpserver
# import socketserver

# def main(port=None):
# 	if port is None:
# 		port = 8000
# 	handler = httpserver.SimpleHTTPRequestHandler
# 	try:
# 		print("serving at port", port)
# 		httpd = socketserver.TCPServer(("", port), handler)
# 		print("serving at port", port)
# 		httpd.serve_forever()
# 	except OSError:
# 		print("Given PORT:{} is unavailable.Try running with diffrent PORT Number!".format(port))

# if __name__ == '__main__':
# 	main()
# server.py
import http.server # Our http server handler for http requests
import socketserver # Establish the TCP Socket connections
 
PORT = 9000
 
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
 
Handler = MyHttpRequestHandler
 
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()