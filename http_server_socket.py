#!/usr/bin/python3

import socket
import threading
import datetime

class HttpServerSocket(socket.socket):
	def __init__(self, ip, port):
		socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
		self.bind((ip, port))
		self.listen(5)
		self.accept_thread = threading.Thread(target=self.worker_thread)
		self.accept_thread.daemon = True
		self.accept_thread.start()
		self.http_handlers = []
		print('[HttpServerSocket] socket started on %s:%d\n' % (ip, port))

	def bind_http_handler(self, handler):
		self.http_handlers.append(handler)

	def send_response(self, client_socket, response):
		(status_code, content_type, response_text) = response
		raw = 'HTTP/1.1 %d\n' % (status_code)
		raw += 'Date: %s\n' % (datetime.datetime.today().strftime('%a, %-d %b %Y %-H:%-M:%-S GMT'))
		raw += 'Server: trainchecker-webserver\n'
		raw += 'Content-Type: %s\n' % (content_type)

		if len(response_text) > 0:
			raw += 'Content-Length: %d\n\n%s\n' % (len(response_text), response_text)

		client_socket.send(raw)
		client_socket.close()


	def handle_client(self, client_socket, client_address):
		request = client_socket.recv(1024)
		#print('[HttpServerSocket] received -> {}'.format(request))
		for handler in self.http_handlers:
			response = handler.handle_request(request)
			if response == False:
				continue
			self.send_response(client_socket, response)
			return

	def worker_thread(self):
		print('[HttpServerSocket] accepting worker thread started\n')
		while True:
			(client_socket, client_address) = self.accept()
			print('[HttpServerSocket] accepted incoming connection from %s:%d\n' % (client_address))
			client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address,))
			client_thread.daemon = True
			client_thread.start()
