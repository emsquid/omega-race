import os
from time import time
from threading import Thread
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from src.base import Object, Text
from src.const import WIN_WIDTH, WIN_HEIGHT, CEN_X, RED


class Data:
    """
    The Database for scores
    """

    def __init__(self):
        load_dotenv()

        self.db = None
        self.scores = []
        self.last_fetch = 0
        self.last_connection = 0
        self.connected = False
        Thread(target=self.connect).start()

    def can_connect(self) -> bool:
        """
        Check if we should try to connect

        :return: bool, Whether it's been long enough or not
        """
        return not self.connected and time() - self.last_connection > 5

    def can_fetch(self) -> bool:
        """
        Check if the scores should be fetched

        :return: bool, Whether it's been long enough or not
        """
        return self.connected and time() - self.last_fetch > 5

    def connect(self):
        """
        Try to connect to the remote database
        """
        if not self.can_connect():
            return
        self.last_connection = time()
        try:
            uri = f"mongodb+srv://omegarace:{os.getenv('TOKEN')}@omegarace.1knm5ap.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(
                uri, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000
            )
            self.db = client["Scores"]
            self.connected = True
            self.fetch()
        except:
            self.connected = False

    def fetch(self):
        """
        Try to fetch scores from the remote database
        """
        if not self.can_fetch():
            return
        self.last_fetch = time()
        try:
            self.scores = [doc for doc in self.db["Single"].find()]
            self.scores.sort(key=lambda doc: doc["score"], reverse=True)
        except:
            self.connected = False

    def insert(self, doc: dict):
        """
        Try to insert a document in the remote database

        :param doc: dict, The document to insert
        """
        if not self.connected:
            return
        try:
            self.db["Single"].insert_one(doc)
        except:
            self.connected = False

    def add_score(self, name: str, score: int, level: int):
        """
        Add a score to the database locally (and try remotely)

        :param name: str, The name of the user who made the score
        :param score: int, The score made
        :param level: int, The level reached
        """
        if len(self.scores) < 10 or score > self.scores[9]["score"]:
            doc = {"name": name, "score": score, "level": level}
            self.scores.append(doc)
            self.scores.sort(key=lambda doc: doc["score"], reverse=True)

            Thread(target=self.insert, args=[doc]).start()

    def highscore(self) -> int:
        """
        Get the highscore from the database

        :return: int, The highscore
        """
        return self.scores[0]["score"] if len(self.scores) > 0 else 0

    def update(self):
        """
        Update the database connections
        """
        Thread(target=self.connect).start()
        Thread(target=self.fetch).start()


class Scores:
    """
    The scores of the game
    """

    def __init__(self):
        self.title = Text("Scores", CEN_X, WIN_HEIGHT / 5, 90)

        self.names = [
            Text(f"{i+1}. -----", 150 - i, 240 + i * 40, anchor="topleft")
            for i in range(10)
        ]
        self.scores = [
            Text("-----", 550, 240 + i * 40, anchor="topright") for i in range(10)
        ]
        self.levels = [
            Text("--", 800, 240 + i * 40, anchor="topright") for i in range(10)
        ]
        self.home = Text("HOME", WIN_WIDTH * 4 / 5, WIN_HEIGHT - 100, 40, RED)

    def update(self, scores: list[dict]):
        """
        Update the situation of all objects

        :param scores: list[dict], The current scores in the game
        """
        for i in range(10):
            if i < len(scores):
                self.names[i].update(content=f"{i+1}. {scores[i]['name']}")
                self.scores[i].update(content=f"{scores[i]['score']}")
                self.levels[i].update(content=f"{scores[i]['level']}")

    def get_objects(self) -> tuple[Object]:
        """
        Get every object handled by the scores

        :return: tuple[Object], All objects
        """
        return (self.title, *self.names, *self.scores, *self.levels, self.home)
