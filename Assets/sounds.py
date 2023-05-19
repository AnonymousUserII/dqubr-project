from os.path import join

import pygame

pygame.mixer.pre_init()
pygame.mixer.init()
CLICK: pygame.mixer.Sound = pygame.mixer.Sound(join("Assets", "Sounds", "click.wav"))
TAB_CLICK: pygame.mixer.Sound = pygame.mixer.Sound(join("Assets", "Sounds", "tab_click.wav"))
ROTATE: pygame.mixer.Sound = pygame.mixer.Sound(join("Assets", "Sounds", "turn.wav"))
