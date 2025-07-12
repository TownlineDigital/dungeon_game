import pygame
import os
from dungeon_recruiter.combat.ability import Ability

class Unit:
    def __init__(self, name, health, mana, attack, defense, abilities=None, speed = 5):
        self.name = name
        self.base_max_health = health
        self.base_max_mana = mana
        self.base_attack = attack
        self.base_defense = defense
        self.speed = speed
        self.weapon = None
        self.armor = None
        self.update_stats()
        self.current_health = self.max_health
        self.current_mana = self.max_mana
        self.abilities = abilities or []
        self.rect = pygame.Rect(0, 0, 100, 120)
        self.level = 1
        self.status_effect = []


    def update_stats(self):
        self.max_health = self.base_max_health
        self.max_mana = self.base_max_mana
        self.attack_val = self.base_attack
        self.defense_val = self.base_defense
        if self.weapon:
            self.attack_val += self.weapon.stats.get('attack', 0)
        if self.armor:
            self.max_health += self.armor.stats.get('health', 0)
            self.defense_val += self.armor.stats.get('defense', 0)

    def equip(self, gear_item, gear_stash):
        if gear_item.type == 'Weapon':
            if self.weapon:
                gear_stash.append(self.weapon)
            self.weapon = gear_item
        elif gear_item.type == 'Armor':
            if self.armor:
                gear_stash.append(self.armor)
            self.armor = gear_item

        self.update_stats()
        self.current_health = min(self.current_health, self.max_health)

    def is_alive(self):
        return self.current_health > 0

    def attack(self, target, power_multiplier=1.0):
        damage = max(1, int(self.attack_val * power_multiplier) - target.defense_val)
        target.current_health = max(0, target.current_health - damage)
        return f"{self.name} hits {target.name} for {damage} damage!"

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)
        return f"{self.name} heals for {amount} HP!"

    def restore_mana(self, amount):
        self.current_mana = min(self.max_mana, self.current_mana + amount)
        return f"{self.name} restores {amount} Mana!"

    def add_status_effects(self):

        remaining_effects = []
        for effect in self.status_effects:
            still_active = effect.tick(self)
            if still_active:
                remaining_effects.append(effect)
            else:
                print(f"[STATUS] {effect.name} expired on {self.name}")
        self.status_effects = remaining_effects
