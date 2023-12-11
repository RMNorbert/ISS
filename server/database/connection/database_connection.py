from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from server.database.models.secret_model import Base
import os

db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")


def initialize_db(created_engine):
    db_name = "iss"
    with created_engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        connection.execute(text(f"USE {db_name}"))


connection_url = f'mysql+mysqlconnector://{db_username}:{db_password}@localhost:3306/'
engine = create_engine(connection_url, echo=True)
initialize_db(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
