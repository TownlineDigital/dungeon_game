import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE_FONT, FONT_BOLD
from colors import DARK_GREY, WHITE, GREEN, GREY
from ui_helpers import draw_text, draw_button
from game_state import GameState
from dungeon_recruiter.units.player import create_player_from_choice, CHARACTER_CHOICES
from game import Game  # Your main Game logic class
from ui_sanctuary import draw_sanctuary_screen
from dungeon_recruiter.dungeon.dungeon_map.dungeon_map import WALL, FLOOR, ENEMY, TREASURE
from dungeon_recruiter.assets.sprite_loader import load_dungeon_assets
from dungeon_recruiter.combat.combat_input_handler import CombatInputHandler
from dungeon_recruiter.combat.combat_ui import draw_battle_screen
from dungeon_recruiter.data.enemy_data import ENEMY_LIST
from dungeon_recruiter.dungeon.dungeon_map.dungeon_map import generate_dungeon_map
# from dungeon_recruiter.units.player import Player  --- Testing the UI with 4 characters on both side
# from dungeon_recruiter.units.enemy import Enemy
from input_handler import handle_input, handle_exploration_input, handle_combat_input
from dungeon_recruiter.combat.combat_menu import PlayerActionMenu
from dungeon_recruiter.combat.combat_manager import CombatManager
from engine_init import initialize_engine
from settings import TILE_SIZE, VIEWPORT_HEIGHT, VIEWPORT_WIDTH
from assets.sprite_loader import get_loaded_sprites
from core.game_initializer import initialize_game
# from dungeon_recruiter.assets.animation_loader import load_character_animations
from input_handler import handle_exploration_input


