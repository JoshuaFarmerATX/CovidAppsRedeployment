import pymysql
from pymysql.cursors import DictCursorMixin, Cursor

#conn_string_proxy = pymysql.connect(host='127.0.0.1', user= "root", password= "ehaarmanny", db= "Covid")

conn_string_deploy = pymysql.connect(unix_socket= "/cloudsql/covid-api-274519:us-central1:covid-19", user= "root", password= "ehaarmanny", db= "Covid")
