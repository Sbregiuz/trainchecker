#!/usr/bin/python3

import threading
import re
import sys
import json
from base_handler import BaseHandler

class ApiHandler(BaseHandler):
	def __init__(self, db):
		BaseHandler.__init__(self)
		self.db = db
		self.routes = {
			'/api/ping': self.handle_ping,
			'/api/stations': self.handle_stations,
			'/api/stations/%': self.handle_station,
			'/api/test/%/test123/%/test': self.handle_test
		}

	def handle_restful_request(self, local_route, request_route, route_exec, params=[]):
		print(local_route)
		if len(local_route) == 0 and len(request_route) == 0:
			return route_exec(params)
		elif (len(local_route) == 0 and len(request_route) != 0) or (len(local_route) != 0 and len(request_route) == 0):
			return False

		if local_route[0] == '%':
			params.append(request_route[0])
		elif local_route[0] != request_route[0]:
			return False

		return self.handle_restful_request(local_route[1:], request_route[1:], route_exec, params)

	def internal_handle_request(self, deserialized_request):
		for route in self.routes:
			result = self.handle_restful_request(route.split('/'), deserialized_request.split('/'), self.routes[route])
			if result == False:
				continue
			return result
		return False

	def make_response(self, rtn, obj):
		return (rtn, 'application/json', json.dumps(obj))


	def handle_test(self, params):
		return self.make_response(200, params)

	def handle_ping(self, params):
		return self.make_response(200, { 'pong': True })

	def handle_stations(self, params):
		return self.make_response(200, self.db.list_stations())

	def handle_station(self, params):
		return self.make_response(200, self.db.get_station(params[0]))
