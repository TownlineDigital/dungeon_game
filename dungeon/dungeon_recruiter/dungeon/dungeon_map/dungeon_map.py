import random

from dungeon_recruiter.data.enemy_data import ENEMY_LIST

WALL = 1
FLOOR = 0
ENEMY = 2
TREASURE = 3

def generate_dungeon_map(width, height, enemy_pool, num_enemies=5, num_treasures=3):
    dungeon = [[WALL for _ in range(width)] for _ in range(height)]
    enemy_placement = {}  # New dict to track which enemy is at which tile

    for y in range(2, height - 2):
        for x in range(2, width - 2):
            dungeon[y][x] = FLOOR

    # Place enemies and store their instance
    for _ in range(num_enemies):
        while True:
            x, y = random.randint(2, width - 3), random.randint(2, height - 3)
            if dungeon[y][x] == FLOOR:
                selected_enemy = random.choice(enemy_pool)
                dungeon[y][x] = ENEMY
                enemy_placement[(x, y)] = selected_enemy
                break

    # Place treasures
    for _ in range(num_treasures):
        while True:
            x, y = random.randint(2, width - 3), random.randint(2, height - 3)
            if dungeon[y][x] == FLOOR:
                dungeon[y][x] = TREASURE
                break

    return dungeon, enemy_placement