import pygame
from game_state import GameState

# === Main Input Router ===
def handle_input(game, keys, now):
    if game.state == GameState.EXPLORATION:
        handle_exploration_input(game, keys, now)
    elif game.state == GameState.COMBAT:
        handle_combat_input(game, keys, now)
    elif game.state == GameState.INVENTORY:
        handle_inventory_input(game, keys, now)
    elif game.state == GameState.SANCTUARY:
        handle_sanctuary_input(game, keys, now)

# === EXPLORATION ===
def handle_exploration_input(game, keys, now):
    if now - game.move_timer > game.get_move_cooldown():
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_s]:
            dy = 1
        elif keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_d]:
            dx = 1

        if dx != 0 or dy != 0:
            game.move_player(dx, dy)
            game.move_timer = now

# === COMBAT ===
def handle_combat_input(game, keys, now):
    combat_input = getattr(game, "combat_input", None)
    if combat_input:
        combat_input.update(keys, now)

# === INVENTORY ===
def handle_inventory_input(game, keys, now):
    # Placeholder for future inventory logic
    pass

# === SANCTUARY ===
def handle_sanctuary_input(game, keys, now):
    # Placeholder for sanctuary logic
    pass