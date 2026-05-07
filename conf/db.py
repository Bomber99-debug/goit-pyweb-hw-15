from configparser import ConfigParser
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_cong = Path(__file__).parent.parent.joinpath("config.ini")
config = ConfigParser()
config.read(file_cong)

user = config.get('DEV_15', 'USER')
password = config.get('DEV_15', 'PASSWORD')
db = config.get('DEV_15', 'DB_NAME')
domian = config.get('DEV_15', 'DOMAIN')
port = config.get('DEV_15', 'PORT')

URI = f'postgresql://{user}:{password}@{domian}:{port}/{db}'

engine = create_engine(URI, echo=False, pool_size=5, max_overflow=0)
DBSession = sessionmaker(bind=engine)
session = DBSession()