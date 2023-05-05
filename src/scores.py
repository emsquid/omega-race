import os
import pygame
from threading import Thread
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from src.base import Object, Text
from src.settings import Settings
from src.const import RED


class Scores:
    """
    The scores of the game
    """

    def __init__(self):
        load_dotenv()
        self.array = []
        self.connected = False
        Thread(target=self.connect).start()

        self.title = Text("Scores", 500, 150, size=90)
        self.names = [
            Text(
                f"{i+1}. {self.array[i]['name'] if i<len(self.array) else '-----'}",
                150 - i,
                240 + i * 40,
                anchor="topleft",
            )
            for i in range(10)
        ]
        self.scores = [
            Text(
                f"{self.array[i]['score'] if i<len(self.array) else '-----'}",
                550,
                240 + i * 40,
                anchor="topright",
            )
            for i in range(10)
        ]
        self.levels = [
            Text(
                f"{self.array[i]['level'] if i<len(self.array) else '--'}",
                800,
                240 + i * 40,
                anchor="topright",
            )
            for i in range(10)
        ]

        self.home = Text("HOME", 800, 700, RED, 40)

    def get_objects(self) -> tuple[Object]:
        """
        Get every object handled by the scores

        :return: tuple[Object], All objects
        """
        for i in range(10):
            if i < len(self.array):
                self.names[i].update(content=f"{i+1}. {self.array[i]['name']}")
                self.scores[i].update(content=f"{self.array[i]['score']}")
                self.levels[i].update(content=f"{self.array[i]['level']}")

        return (self.title, *self.names, *self.scores, *self.levels, self.home)

    def handle_keys(self, keys: pygame.key.ScancodeWrapper, settings: Settings):
        """
        Handle user inputs in the settings

        :param keys: pygame.key.ScancodeWrapper, The pressed keys
        :param settings: Settings, The current keys settings
        """
        pass

    def connect(self):
        if self.connected:
            return
        try:
            uri = f"mongodb+srv://omegarace:{os.getenv('TOKEN')}@omegarace.1knm5ap.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(uri, server_api=ServerApi("1"))
            self.db = client["Scores"]
            self.connected = True
            self.fetch()
        except Exception as e:
            self.db = None
            self.connected = False
            print(e)

    def fetch(self):
        if self.connected:
            self.array = [doc for doc in self.db["Single"].find()]
            self.array.sort(key=lambda doc: doc["score"], reverse=True)

    def insert(self, doc: dict):
        if self.connected:
            try:
                self.db["Single"].insert_one(doc)
            except Exception as e:
                self.connected = False
                print(e)

    def add_score(self, name: str, score: int, level: int):
        if len(self.array) < 10 or score > self.array[9]["score"]:
            doc = {"name": name, "score": score, "level": level}
            self.array.append(doc)
            self.array.sort(key=lambda doc: doc["score"], reverse=True)

            Thread(target=self.insert, args=(doc)).start()

    def highscore(self) -> int:
        return self.array[0]["score"] if len(self.array) > 0 else 0
