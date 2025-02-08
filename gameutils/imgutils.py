import pygame

IMG_PATH = 'Assets/Images/'

def load_image(path):
    img = pygame.image.load(IMG_PATH + path).convert()

    return img

def load_image_no_convert(path):
    img = pygame.image.load(IMG_PATH + path)

    return img