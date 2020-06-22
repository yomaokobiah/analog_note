import os

SECRET_KEY = 'qCJs2OkujX5Iz5VJSPbxHg'
#SQLALCHEMY_DATABASE_URI = 'mysql://analog:dt2016@localhost/analog_data'
SQLALCHEMY_DATABASE_URI = os.environ.get("CLEARDB_DATABASE_URL")
