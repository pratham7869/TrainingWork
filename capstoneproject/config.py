# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "inventory_management"
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# In this file, the code defines configuration variables for connecting to a MySQL database.
# DB_HOST = "localhost": This variable specifies the hostname or IP address of the MySQL server.
# DB_USER = "root": This variable specifies the username used to authenticate with the MySQL server.
# DB_PASSWORD = "root": This variable specifies the password used to authenticate with the MySQL server.
# DB_NAME = "inventory_management": This variable specifies the name of the MySQL db that application will connect to.
# By defining these configuration variables in a config.py file,
# you can easily manage database connection and avoid hardcoded them directly into your code.
