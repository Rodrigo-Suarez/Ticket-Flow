from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import db_user, db_password, db_host, db_name
from fastapi.exceptions import HTTPException

#Base de datos MySQL
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}', echo=True)

#Definir la base de datos ORM
Base = declarative_base()

#Crear la sesion
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
        print("Conexion exitosa a base de datos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    finally:
        if db:
            db.close()
            print("Conexion a base de datos finalizada")