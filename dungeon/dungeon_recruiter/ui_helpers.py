import pygame
from settings import FONT, FONT_BOLD
from colors import WHITE, GREY, DARK_GREY

def draw_text(surface, text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect

def draw_button(surface, rect, text, base_color, hover_color, selected=False, disabled=False):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_pos)
    color = DARK_GREY if disabled else hover_color if is_hovered else base_color

    if selected and not disabled:
        pygame.draw.rect(surface, (255, 215, 0), rect.inflate(6, 6), 3, border_radius=10)

    pygame.draw.rect(surface, color, rect, border_radius=8)
    draw_text(surface, text, FONT_BOLD, WHITE if not disabled else GREY, rect.centerx, rect.centery, center=True)

    return is_hovered and not disabled and pygame.mouse.get_pressed()[0]

def draw_health_bar(surface, x, y, width, height, current, maximum, color):
    ratio = max(0, current / maximum) if maximum > 0 else 0
    pygame.draw.rect(surface, DARK_GREY, (x, y, width, height))
    pygame.draw.rect(surface, color, (x, y, width * ratio, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)