from dungeon_recruiter.units.enemy import Enemy
from dungeon_recruiter.data.enemy_data import ENEMY_TEMPLATES
import random
from dungeon_recruiter.data.enemy_data import ENEMY_LIST

def create_enemy_by_name(name):
    template = ENEMY_TEMPLATES.get(name)
    if not template:
        raise ValueError(f"Enemy '{name}' not found in ENEMY_TEMPLATES.")

    return Enemy(
        name=template["name"],
        health=template["health"],
        mana=template["mana"],
        attack=template["attack"],
        defense=template["defense"],
        rarity=template["rarity"]
    )

def get_all_enemy_names():
    return list(ENEMY_TEMPLATES.keys())



def create_random_enemy():
    enemy_name = random.choice(ENEMY_LIST)
    return create_enemy_by_name(enemy_name)

enemy = create_random_enemy()
print(enemy)