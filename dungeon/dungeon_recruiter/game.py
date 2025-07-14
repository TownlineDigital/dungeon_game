import pygame

from dungeon_recruiter.units.enemy import Enemy
from game_state import GameState
from items.gear import Gear
from dungeon_recruiter.dungeon.dungeon_map.dungeon_map import generate_dungeon_map
from dungeon_recruiter.data.enemy_data import ENEMY_LIST
from settings import VIEWPORT_WIDTH, VIEWPORT_HEIGHT


class Game:
    def __init__(self):
        self.state = GameState.CHARACTER_SELECT
        self.clock = pygame.time.Clock()
        self.player = None  # Set when chosen

        #Movement logic
        self.move_timer = 0
        self.move_cooldown = 150

        # Sanctuary Setup
        self.sanctuary_roster = [
            Enemy("Goblin Grunt", 40, 10, 8, 2, 6, "Common")
        ]

        # Inventory and gear
        self.inventory = {
            "Healing Potion": 2,
            "Mana Potion": 1,
            "EXP Booster": 0
        }
        self.gear_stash = [
            Gear("Old Helmet", "Armor", {"defense": 2})
        ]

        # Dungeon (later)
        self.dungeon_level = 1
        self.dungeon_map, self.enemy_placement = generate_dungeon_map(60, 40, ENEMY_LIST, num_enemies=15, num_treasures=10)
        self.player_map_pos = [30, 20]

        # Combat (later)
        self.active_party = []
        self.enemy_party = []
        self.dungeon_party = []
        # self.battle_intro_done = False

        # UI
        self.notification = ""
        self.notification_timer = 0

    def set_notification(self, message):
        self.notification = message
        self.notification_timer = 180  # 3 seconds at 60 FPS

    def get_move_cooldown(self):
        base = 120  # base cooldown in milliseconds
        if self.player and hasattr(self.player, "speed"):
            return max(30, base - self.player.speed * 15)  # speed 5 = 45ms
        return base  # fallback if player not set yet

    def move_player(self, dx, dy):
        new_x = self.player_map_pos[0] + dx
        new_y = self.player_map_pos[1] + dy

        if 0 <= new_x < len(self.dungeon_map[0]) and 0 <= new_y < len(self.dungeon_map):
            destination = self.dungeon_map[new_y][new_x]

            if destination == 0:  # FLOOR
                self.player_map_pos = [new_x, new_y]
                self.center_camera_on_player()
            elif destination == 2:  # ENEMY
                self.state = GameState.COMBAT
                self.combat_initialized = False
                # Get the enemy at this tile
                enemy = self.enemy_placement.get((new_x, new_y))
                if enemy:
                    print(f"Enemy encounter triggered with: {enemy.name}")
                    self.enemy_party = [enemy]  # optional: prep combat system

                    self.dungeon_map[new_y][new_x] = 0  # Set back to FLOOR
                    self.enemy_placement.pop((new_x, new_y), None)

                    self.player_map_pos = [new_x, new_y]  # ✅ actually move the player
                    self.center_camera_on_player()  # ✅ recenter camera
                    self.state = GameState.COMBAT  # ✅ switch to combat mode
                    self.combat_initialized = False
                else:
                    print("Enemy encounter triggered, but no enemy found in placement!")
            elif destination == 3:  # TREASURE
                self.inventory["EXP Booster"] += 1
                self.dungeon_map[new_y][new_x] = 0  # Convert to FLOOR after collecting
                self.set_notification("You found a treasure!")
                self.player_map_pos = [new_x, new_y]

    def center_camera_on_player(self):
        self.camera_x = max(
            0,
            min(self.player_map_pos[0] - VIEWPORT_WIDTH // 2, len(self.dungeon_map[0]) - VIEWPORT_WIDTH)
        )
        self.camera_y = max(
            0,
            min(self.player_map_pos[1] - VIEWPORT_HEIGHT // 2, len(self.dungeon_map) - VIEWPORT_HEIGHT)
        )