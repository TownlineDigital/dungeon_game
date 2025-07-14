# from .base import Unit
from dungeon_recruiter.data.player_abilities import player_abilities
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
        self.abilities = []

    def get_idle_sprite(self, scale=96):
        return get_player_idle_sprite(self.name, scale=scale)

    def get_in_dungeon_sprite(self, scale=32):
        return get_in_dungeon_sprite(self.name, scale=scale, is_enemy=False)

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
    player = Player(
        data["name"],
        data["health"],
        data["mana"],
        data["attack"],
        data["defense"],
        data["recruiting"],
        data["speed"]
    )
    #assign class_specific abilities
    if data["name"] in player_abilities:
        player.abilities = player_abilities.get(data["name"], [])
    else:
        player.abilities = []
    return player