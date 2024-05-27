import os
import sys
from time import time
from threading import Thread


class Data:
    """
    The Database for scores
    """

    def __init__(self):
        self.db = None
        self.scores = []
        self.last_fetch = 0
        self.last_connection = 0
        self.connected = False
        Thread(target=self.connect).start()

    @property
    def highscore(self) -> int:
        """
        Get the highscore from the database

        :return: int, The highscore
        """
        return self.scores[0]["score"] if len(self.scores) > 0 else 0

    def can_connect(self) -> bool:
        """
        Check if we should try to connect

        :return: bool, Whether it's been long enough or not
        """
        return not self.connected and time() - self.last_connection > 5 and sys.platform != "emscripten"

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
        try:
            import certifi
            from dotenv import load_dotenv
            from pymongo.server_api import ServerApi
            from pymongo.mongo_client import MongoClient

            load_dotenv()

            uri = f"mongodb+srv://omegarace:{os.getenv('TOKEN')}@omegarace.1knm5ap.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(
                uri,
                server_api=ServerApi("1"),
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000,
            )
            self.db = client["Scores"]
            self.connected = True
            self.fetch()
        except Exception:
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
        except Exception:
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
        except Exception:
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

    def update(self):
        """
        Update the database connections
        """
        Thread(target=self.connect).start()
        Thread(target=self.fetch).start()
