#!/usr/bin/python3

from http_server_socket import HttpServerSocket
from api_handler import ApiHandler
from web_handler import WebHandler
from db_manager import DbManager
from console_breaker import ConsoleBreaker

breaker = ConsoleBreaker()

web_server = HttpServerSocket('127.0.0.1', 80)
web_server.bind_http_handler(ApiHandler(DbManager('./db/api.db', './db/api_db.sql', './db/queries/')))
web_server.bind_http_handler(WebHandler('./web'))

breaker.install_breaker()
