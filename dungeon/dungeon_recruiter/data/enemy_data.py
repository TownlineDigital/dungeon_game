from dungeon_recruiter.units.enemy import Enemy
from dungeon_recruiter.data.enemy_abilities import enemy_abilities

# Example enemies — add more as needed
SLIME = Enemy(
    name="Slime",
    health=30,
    mana=0,
    attack=5,
    defense=2,
    speed=2,
    rarity="Common",
    description="A squishy blob that wiggles menacingly.",
    sprite_folder="assets/enemy_sprites/slime/idle",
    abilities=enemy_abilities["Slime"],
    recruit_chance=.25
)

GOBLIN = Enemy(
    name="Goblin",
    health=40,
    mana=10,
    attack=8,
    defense=3,
    speed=6,
    rarity="Uncommon",
    description="A nasty little trickster with a dagger.",
    sprite_folder="assets/enemy_sprites/goblin/idle",
    abilities=enemy_abilities["Goblin"],
    recruit_chance=.15
)

DARK_MAGE = Enemy(
    name="Dark Mage",
    health=35,
    mana=40,
    attack=12,
    defense=2,
    speed=4,
    rarity="Rare",
    description="A shadowy figure that manipulates dark magic.",
    sprite_folder="assets/enemy_sprites/dark_mage/idle",
    abilities=enemy_abilities["Dark Mage"],
    recruit_chance=.05
)


# Registry of all enemies for spawning or display
ENEMY_REGISTRY = {
    "Slime": SLIME,
    "Goblin": GOBLIN,
    "Dark Mage": DARK_MAGE,
}

# For random generation
ENEMY_LIST = list(ENEMY_REGISTRY.values())