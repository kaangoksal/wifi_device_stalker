from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# postgresql_username = ''
# postgresql_password = ""
# postgresql_host = ''
# database_name = ""

# engine = create_engine('postgresql://' + postgresql_username + ':' + postgresql_password + '@' + postgresql_host + '/' +
#                        database_name)

Base = declarative_base()