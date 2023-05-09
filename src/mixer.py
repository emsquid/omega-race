import pygame


class Mixer:
    """
    -
    """

    def __init__(self, volume: float):
        self.volume = volume

    def music(self, file: str):
        pygame.mixer.music.load(f"assets/sounds/{file}")
        pygame.mixer.music.set_volume(self.volume) 
        pygame.mixer.music.play(-1)

    def play(self, file: str):
        sound = pygame.mixer.Sound(f"assets/sounds/{file}")
        sound.set_volume(self.volume)
        sound.play()
