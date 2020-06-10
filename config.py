import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
dbUSER = os.environ.get('MD') 
dbPASS = os.environ.get('Mp')
# Enable debug mode.
DEBUG = True

print(dbUSER)
print(dbPASS)
# Connect to the database 
#postgres

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@localhost:5432/fyyurapp'.format(dbUSER,dbPASS)
SQLALCHEMY_TRACK_MODIFICATIONS = False