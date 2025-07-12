import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_BOLD
from colors import WHITE, GREEN, RED, BLUE, BLACK
from ui_helpers import draw_text

def draw_health_bar(surface, x, y, current, max_value, width=120, height=12):
    pygame.draw.rect(surface, RED, (x, y, width, height))  # background
    if max_value > 0:
        ratio = current / max_value
        pygame.draw.rect(surface, GREEN, (x, y, int(width * ratio), height))  # foreground

def draw_mana_bar(surface, x, y, current, max_value, width=120, height=8):
    pygame.draw.rect(surface, BLUE, (x, y, width, height))  # background
    if max_value > 0:
        ratio = current / max_value
        pygame.draw.rect(surface, (0, 200, 255), (x, y, int(width * ratio), height))  # foreground

def draw_battle_screen(surface, player_party, enemy_party, message="", combat_menu=None):
    surface.fill((20, 20, 20))  # Dark background

    # ⛑️ Backward compatibility: if passed a single unit instead of a list
    if not isinstance(player_party, list):
        player_party = [player_party]
    if not isinstance(enemy_party, list):
        enemy_party = [enemy_party]

    # Layout constants
    unit_scale = 96
    spacing = 140
    bottom_y = SCREEN_HEIGHT - 200

    # --- Draw Player Party (left side) ---
    for i, unit in enumerate(player_party):
        sprite = unit.get_idle_sprite(scale=unit_scale)
        x_pos = 120 + i * spacing
        rect = sprite.get_rect(midbottom=(x_pos, bottom_y))
        surface.blit(sprite, rect)

        draw_text(surface, unit.name, FONT_BOLD, WHITE, rect.centerx, rect.top - 30, center=True)
        draw_health_bar(surface, rect.left, rect.top - 20, unit.current_health, unit.max_health)
        draw_mana_bar(surface, rect.left, rect.top - 5, unit.current_mana, unit.max_mana)

    # --- Draw Enemy Party (right side) ---
    for i, unit in enumerate(enemy_party):
        sprite = unit.get_idle_sprite(scale=unit_scale)
        x_pos = SCREEN_WIDTH - (120 + i * spacing)
        rect = sprite.get_rect(midbottom=(x_pos, bottom_y))
        surface.blit(sprite, rect)

        draw_text(surface, unit.name, FONT_BOLD, WHITE, rect.centerx, rect.top - 30, center=True)
        draw_health_bar(surface, rect.left, rect.top - 20, unit.current_health, unit.max_health)
        draw_mana_bar(surface, rect.left, rect.top - 5, unit.current_mana, unit.max_mana)

    # --- Message / Notification Box ---
    if message:
        pygame.draw.rect(surface, BLACK, (50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 40))
        draw_text(surface, message, FONT_BOLD, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, center=True)

     # --- 👇 Draw Combat Menu ---
    if combat_menu and combat_menu.visible:
        pygame.draw.rect(surface, (0, 0, 0), (40, 40, 180, len(combat_menu.actions) * 40 + 20))
        pygame.draw.rect(surface, (255, 255, 255), (40, 40, 180, len(combat_menu.actions) * 40 + 20), 2)
        draw_player_action_menu(
            surface,
            actions=combat_menu.actions,
            selected_index=combat_menu.selected_index,
            font=FONT_BOLD,
            x=50,
            y=50,
            # ability_submenu = combat_menu.abilities if getattr(combat_menu, "ability_menu_visible", False) else None,
            # ability_index = getattr(combat_menu, "selected_ability_index", 0)
        )

        # 🔹 Draw ability submenu if active
        if combat_menu.ability_menu_visible and combat_menu.abilities:
            pygame.draw.rect(surface, (0, 0, 0), (250, 40, 200, len(combat_menu.abilities) * 40 + 20))
            pygame.draw.rect(surface, (255, 255, 255), (250, 40, 200, len(combat_menu.abilities) * 40 + 20), 2)

            draw_ability_menu(
                surface,
                abilities=combat_menu.abilities,
                selected_index=combat_menu.selected_ability_index,
                font=FONT_BOLD,
                x=260,
                y=50
            )

    # 🔹 Draw ability submenu if visible
    # if hasattr(combat_menu, "ability_menu_visible") and combat_menu.ability_menu_visible:
    #     draw_ability_menu(
    #         surface,
    #         abilities=combat_menu.abilities,
    #         selected_index=combat_menu.selected_ability_index,
    #         font=FONT_BOLD,
    #         x=250,  # X offset to draw next to main menu
    #         y=50
    #     )

def draw_player_action_menu(surface, actions, selected_index, font, x, y, spacing=40):
    """
    Draws a vertical action menu for the player with highlight on the selected option.
    """
    for i, action in enumerate(actions):
        color = GREEN if i == selected_index else WHITE
        draw_text(surface, action, font, color, x, y + i * spacing)

def draw_ability_menu(surface, abilities, selected_index, font, x, y, spacing=40):
    pygame.draw.rect(surface, (50, 50, 50), (x - 10, y - 10, 200, spacing * len(abilities) + 20))
    """
    Draws a vertical submenu listing abilities.
    """
    for i, ability in enumerate(abilities):
        name = ability.name if hasattr(ability, 'name') else str(ability)
        cost = f" - {ability.mana_cost} MP" if hasattr(ability, 'mana_cost') else ""
        color = GREEN if i == selected_index else WHITE
        draw_text(surface, f"{name}{cost}", font, color, x, y + i * spacing)
