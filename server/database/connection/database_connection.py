from sqlalchemy import create_engine, text, pool
from sqlalchemy.orm import sessionmaker
from server.database.models.secret_model import Base
import os

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


def initialize_db(created_engine):
    try:
        db_name = "iss"
        with created_engine.connect() as connection:
            connection.execute(
                text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            connection.execute(text(f"USE {db_name}"))
    except Exception as e:
        print(f"Unexpected error: {e}")


connection_url = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@localhost:3306/'
engine = create_engine(connection_url, poolclass=pool.QueuePool, echo=True)
initialize_db(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
