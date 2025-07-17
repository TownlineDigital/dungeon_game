import os
import pygame

# sprites = load_dungeon_assets(tile_size=TILE_SIZE)

def get_loaded_sprites(tile_size=32):
    return load_dungeon_assets(tile_size = tile_size)

def load_sprite(path, scale):
    image = pygame.image.load(path).convert_alpha()
    if image.get_size() != (scale, scale):
        image = pygame.transform.scale(image, (scale, scale))
    return image

# def load_sprite(path, scale=32):
#     sprite = pygame.image.load(path).convert_alpha()
#     return pygame.transform.scale(sprite, (scale, scale))

def get_player_idle_sprite(name, scale=None):
    safe_name = name.lower()
    filename = f"{safe_name}_idle_0.png"
    path = os.path.join("assets", "sprites", safe_name, "idle", filename)

    if os.path.exists(path):
        sprite = pygame.image.load(path).convert_alpha()
        if scale:
            sprite = pygame.transform.scale(sprite, (scale, scale))
        return sprite
    else:
        print(f"[ERROR] Player idle sprite not found at: {path}")
        fallback_size = scale or 96
        fallback = pygame.Surface((fallback_size, fallback_size), pygame.SRCALPHA)
        pygame.draw.rect(fallback, (255, 0, 0, 128), fallback.get_rect(), 2)
        return fallback

def get_enemy_idle_sprite(name, scale=None):
    safe_name = name.lower().replace(" ", "_")
    filename = f"{safe_name}_idle_0.png"
    path = os.path.join("assets", "enemy_sprites", safe_name, "idle", filename)

    if os.path.exists(path):
        sprite = pygame.image.load(path).convert_alpha()
        if scale:
            sprite = pygame.transform.scale(sprite, (scale, scale))
        return sprite
    else:
        print(f"[ERROR] Enemy idle sprite not found at: {path}")
        fallback_size = scale or 96
        fallback = pygame.Surface((fallback_size, fallback_size), pygame.SRCALPHA)
        pygame.draw.rect(fallback, (255, 0, 0, 128), fallback.get_rect(), 2)
        return fallback

def get_in_dungeon_sprite(name, scale=None, is_enemy=False):
    """
    Load in-dungeon sprite for characters and enemies by name.
    `is_enemy`: True if loading for an enemy.
    `scale`: optional int size to scale the sprite to.
    """
    base_folder = "enemy_sprites" if is_enemy else "sprites"
    safe_name = name.lower().replace(" ", "_")
    filename = f"{safe_name}_in_dungeon.png"
    path = os.path.join("assets", base_folder, safe_name, "in_dungeon", filename)

    if os.path.exists(path):
        sprite = pygame.image.load(path).convert_alpha()
        if scale:
            sprite = pygame.transform.scale(sprite, (scale, scale))
        return sprite
    else:
        print(f"[ERROR] In-dungeon sprite not found at: {path}")
        fallback_size = scale or 32
        fallback = pygame.Surface((fallback_size, fallback_size), pygame.SRCALPHA)
        pygame.draw.rect(fallback, (0, 255, 0, 128), fallback.get_rect(), 2)
        return fallback

def load_dungeon_assets(tile_size=32):
    """
    Preloads static tile, enemy, and player sprites into a dictionary.
    Used for the dungeon exploration map.
    """
    sprite_dict = {}

    # Tiles
    tile_path = os.path.join("assets", "tiles")
    if os.path.exists(tile_path):
        for file in os.listdir(tile_path):
            if file.endswith(".png"):
                key = file.split(".")[0].upper()
                path = os.path.join(tile_path, file)
                sprite_dict[key] = load_sprite(path, scale=tile_size)
                print(f"[TILE] Loaded: {key} from {path}")

    # Enemy in-dungeon sprites
    enemy_base = os.path.join("assets", "enemy_sprites")
    if os.path.exists(enemy_base):
        for enemy_folder in os.listdir(enemy_base):
            in_dungeon_path = os.path.join(enemy_base, enemy_folder, "in_dungeon")
            if os.path.exists(in_dungeon_path):
                for file in os.listdir(in_dungeon_path):
                    if file.endswith(".png"):
                        key = f"ENEMY_{enemy_folder.upper()}"
                        path = os.path.join(in_dungeon_path, file)
                        sprite_dict[key] = load_sprite(path,scale=tile_size)
                        print(f"[ENEMY] Loaded: {key} from {path}")

    # Player in-dungeon sprites
    player_base = os.path.join("assets", "sprites")
    if os.path.exists(player_base):
        for player_folder in os.listdir(player_base):
            in_dungeon_path = os.path.join(player_base, player_folder, "in_dungeon")
            if os.path.exists(in_dungeon_path):
                for file in os.listdir(in_dungeon_path):
                    if file.endswith(".png"):
                        key = f"PLAYER_{player_folder.upper()}"
                        path = os.path.join(in_dungeon_path, file)
                        sprite_dict[key] = load_sprite(path, scale=tile_size)
                        print(f"[PLAYER] Loaded: {key} from {path}")

    return sprite_dict
