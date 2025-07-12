from .base import Unit
from dungeon_recruiter.items.skill_tree import SkillTree
from dungeon_recruiter.assets.sprite_loader import get_enemy_idle_sprite, get_in_dungeon_sprite
from dungeon_recruiter.combat.ability import Ability

import pygame
import os

class Enemy(Unit):
    def __init__(
        self,
        name,
        health,
        mana,
        attack,
        defense,
        speed,
        rarity,
        description="",
        sprite_folder="",
        abilities=None,
        recruit_chance=.25
    ):
        super().__init__(name, health, mana, attack, defense, speed)
        self.rarity = rarity
        self.exp = 0
        self.exp_to_next_level = 100
        self.skill_points = 0
        self.skill_tree = SkillTree(rarity)

        # NEW FIELDS (optional)
        self.description = description
        self.sprite_folder = sprite_folder
        self.abilities = abilities or []
        self.recruitable = True
        self.recruit_chance = 0.25  # Default recruit chance
        self.recruitable = True  # can this enemy type ever be recruited
        self.is_recruitable = False  # is it recruitable *right now*

    def gain_exp(self, amount, game):
        self.exp += amount
        leveled_up = False

        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up(game)
            leveled_up = True

        return leveled_up

    # def get_idle_sprite(self):
    #     path = os.path.join("assets", "sprites", "enemies", self.sprite_folder, "idle_0.png")
    #     return pygame.image.load(path).convert_alpha()
    def get_idle_sprite(self, scale=96):
        return get_enemy_idle_sprite(self.name, scale=scale)

    def get_in_dungeon_sprite(self, scale=32):
        return get_in_dungeon_sprite(self.name, scale=scale, is_enemy=True)

    def level_up(self, game):
        self.level += 1
        self.skill_points += 1
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)

        self.base_max_health += 10
        self.base_attack += 2
        self.base_defense += 1

        self.update_stats()
        self.current_health = self.max_health
        self.current_mana = self.max_mana

        game.set_notification(f"{self.name} grew to Level {self.level}!")

    def check_recruitable(self, player_recruit_skill):
        """
        Calculates recruit chance based on current HP %, base recruit chance,
        and player recruiting stat. Returns (bool, actual chance %)
        """
        hp_percent = self.current_health / self.max_health
        adjusted_chance = self.recruit_chance * (1 - hp_percent) + (player_recruit_skill * 0.02)

        rolled = random.random()
        if rolled <= adjusted_chance:
            self.is_recruitable = True
            return True, adjusted_chance
        return False, adjusted_chance

    def can_be_recruited(self):
        """
        Returns True if this enemy is currently eligible for recruitment.
        """
        return self.is_recruitable