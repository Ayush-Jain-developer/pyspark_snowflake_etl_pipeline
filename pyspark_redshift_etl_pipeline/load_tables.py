from sqlalchemy import create_engine
import os
from models import metadata
from snowflake.sqlalchemy import URL

def snowflake_engine(**kwargs):
    try:
        return create_engine(URL(
            user = kwargs['user'],
            password = kwargs['password'],
            account = kwargs['account'],
            database = kwargs['database'],
            warehouse = kwargs['warehouse'],
            schema = kwargs['schema']
        ))
    except Exception as e:
        print(f"Error while creating engine: {e}" )
        return None

engine = snowflake_engine(user=os.getenv("SNOWFLAKE_USERNAME"), 
                          password= os.getenv("SNOWFLAKE_PASSWORD"), 
                          account=os.getenv("SNOWFLAKE_ACCOUNT"),
                          warehouse= os.getenv("SNOWFLAKE_WAREHOUSE"),
                          database= os.getenv("SNOWFLAKE_DATABASE"),
                          schema = os.getenv("SNOWFLAKE_SCHEMA"))

def load_tables():
    if engine:
        print("Successfully connected to snowflake database")
        metadata.create_all(engine)
    else:
        print("Failed to connect to snowflake databse")






