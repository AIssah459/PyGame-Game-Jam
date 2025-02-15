import pygame
from pygame.mixer import music

IMG_PATH = 'Assets/Images/'
SOUND_PATH = 'Assets/Sounds/'
MUSIC_PATH = 'Assets/Music/'

def load_image(path):
    img = pygame.image.load(IMG_PATH + path).convert()

    return img

def load_image_no_convert(path):
    img = pygame.image.load(IMG_PATH + path)

    return img

def load_sound(path):
    return pygame.mixer.Sound(SOUND_PATH + path)

def load_music(path):
    music.load(MUSIC_PATH + path)
