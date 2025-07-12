import pygame
import os

def load_animation_frames_by_type(base_path):
    """Returns a dict: {'idle': [...], 'walk': [...]}"""
    animations = {}
    for animation_type in os.listdir(base_path):
        type_path = os.path.join(base_path, animation_type)
        if os.path.isdir(type_path):
            frames = []
            for file in sorted(os.listdir(type_path)):
                if file.endswith(".png"):
                    img = pygame.image.load(os.path.join(type_path, file)).convert_alpha()
                    frames.append(img)
            animations[animation_type] = frames
    return animations

class CharacterAnimationManager:
    def __init__(self, animations_dict, frame_duration=200):
        self.animations = animations_dict
        self.current_type = "idle"
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

    def set_animation(self, animation_type):
        if animation_type in self.animations and animation_type != self.current_type:
            self.current_type = animation_type
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()

    def get_current_frame(self):
        frames = self.animations[self.current_type]
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.last_update = now
        return frames[self.current_frame]

    def get_static_frame(self):
        return self.animations[self.current_type][0]

# class AnimatedSprite:
#     def __init__(self, frames, frame_duration=200):
#         self.frames = frames
#         self.frame_duration = frame_duration  # milliseconds
#         self.current_frame = 0
#         self.last_update = pygame.time.get_ticks()
#
#     def get_current_frame(self):
#         now = pygame.time.get_ticks()
#         if now - self.last_update > self.frame_duration:
#             self.current_frame = (self.current_frame + 1) % len(self.frames)
#             self.last_update = now
#         return self.frames[self.current_frame]