import os
import pygame
from animations import load_animation_frames_by_type, CharacterAnimationManager

character_animations = {
    "Knight": CharacterAnimationManager(load_animation_frames_by_type("assets/sprites/knight")),
    "Mage": CharacterAnimationManager(load_animation_frames_by_type("assets/sprites/mage")),
    "Rogue": CharacterAnimationManager(load_animation_frames_by_type("assets/sprites/rogue")),
    "Cleric": CharacterAnimationManager(load_animation_frames_by_type("assets/sprites/cleric")),
    "Barbarian": CharacterAnimationManager(load_animation_frames_by_type("assets/sprites/barbarian"))
    }