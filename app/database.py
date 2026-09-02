import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommot=False, autoflush=False, bind=engine)

Base = declarative_base()

if __name__ == "__main__":
    connection = engine.connect()
    print("Успешно подключились!")
    connection.close()