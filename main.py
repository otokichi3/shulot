from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from dotenv import load_dotenv
import os

# SQLAlchemyのCRUD操作
# https://qiita.com/curry__30/items/432a21426c02a68e77e8#read

load_dotenv(".env")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = "localhost"

app = FastAPI()

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)


# テーブルを作成する
Base = declarative_base()

Base.metadata.create_all(engine)

# セッションの作成
session = sessionmaker(engine)
db_session = scoped_session(session)


class Player(Base):
    __tablename__ = "player"
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    level = Column(Integer, nullable=False)
    sex = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


@app.get("/")
async def root():
    players = db_session.query(Player).all()
    for row in players:
        print(row.id)
        print(row.level)
    return players
    # return {"message": "Hello World"}
