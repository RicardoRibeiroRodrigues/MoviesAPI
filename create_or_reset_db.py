import os
from dotenv import load_dotenv
import MySQLdb


load_dotenv()

user = os.getenv("MD_DB_USERNAME")
password = os.getenv("MD_DB_PASSWORD")
host = os.getenv("MD_DB_SERVER")
database = "moviesProj"


connection = MySQLdb.connect(user=user, passwd=password, host=host)

# Create a cursor object to execute SQL statements
cursor = connection.cursor()

# Execute the SQL statement to create the schema
cursor.execute(f"DROP SCHEMA IF EXISTS `{database}`")
cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `{database}`")

# Commit the transaction
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
