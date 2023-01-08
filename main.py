from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import logging
import json

formatter = (
    "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d %(funcName)s] %(message)s"
)
logging.basicConfig(level=logging.DEBUG, format=formatter)
logging.disable(logging.DEBUG)

# SQLAlchemyのCRUD操作
# https://qiita.com/curry__30/items/432a21426c02a68e77e8#read

load_dotenv(".env")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
ALLOWABLE_ERROR = int(os.getenv("ALLOWABLE_ERROR"))

app = FastAPI()


origins = [
    "null",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)


# テーブルを作成する
Base = declarative_base()

Base.metadata.create_all(engine)

# セッションの作成
session = sessionmaker(engine)
db_session = scoped_session(session)


class PlayerOrm(Base):
    __tablename__ = "player"
    id = Column(String(64), primary_key=True)
    name = Column(String(64), nullable=False)
    level = Column(Integer, nullable=False)
    sex = Column(Integer, nullable=True)
    on_break = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "sex": self.sex,
            "on_break": self.on_break,
        }

# class PairOrm(Base):
#     __tablename__ = "pair"
#     id :str = Column(String(64), primary_key=True, nullable=True)
#     player1_id :str = Column(String(64), nullable=False)
#     player2_id :str = Column(String(64), nullable=False)
#     created_at :str = Column(TIMESTAMP, nullable=True)
#     updated_at :str = Column(TIMESTAMP, nullable=True)

class Pair(BaseModel):
    player1_id :str
    player2_id :str

class Match(BaseModel):
    pair1_id :str
    pair2_id :str

# フロントエンドから受け取るリクエストボディ用のクラス
# class Match():
#     __tablename__ = "match"
#     id = Column(String(64), primary_key=True)
#     name = Column(String(64), nullable=False)
#     level = Column(Integer, nullable=False)
#     sex = Column(Integer, nullable=True)
#     on_break = Column(Integer, nullable=True)
#     created_at = Column(TIMESTAMP, nullable=True)
#     updated_at = Column(TIMESTAMP, nullable=True)

# ロギングデコレータ
def mylogging(func):
    def wrapper(*args, **kwargs):
        logging.debug(f"{func.__name__} start")
        res = func(*args, **kwargs)
        logging.debug(f"{func.__name__} end")
        return res

    return wrapper


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    ###########################################################################
    # 前提となる考え方
    # ・ひとまずすべての組み合わせを列挙してからNGを除外していく
    #   ・例えば自ペアと相手ペアに同じ人がいても気にしない（影分身問題）
    ###########################################################################
    # TODO: その日の参加回数、休憩フラグをDBから取得する
    # レコード順に依存しないようランダムに取得する
    # 高々30レコード程度のため RAND() によるオーバーヘッドは無視する
    # sql = "SELECT id, name, level, sex, on_break FROM player ORDER BY RAND()"
    # players = db_session.execute(sql).all()
    players = db_session.query(PlayerOrm).all()
    # 与えられたメンバーリストから(無条件に)考えられるすべてのペアを作成する
    pairs = []
    player_count = len(players)
    for i in range(player_count):
        for j in range(i + 1, player_count):
            pairs.append(
                {
                    "player1": players[i].to_dict(),
                    "player2": players[j].to_dict(),
                    "pair_level": players[i].level + players[j].level,
                }
            )
    logging.debug(json.dumps(pairs, ensure_ascii=False))

    # すべてのペアからレベルが等しいペアの組み合わせリストを作成する
    matchs = []
    pair_count = len(pairs)
    for i in range(pair_count):
        for j in range(i + 1, pair_count):
            if is_level_equal(
                pairs[i]["pair_level"], pairs[j]["pair_level"], ALLOWABLE_ERROR
            ):
                matchs.append({"pair1": pairs[i], "pair2": pairs[j]})

    # TODO: 休憩する人がいる組み合わせを除外する
    # TODO: すでに対戦した組み合わせを除外する（まったく同じペア、メンバーのとき）
    #   TODO: 対戦リストを作成する

    # 対戦する二つのペアに同じ人がいる場合にその組み合わせを除外する
    # ※リスト内包表記を使って新しいリストを作成し、除外を実現する
    good_matchs = [
        m for m in matchs if not (is_player_duplicated(m["pair1"], m["pair2"]))
    ]
    logging.debug(json.dumps(good_matchs, ensure_ascii=False))

    # 抽出した組み合わせのメンバーのリストを作成する
    def get_players(match):
        players = []
        players.append(match["pair1"]["player1"]["name"])
        players.append(match["pair1"]["player2"]["name"])
        players.append(match["pair2"]["player1"]["name"])
        players.append(match["pair2"]["player2"]["name"])
        return players

    # TODO: 組み合わせに入っているプレイヤー全員の合計参加回数が少ない順にリストを並べ替える

    players = []
    fixed_matchs = []
    COURT_COUNT = 4  # TODO: その日のコート数に合わせて設定する
    court_occupied = 0  # すでに埋まったコートの数
    for i in range(len(good_matchs) - 1):
        match = good_matchs[i]
        new_players = get_players(match)
        # すでにコートに入ることが決まっているプレイヤーが次の組み合わせにも存在したらスキップ
        if set(players) & set(new_players):
            continue
        else:
            fixed_matchs.append(match)
            players.extend(new_players)
            court_occupied += 1
        # コート数分だけ組み合わせが決まれば終了
        if COURT_COUNT == court_occupied:
            break

    logging.debug(fixed_matchs)

    return {"matchs": fixed_matchs}

    # TODO: レベル差が小さい組み合わせを優先する
    # TODO: ペアとのレベル差が小さい組み合わせを優先する(1+7vs4+4より3+5vs4+4)
    # TODO: 試合回数の少ないプレイヤーを優先する
    # TODO: 休憩中のプレイヤーは選ばない
    # TODO: NGペアを作成しない（AさんとBさんは一緒にしてはいけない）


@app.post("/pairs", status_code=status.HTTP_201_CREATED)
async def pairs(pair: Pair):
    logging.info(pair)
    return "pair_id"

@app.post("/matchs", status_code=status.HTTP_201_CREATED)
async def pairs(match: Match):
    logging.info(match)
    return "match_id"

# レベル差が許容誤差の範囲内かを判定する
@mylogging
def is_level_equal(pair1_level, pair2_level, allowable_error=0):
    logging.debug(json.dumps([pair1_level, pair2_level, allowable_error]))
    return abs(pair1_level - pair2_level) <= allowable_error


# 二つのペアに重複するプレイヤーが存在するかを判定する（同一プレイヤーが２つのペアには所属出来ない）
@mylogging
def is_player_duplicated(pair1, pair2):
    logging.debug(json.dumps([pair1, pair2]))
    return (
        pair1["player1"]["name"] == pair2["player1"]["name"]
        or pair1["player1"]["name"] == pair2["player2"]["name"]
        or pair1["player2"]["name"] == pair2["player1"]["name"]
        or pair1["player2"]["name"] == pair2["player2"]["name"]
    )
