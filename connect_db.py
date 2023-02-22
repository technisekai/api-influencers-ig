import pymysql              #connect to db

# to connect MYSQL server
HOST_DB = 'localhost'
USER_DB = 'root'
PASS_DB = ''
DB = 'influencers_db'
# Connect to the database
connection = pymysql.connect(
    host=HOST_DB,
    user=USER_DB,
    password=PASS_DB,
    db=DB,
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()
