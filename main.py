import asyncio

# import aio.gthread
from src.game import Game

if __name__ == "__main__":
    asyncio.run(Game().run())
