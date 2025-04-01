


from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("sqlite:///Databases/ChatMSG.db", echo=True)

create_database(engine.url)