# --- Main Game Loop ---
def main():
    WIN = initialize_engine()
    game = initialize_game()

    # game.exploration_input_handler = ExplorationInputHandler(game)

    from dungeon_recruiter.assets.animation_loader import character_animations

    sprites = get_loaded_sprites(tile_size=TILE_SIZE)
    # game = Game()
    try:
        clock = pygame.time.Clock()

        while True:
            # Handle Movement

            now = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            clock.tick(FPS)
            WIN.fill(DARK_GREY)
            clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True

            # --- Game States ---
            if game.state == GameState.CHARACTER_SELECT:
                draw_text(WIN, "Choose Your Hero", TITLE_FONT, WHITE, SCREEN_WIDTH // 2, 60, center=True)

                card_width, card_height = 220, 220
                spacing = 40
                total_width = len(CHARACTER_CHOICES) * (card_width + spacing) - spacing
                start_x = (SCREEN_WIDTH - total_width) // 2

                # Initialize hover variables
                hovered_description = ""
                hovered_x, hovered_y = 0, 0

                for i, data in enumerate(CHARACTER_CHOICES):
                    x = start_x + i * (card_width + spacing)
                    y = SCREEN_HEIGHT // 2 - card_height // 2
                    card_rect = pygame.Rect(x, y, card_width, card_height)
                    pygame.draw.rect(WIN, GREY, card_rect)

                    # Draw name above card
                    draw_text(WIN, data["name"], FONT_BOLD, WHITE, card_rect.centerx, card_rect.top - 30, center=True)

                    # Handle card click
                    if draw_button(WIN, card_rect, "", GREY, GREEN):
                        game.player = create_player_from_choice(i)
                        print(f"[DEBUG] Created player: {game.player.name}")
                        print(f"[DEBUG] Abilities: {[a.name for a in game.player.abilities]}")
                        game.center_camera_on_player()
                        game.state = GameState.SANCTUARY

                    # Detect hover
                    if card_rect.collidepoint(pygame.mouse.get_pos()):
                        hovered_description = data.get("description", "")
                        hovered_x = card_rect.centerx
                    is_hovering = card_rect.collidepoint(pygame.mouse.get_pos())

                    if is_hovering:
                        hovered_description = data.get("description", "")
                        hovered_x = card_rect.centerx

                        name = data["name"]
                        if name in character_animations:
                            anim = character_animations[name]
                            anim.set_animation("idle")
                            frame = anim.get_static_frame()  # Or .get_current_frame() for animation
                            resized = pygame.transform.scale(frame, (120, 120))
                            frame_rect = resized.get_rect(center=(SCREEN_WIDTH // 2, 160))
                            WIN.blit(resized, frame_rect)



                    # Draw stats
                    draw_text(WIN, f"HP: {data['health']}", FONT_BOLD, WHITE, x + 10, y + 40)
                    draw_text(WIN, f"ATK: {data['attack']}", FONT_BOLD, WHITE, x + 10, y + 70)
                    draw_text(WIN, f"DEF: {data['defense']}", FONT_BOLD, WHITE, x + 10, y + 100)
                    draw_text(WIN, f"MP: {data['mana']}", FONT_BOLD, WHITE, x + 10, y + 130)
                    draw_text(WIN, f"SCL: {data['recruiting']}", FONT_BOLD, WHITE, x + 10, y + 160)
                    draw_text(WIN, f"SPD: {data['speed']}", FONT_BOLD, WHITE, x + 10, y + 190)

                # ✅ Draw description BELOW all cards
                if hovered_description:
                    draw_text(
                        WIN,
                        hovered_description,
                        FONT_BOLD,
                        WHITE,
                        SCREEN_WIDTH // 2,  # centered horizontally
                        SCREEN_HEIGHT // 2 + card_height // 2 + 80,  # under all cards
                        center=True
                    )


            elif game.state == GameState.SANCTUARY:
                idle_sprite = character_animations[game.player.name].get_current_frame()
                game.state = draw_sanctuary_screen(WIN, idle_sprite, GameState, FONT_BOLD, WHITE, GREY, GREEN)



            elif game.state == GameState.EXPLORATION:

                tile_size = 64
                player_x, player_y = game.player_map_pos
                camera_x = game.camera_x
                camera_y = game.camera_y
                handle_exploration_input(game, keys, now)


                # Draw Dungeon Tiles
                for y in range(VIEWPORT_HEIGHT):
                    for x in range(VIEWPORT_WIDTH):
                        map_x = x + camera_x
                        map_y = y + camera_y

                        if 0 <= map_x < len(game.dungeon_map[0]) and 0 <= map_y < len(game.dungeon_map):
                            tile = game.dungeon_map[map_y][map_x]
                            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)

                            sprite_key = None
                            if tile == WALL:
                                sprite_key = "WALL"
                            elif tile == FLOOR:
                                sprite_key = "FLOOR"
                            elif tile == ENEMY:
                                enemy = game.enemy_placement.get((map_x, map_y))
                                if enemy:
                                    sprite_key = f"ENEMY_{enemy.name.upper().replace(' ', '_')}"
                            elif tile == TREASURE:
                                sprite_key = "TREASURE"

                            if sprite_key in sprites:
                                WIN.blit(sprites[sprite_key], rect)
                            else:
                                pygame.draw.rect(WIN, (50, 50, 50), rect)

                # Draw Player

                player_screen_x = (player_x - camera_x) * tile_size
                player_screen_y = (player_y - camera_y) * tile_size
                player_rect = pygame.Rect(player_screen_x, player_screen_y, tile_size, tile_size)

                player_sprite_key = f"PLAYER_{game.player.name.upper()}"
                player_sprite = sprites.get(player_sprite_key)

                if player_sprite:
                    WIN.blit(player_sprite, (player_screen_x, player_screen_y))
                else:
                    pygame.draw.rect(WIN, (50, 200, 255), player_rect)


                # if game.state == GameState.COMBAT:
                #     if game.combat_input_handler:
                #         game.combat_input_handler.update(keys, now)
                #     else:
                #         print("[Warning] combat_input_handler not initialized yet.")
                # elif game.state == GameState.EXPLORATION:
                #     if game.exploration_input_handler:
                #         game.exploration_input_handler.update(keys, now)
                #     else:
                #         print("[Warning] exploration_input_handler not initialized yet.")

                if game.state == GameState.COMBAT:
                    if not getattr(game, "combat_initialized", False):
                        # Setup combat components only once when combat starts
                        game.active_party = [game.player]  # Later this might include more units
                        game.combat_manager = CombatManager(game.active_party, game.enemy_party)
                        game.combat_menu = PlayerActionMenu()
                        game.combat_input_handler = CombatInputHandler(game.combat_manager, game.combat_menu, game)
                        game.battle_intro_start = now
                        game.battle_intro_done = False
                        game.combat_initialized = True

                    if game.state == GameState.COMBAT and game.combat_input_handler:
                        game.combat_input_handler.update(keys, now)



                # handle_input(game, keys, now)

                # game.combat_input = CombatInputHandler(game.combat_manager, game.combat_menu)
                # game.combat_input_handler = CombatInputHandler(CombatManager, combat_menu)

                # Notification
                if game.notification:
                    draw_text(WIN, game.notification, FONT_BOLD, WHITE, SCREEN_WIDTH // 2, 40, center=True)
                    game.notification_timer -= 1
                    if game.notification_timer <= 0:
                        game.notification = ""


            elif game.state == GameState.COMBAT:
                # game.combat_initialized = False
                now = pygame.time.get_ticks()
                keys = pygame.key.get_pressed()

                # print("[Debug] Checking if combat is initializing...")



                # --- Initialize Combat Components Once ---
                # if not hasattr(game, "combat_initialized") or not game.combat_initialized:
                if not getattr(game, "combat_initialized", False):
                    # print("[Init] Setting up combat...")
                    game.active_party = [game.player]  # Later: use full party
                    # print(f"[Debug] Active party setup: {[unit.name for unit in game.active_party]}")
                    # print(f"[Debug] {game.player.name}'s abilities: {[a.name for a in game.player.abilities]}")

                    game.combat_manager = CombatManager(game.active_party, game.enemy_party)
                    game.combat_menu = PlayerActionMenu()
                    game.combat_input = CombatInputHandler(game.combat_manager, game.combat_menu)
                    game.battle_intro_start = now
                    game.battle_intro_done = False
                    game.combat_initialized = True
                    # print(f"[Debug] Combat initialized: {game.combat_initialized}")

                # --- Battle Intro Message ---
                if not game.battle_intro_done:
                    draw_battle_screen(WIN, game.active_party, game.enemy_party, message="A Wild Battle Begins!", combat_menu=None)
                    pygame.display.update()

                    # ⏳ Let the intro message show for 1500ms
                    if now - game.battle_intro_start >= 1500:
                        game.battle_intro_done = True
                        game.combat_menu.show()
                    else:
                        continue

                # --- Handle Player Turn ---
                current_unit = game.combat_manager.get_current_unit()
                if current_unit in game.enemy_party:
                    game.combat_manager.take_turn()
                else:
                    game.combat_input_handler.update(keys, now)

                # --- Render Combat UI ---
                draw_battle_screen(WIN, game.active_party, game.enemy_party, combat_menu=game.combat_menu)
                pygame.display.update()


                now = pygame.time.get_ticks()
                keys = pygame.key.get_pressed()

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


                if game.notification:
                    draw_text(WIN, game.notification, FONT_BOLD, WHITE, SCREEN_WIDTH // 2, 40, center=True)
                    game.notification_timer -= 1
                    if game.notification_timer <= 0:
                        game.notification = ""


            pygame.display.update()

    except Exception as e:
        import traceback
        traceback.print_exc()
        pygame.quit()
        raise e


if __name__ == "__main__":
    main()