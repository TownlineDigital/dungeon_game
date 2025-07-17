import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

def initialize_engine():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dungeon Recruiter: Loot & Legends")
    return screen