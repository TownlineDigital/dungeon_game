import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60
TITLE_SIZE = 32
TILE_SIZE = 32

pygame.font.init()
FONT = pygame.font.SysFont("corbel", 22)
FONT_BOLD = pygame.font.SysFont("corbel", 26, bold=True)
TITLE_FONT = pygame.font.SysFont("georgia", 60, bold = True)
VIEWPORT_WIDTH = 16 # e.g. 25 tiles wide
VIEWPORT_HEIGHT = 12

WINDOW_TITLE = "Dungeon Delve: Loot & Recruit"