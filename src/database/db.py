from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import db_user, db_password, db_host, db_name

#Base de datos MySQL
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}', echo=True)

#Definir la base de datos ORM
Base = declarative_base()

#Crear la sesion
Session = sessionmaker(bind=engine)


