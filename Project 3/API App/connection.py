# import pymysql

# conn_string_proxy = pymysql.connect(host='127.0.0.1', user= "root", password= "RootinTootinSQLBootin7869!", db= "Covid")

# conn_string_deploy = pymysql.connect(unix_socket= "/cloudsql/project-3-280623:us-central1:covid-fastapi", user= "root", password= "ehaarmanny", db= "Covid")

conn_string_proxy = "mysql+pymysql://root:RootinTootinSQLBootin7869!@127.0.0.1:3306/Covid"

conn_string_deploy = "mysql+pymysql://root:ehaarmanny@/Covid?unix_socket=/cloudsql/project-3-280623:us-central1:covid-fastapi"
