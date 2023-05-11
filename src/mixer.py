import pygame
from src.config import Config


class Mixer:
    """
    Mixer handles music and sound effects in the game

    :param config: Config, The game configuration
    """

    def __init__(self, config: Config):
        self.config = config
        self.music_volume = 1

    def update(self):
        """
        Update the state of the mixer
        """
        pygame.mixer.music.set_volume(self.music_volume * self.config.volume)

    def music(self, file: str, volume: float):
        """
        Play the game ambiant music

        :param file: str, The filename of the music
        :param volume: float, The volume to play the music at
        """
        self.music_volume = volume
        pygame.mixer.music.load(f"assets/sounds/{file}")
        pygame.mixer.music.set_volume(self.music_volume * self.config.volume)
        pygame.mixer.music.play(-1)

    def play(self, file: str, volume: float):
        """
        Play a sound effect

        :param file: str, The filename of the sound
        :param volume: float, The volume to play the sound at
        """
        sound = pygame.mixer.Sound(f"assets/sounds/{file}")
        sound.set_volume(volume * self.config.volume)
        sound.play()
