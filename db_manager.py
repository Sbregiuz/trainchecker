#!/usr/bin/python3

import os
import sqlite3
import sys

class DbManager():
	def __init__(self, database_path, db_schema_path, queries_folder):
		self.database_path = database_path
		self.db_schema_path = db_schema_path

		if not queries_folder.endswith('/'):
			queries_folder = queries_folders + '/'
		self.queries_folder = queries_folder

		self.init_db()

	def create_db(self):
		print('[DbManager] Creating a new database...')
		if not os.path.exists(self.db_schema_path):
			print('[DbManager] Failed to load %s path for initialize the database!')
			sys.exit(0)

		schema_text = ''
		print('[DbManager] Reading DB initialization script...')
		with open(self.db_schema_path) as db_schema_file:
			schema_text = db_schema_file.read()
		print('[DbManager] Executing DB initialization script...')
		self.database_connection.executescript(schema_text)

		print('[DbManager] Database creation finished!')

	def init_db(self):
		new_db = not os.path.exists(self.database_path)
		self.database_connection = sqlite3.connect(self.database_path, check_same_thread=False)
		if new_db:
			print('[DbManager] Initializing a new database...')
			self.create_db()

		print('[DbManager] Database correctly initialized!')

	def exec_query(self, query_name, params=[]):
		print(params)
		query_file = '%s%s.sql' % (self.queries_folder, query_name)
		if not os.path.exists(query_file):
			print('[DbManager] Query %s does not exists!' % (query_name))
			return False

		with sqlite3.connect(self.database_path) as db_connection:
			cursor = self.database_connection.cursor()

			with open(query_file) as query_file:
				query_text = query_file.read()
				for i in range(len(params)):
					params[i] = params[i].replace('\'', ' ')
					query_text = query_text.replace('@%d' % (i), params[i])

				cursor.execute(query_text)
				results = []
				field_names = list(map(lambda x: x[0], cursor.description))
				row_index = 0
				for row in cursor.fetchall():
					col_index = 0
					out_dict = dict()
					for column in row:
						out_dict[field_names[col_index]] = column
						col_index += 1
					results.append(out_dict)
					row_index += 1

				return results

	# Queries
	def list_stations(self):
		return self.exec_query('select_stations')

	def get_station(self, station_id):
		return self.exec_query('get_station', [station_id])

	def list_trains(self):
		return []

	def get_train(self, train_id):
		return False

