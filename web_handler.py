#!/usr/bin/python3

import threading
import re
import sys
import json
import os
from base_handler import BaseHandler

class WebHandler(BaseHandler):
	def __init__(self, web_path):
		BaseHandler.__init__(self)
		if not web_path.endswith('/'):
			web_path = web_path + '/'

		self.web_path = web_path

	def internal_handle_request(self, deserialized_request):
		pattern = re.compile("\/web\\/(\\w.+)")
		matches = pattern.match(deserialized_request)
		if not matches:
			request_file = 'index.html'
		else:
			request_file = matches.group(1)

		request_file = request_file.replace('..', '.')

		return self.load_and_return_file(self.web_path + request_file)

	def get_mime_type(self, request_file):
		if request_file.endswith('.html'):
			return 'text/html'
		if request_file.endswith('.css'):
			return 'text/css'
		if request_file.endswith('.png'):
			return 'image/png'
		if request_file.endswith('.js'):
			return 'application/javascript'

	def load_and_return_file(self, request_file):
		if not os.path.exists(request_file):
			return (404, 'plain/text', 'not found')

		with open(request_file) as request_file_handle:
			return (200, self.get_mime_type(request_file), request_file_handle.read())
