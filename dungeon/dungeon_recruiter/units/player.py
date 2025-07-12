# from .base import Unit
from dungeon_recruiter.units.base import Unit
from dungeon_recruiter.assets.sprite_loader import get_player_idle_sprite, get_in_dungeon_sprite
import os
import pygame
print("current working directory:", os.getcwd())

class Player(Unit):
    def __init__(self, name, health, mana, attack, defense, recruiting, speed):
        super().__init__(name, health, mana, attack, defense)
        self.recruiting = recruiting
        self.speed = speed

    def get_idle_sprite(self, scale=96):
        return get_player_idle_sprite(self.name, scale=scale)

    def get_in_dungeon_sprite(self, scale=32):
        return get_in_dungeon_sprite(self.name, scale=scale, is_enemy=False)

            # def get_idle_sprite(self, size=None):
    #     folder = os.path.join("sprites", self.name.lower(), "idle")
    #     frame_path = os.path.join(folder, f"{self.name.lower()}_idle_0.png")
    #
    #     if os.path.exists(frame_path):
    #         sprite = pygame.image.load(frame_path).convert_alpha()
    #         if size:
    #             sprite = pygame.transform.scale(sprite, size)
    #         return sprite
    #
    #     fallback = pygame.Surface((96, 96), pygame.SRCALPHA)
    #     pygame.draw.rect(fallback, (255, 0, 0, 128), fallback.get_rect(), 2)
    #     return fallback


    # def get_in_dungeon_sprite(self, size=None):
    #     folder = os.path.join("sprites", self.name.lower(), "in_dungeon")
    #     frame_path = os.path.join(folder, f"{self.name.lower()}_in_dungeon.png")
    #
    #     if os.path.exists(frame_path):
    #         sprite = pygame.image.load(frame_path).convert_alpha()
    #         if size:
    #             sprite = pygame.transform.scale(sprite, size)
    #         return sprite
    #
    #     fallback = pygame.Surface((32, 32), pygame.SRCALPHA)
    #     pygame.draw.rect(fallback, (0, 255, 0, 128), fallback.get_rect(), 2)
    #     return fallback

# Predefined characters to choose from
CHARACTER_CHOICES = [
    {
        "name": "Knight",
        "health": 120,
        "mana": 20,
        "attack": 10,
        "defense": 10,
        "recruiting": 5,
        "speed": 5,
        "description": "A stalwart defender who protects the weak. Balanced stats make the Knight a reliable frontliner."
    },
    {
        "name": "Mage",
        "health": 80,
        "mana": 60,
        "attack": 18,
        "defense": 3,
        "recruiting": 3,
        "speed" : 3,
        "description": "A glass cannon with devastating spells. Low health, but unmatched magical power.A tad unsocial"
    },
    {
        "name": "Rogue",
        "health": 100,
        "mana": 30,
        "attack": 15,
        "defense": 5,
        "recruiting": 2,
        "speed": 10,
        "description": "Quick and cunning, the Rogue strikes fast and vanishes. Has a hard time being trusted"
    },
    {
        "name": "Cleric",
        "health": 90,
        "mana": 50,
        "attack": 8,
        "defense": 7,
        "recruiting": 6,
        "speed": 4,
        "description": "A holy healer who keeps the team going. Balanced in combat, strong in support and recruiting."
    },
    {
        "name": "Barbarian",
        "health": 140,
        "mana": 10,
        "attack": 20,
        "defense": 2,
        "recruiting": 1,
        "speed":8,
        "description": "Pure brute force. The Barbarian smashes enemies with ease but struggles to recruit allies."
    }
]

def create_player_from_choice(index):
    data = CHARACTER_CHOICES[index]
    return Player(
        data["name"],
        data["health"],
        data["mana"],
        data["attack"],
        data["defense"],
        data["recruiting"],
        data["speed"]
    )