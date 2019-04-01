#!/usr/bin/python3

import threading
import time

class ConsoleBreaker(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True
		self.start()

	def run(self):
		print('[ConsoleBreaker] Breaker thread started')
		while(True):
			time.sleep(10000)

	def install_breaker(self):
		while(True):
			self.join(1)
