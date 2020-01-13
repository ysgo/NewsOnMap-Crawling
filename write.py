import pymysql

# Open database connection
db = pymysql.connect(host='localhost', port=3306, user='user', passwd='pass', db='dbname', charset='utf8', autocommit=True)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL Query using execute() method
cursor.execute('SELECT VERSION()')

# Fetch a single row using fetchone() method
data = cursor.fetchone()
print(data)

# disconnect from server
db.close()