import pygame
from pygame import Rect

def draw_button(surface, rect, text, color, hover_color, font, text_color):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    pygame.draw.rect(surface, hover_color if is_hovered else color, rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
    return is_hovered and pygame.mouse.get_pressed()[0]

def draw_sanctuary_screen(WIN, player_sprite, GameState, FONT_BOLD, WHITE, GREY, GREEN):
    # Load sanctuary background
    background = pygame.image.load("assets/menus/sanctuary/sanctuary_bg.png").convert()
    background = pygame.transform.scale(background, (WIN.get_width(), WIN.get_height()))
    WIN.blit(background, (0, 0))

    # Draw player's idle sprite
    if player_sprite:
        scaled_sprite = pygame.transform.scale(player_sprite, (120, 120))
        WIN.blit(scaled_sprite, (100, WIN.get_height() // 2 - 60))

    # Button layout
    button_width, button_height = 220, 50
    spacing = 20
    start_y = WIN.get_height() // 2 - 100
    start_x = WIN.get_width() - button_width - 100

    buttons = [
        ("Enter the Dungeon", GameState.EXPLORATION),
        ("Manage Recruits", GameState.RECRUITS),
        ("Manage Inventory", GameState.INVENTORY),
    ]

    for i, (label, state) in enumerate(buttons):
        rect = Rect(start_x, start_y + i * (button_height + spacing), button_width, button_height)
        if draw_button(WIN, rect, label, GREY, GREEN, FONT_BOLD, WHITE):
            return state  # Change game state

    return GameState.SANCTUARY  # Stay in sanctuary by default