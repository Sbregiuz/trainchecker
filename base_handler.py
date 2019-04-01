#!/usr/bin/python3

import re
import sys
import json

class BaseHandler():
	def __init__(self):
		pass

	def deserialize_request(self, request):
		pattern = re.compile("(\\w+.)\s(\\S.+)\\sHTTP\\/(\\d\\.\\d)")
		matches = pattern.match(request)
		if not matches:
			return False

		return matches.group(2)

	def handle_request(self, request):
		deserialized_request = self.deserialize_request(request)
		if deserialized_request == False:
			return False

		rtn_value = self.internal_handle_request(deserialized_request)
		if rtn_value == False:
			return False
		else:
			return rtn_value

	def internal_handle_request(self, deserialized_request):
		pass


