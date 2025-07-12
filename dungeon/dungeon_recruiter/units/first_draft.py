import pygame
import random
import sys
import time

# --- Pygame Initialization ---
pygame.init()

# --- Game Constants ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 800
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Recruiter: Loot & Legends")
FPS = 60
FONT = pygame.font.SysFont("corbel", 22)
FONT_BOLD = pygame.font.SysFont("corbel", 26, bold=True)
TITLE_FONT = pygame.font.SysFont("georgia", 60, bold=True)
TILE_SIZE = 32

# --- Colors (unchanged) ---
BLACK, WHITE, DARK_GREY, GREY, LIGHT_GREY = (0, 0, 0), (255, 255, 255), (25, 25, 25), (100, 100, 100), (170, 170, 170)
PLAYER_COLOR, ENEMY_COLOR, ELITE_ENEMY_COLOR = (60, 150, 255), (220, 40, 40), (139, 0, 0)
GREEN, MANA_BLUE, GOLD = (40, 200, 40), (90, 120, 255), (255, 215, 0)
FLOOR_COLOR, WALL_COLOR, EXIT_COLOR, CHEST_COLOR = (50, 50, 50), (80, 70, 60), (60, 200, 220), (140, 80, 30)
OVERLAY_BG = (0, 0, 0, 200)


# --- Game State Enum ---
class GameState:
    MAIN_MENU, SANCTUARY, EXPLORATION, COMBAT, GAME_OVER = range(5)


# --- Game Logic Classes (Unchanged) ---
class Ability:
    def __init__(self, name, power_multiplier,
                 mana_cost): self.name, self.power, self.cost = name, power_multiplier, mana_cost


class Gear:
    def __init__(self, name, gear_type, stat_boosts): self.name, self.type, self.stats = name, gear_type, stat_boosts

    def __str__(self): return self.name if self is not None else "None"


class Skill:
    def __init__(self, name, description, effects):
        self.name, self.description, self.effects, self.unlocked = name, description, effects, False

    def apply(self, unit):
        if self.unlocked: return
        for stat, value in self.effects.items():
            base_stat_name = f"base_{stat}"
            setattr(unit, base_stat_name, getattr(unit, base_stat_name) + value)
        unit.update_stats();
        self.unlocked = True


class SkillTree:
    def __init__(self, rarity):
        self.skills = []
        if rarity == "Common":
            self.skills.append(Skill("Toughness I", "+15 HP", {'max_health': 15}))
        elif rarity == "Elite":
            self.skills.append(Skill("Toughness II", "+30 HP", {'max_health': 30})); self.skills.append(
                Skill("Strength I", "+5 ATK", {'attack': 5}))


class Unit:
    def __init__(self, name, health, mana, attack, defense):
        self.name = name;
        self.base_max_health, self.base_max_mana, self.base_attack, self.base_defense = health, mana, attack, defense
        self.weapon, self.armor = None, None;
        self.update_stats()
        self.current_health, self.current_mana = self.max_health, self.max_mana
        self.abilities = [Ability("Power Strike", 1.5, 10)];
        self.rect = pygame.Rect(0, 0, 100, 120);
        self.level = 1

    def update_stats(self):
        self.max_health, self.max_mana, self.attack_val, self.defense_val = self.base_max_health, self.base_max_mana, self.base_attack, self.base_defense
        if self.weapon: self.attack_val += self.weapon.stats.get('attack', 0)
        if self.armor: self.max_health += self.armor.stats.get('health', 0); self.defense_val += self.armor.stats.get(
            'defense', 0)

    def equip(self, gear_item, gear_stash):
        if gear_item.type == 'Weapon':
            if self.weapon: gear_stash.append(self.weapon)
            self.weapon = gear_item
        elif gear_item.type == 'Armor':
            if self.armor: gear_stash.append(self.armor)
            self.armor = gear_item
        self.update_stats();
        self.current_health = min(self.current_health, self.max_health)

    def is_alive(self):
        return self.current_health > 0

    def attack(self, target, power_multiplier=1.0):
        damage = max(1, int(self.attack_val * power_multiplier) - target.defense_val)
        target.current_health = max(0, target.current_health - damage)
        return f"{self.name} hits {target.name} for {damage} damage!"

    def heal(self, amount):
        self.current_health = min(self.max_health,
                                  self.current_health + amount); return f"{self.name} heals for {amount} HP!"

    def restore_mana(self, amount):
        self.current_mana = min(self.max_mana,
                                self.current_mana + amount); return f"{self.name} restores {amount} Mana!"


class Player(Unit):
    def __init__(self): super().__init__("Hero", 100, 30, 15, 5)


class Enemy(Unit):
    def __init__(self, name, health, mana, attack, defense, rarity):
        super().__init__(name, health, mana, attack, defense);
        self.rarity = rarity
        self.exp, self.exp_to_next_level = 0, 100;
        self.skill_points = 0;
        self.skill_tree = SkillTree(rarity)

    def gain_exp(self, amount, game):
        self.exp += amount;
        leveled_up = False
        while self.exp >= self.exp_to_next_level: self.exp -= self.exp_to_next_level; self.level_up(
            game); leveled_up = True
        return leveled_up

    def level_up(self, game):
        self.level += 1;
        self.skill_points += 1;
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.base_max_health += 10;
        self.base_attack += 2;
        self.base_defense += 1;
        self.update_stats()
        self.current_health, self.current_mana = self.max_health, self.max_mana
        game.set_notification(f"{self.name} grew to Level {self.level}!")


# --- UI Helper Functions ---
def draw_text(text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color);
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    WIN.blit(text_surface, text_rect);
    return text_rect


def draw_button(rect, text, base_color, hover_color, selected=False, disabled=False):
    mouse_pos = pygame.mouse.get_pos();
    is_hovered = rect.collidepoint(mouse_pos)
    color = base_color
    if disabled:
        color = DARK_GREY
    elif is_hovered:
        color = hover_color
    if selected and not disabled: pygame.draw.rect(WIN, GOLD, rect.inflate(6, 6), 3, border_radius=10)
    pygame.draw.rect(WIN, color, rect, border_radius=8)
    draw_text(text, FONT_BOLD, WHITE if not disabled else GREY, rect.centerx, rect.centery, center=True)
    return is_hovered and not disabled and pygame.mouse.get_pressed()[0]


def draw_health_bar(x, y, width, height, current, maximum, color):
    ratio = max(0, current / maximum) if maximum > 0 else 0
    pygame.draw.rect(WIN, DARK_GREY, (x, y, width, height));
    pygame.draw.rect(WIN, color, (x, y, width * ratio, height))
    pygame.draw.rect(WIN, WHITE, (x, y, width, height), 2)


# --- Main Game Class ---
class Game:
    def __init__(self):
        self.state = GameState.MAIN_MENU;
        self.clock = pygame.time.Clock()
        self.player = Player();
        self.sanctuary_roster = [Enemy("Goblin Grunt", 40, 10, 8, 2, "Common")]
        self.dungeon_level = 1;
        self.inventory = {'Healing Potion': 2, 'Mana Potion': 1, 'EXP Booster': 0}
        self.gear_stash = [Gear("Old Helmet", "Armor", {'defense': 2})];
        self.player_map_pos = [0, 0];
        self.dungeon_map = []
        self.show_extraction_prompt, self.show_inventory_screen = False, False
        self.move_timer, self.move_cooldown = 0, 120;
        self.notification, self.notification_timer = "", 0
        self.active_party, self.enemy_party, self.dungeon_party = [], [], []
        self.turn_index, self.turn_phase = 0, "PLAYER";
        self.combat_sub_state, self.selected_action = "SELECT_ACTION", None;
        self.combat_log = []
        self.selected_unit_for_management = None;
        self.combat_menu_selection = 0
        self.combat_menu_options = ["Attack", "Ability", "Item", "Recruit", "Retreat"]
        self.loot_table = ['Healing Potion', 'Mana Potion', Gear("Tattered Tunic", "Armor", {'health': 20}),
                           Gear("Iron Sword", "Weapon", {'attack': 5}), 'EXP Booster']
        self.difficulty_colors = {'Common': ENEMY_COLOR, 'Elite': ELITE_ENEMY_COLOR}

    def set_notification(self, message):
        self.notification = message; self.notification_timer = FPS * 3

    def generate_dungeon_map(self, width=100, height=100, steps=20000):
        # (Unchanged)
        self.dungeon_map = [['W' for _ in range(width)] for _ in range(height)]
        x, y = width // 2, height // 2
        for _ in range(steps):
            self.dungeon_map[y][x] = ' ';
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)]);
            x, y = max(1, min(width - 2, x + dx)), max(1, min(height - 2, y + dy))
        self.player_map_pos = [width // 2, height // 2]
        for _ in range(50):
            rx, ry = random.randint(1, width - 2), random.randint(1, height - 2)
            if self.dungeon_map[ry][rx] == ' ': self.dungeon_map[ry][rx] = random.choice(['E', 'E', 'E', 'S', 'T', 'T'])
        while True:
            rx, ry = random.randint(1, width - 2), random.randint(1, height - 2)
            if self.dungeon_map[ry][rx] == ' ': self.dungeon_map[ry][rx] = 'X'; break

    def move_player(self, dx, dy):
        if self.show_extraction_prompt or self.show_inventory_screen: return
        new_x, new_y = self.player_map_pos[0] + dx, self.player_map_pos[1] + dy
        if self.dungeon_map[new_y][new_x] != 'W':
            self.player_map_pos = [new_x, new_y];
            tile = self.dungeon_map[new_y][new_x]
            if tile == 'E':
                self.dungeon_map[new_y][new_x] = ' '; self.start_combat(is_elite=False)
            elif tile == 'S':
                self.dungeon_map[new_y][new_x] = ' '; self.start_combat(is_elite=True)
            elif tile == 'X':
                self.state = GameState.SANCTUARY
            elif tile == 'T':
                self.dungeon_map[new_y][new_x] = ' '; self.get_loot()

    def get_loot(self):
        found_item = random.choice(self.loot_table)
        if isinstance(found_item, str):
            self.inventory[found_item] = self.inventory.get(found_item, 0) + 1; self.set_notification(
                f"Found: {found_item}!")
        elif isinstance(found_item, Gear):
            self.gear_stash.append(found_item); self.set_notification(f"Found Gear: {found_item.name}!")

    def start_combat(self, is_elite=False):
        self.state = GameState.COMBAT;
        self.active_party = self.dungeon_party
        if is_elite:
            self.enemy_party = [Enemy("Elite Orc", 120, 20, 18, 10, "Elite")]
        else:
            self.enemy_party = [Enemy("Cave Bat", 30, 0, 8, 2, "Common"), Enemy("Slime", 50, 20, 6, 4, "Common")]
        for i, unit in enumerate(self.active_party): unit.rect.center = (300, 200 + i * 180)
        for i, unit in enumerate(self.enemy_party): unit.rect.center = (SCREEN_WIDTH - 300, 200 + i * 180)
        self.turn_index, self.turn_phase, self.combat_menu_selection = 0, "PLAYER", 0;
        self.combat_sub_state = "SELECT_ACTION";
        self.combat_log = ["A battle begins!"]

    # FIXED: Rewrote next_turn to be non-recursive and prevent crashes.
    def next_turn(self):
        self.combat_sub_state = "SELECT_ACTION"
        self.combat_menu_selection = 0

        if self.turn_phase == "PLAYER":
            # Move to the next player or switch to enemy phase
            self.turn_index += 1
            if self.turn_index >= len(self.active_party):
                self.turn_index = 0
                self.turn_phase = "ENEMY"
        else:  # ENEMY turn
            # Move to the next enemy or switch to player phase
            self.turn_index += 1
            if self.turn_index >= len(self.enemy_party):
                self.turn_index = 0
                self.turn_phase = "PLAYER"

        # Now, find the next living unit using a safe while loop
        iterations = 0
        while iterations < len(self.active_party) + len(self.enemy_party):
            current_party = self.active_party if self.turn_phase == "PLAYER" else self.enemy_party
            # Check if party has members before indexing
            if not current_party:
                # This party is empty, switch to the other one
                self.turn_phase = "PLAYER" if self.turn_phase == "ENEMY" else "ENEMY"
                self.turn_index = 0
                iterations += 1
                continue

            # Check if current unit is alive
            if current_party[self.turn_index].is_alive():
                return  # Found a living unit, exit the function

            # If not alive, advance turn
            self.turn_index += 1
            if self.turn_phase == "PLAYER" and self.turn_index >= len(self.active_party):
                self.turn_index = 0;
                self.turn_phase = "ENEMY"
            elif self.turn_phase == "ENEMY" and self.turn_index >= len(self.enemy_party):
                self.turn_index = 0;
                self.turn_phase = "PLAYER"

            iterations += 1

    def enter_dungeon(self):
        self.dungeon_party = [self.player] + self.sanctuary_roster[:2]
        self.generate_dungeon_map();
        self.state = GameState.EXPLORATION


if __name__ == "__main__":
    game = Game()
    while True:
        game.clock.tick(FPS);
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: clicked = True

            if event.type == pygame.KEYDOWN:
                if game.state == GameState.EXPLORATION:
                    if event.key == pygame.K_i:
                        game.show_inventory_screen = not game.show_inventory_screen; game.combat_sub_state = "SELECT_ACTION"
                    elif event.key == pygame.K_ESCAPE:
                        game.show_inventory_screen = False
                    if not game.show_extraction_prompt and not game.show_inventory_screen:
                        if event.key == pygame.K_e: game.show_extraction_prompt = True
                    elif game.show_extraction_prompt:
                        if event.key == pygame.K_y:
                            game.state, game.show_extraction_prompt = GameState.SANCTUARY, False
                        elif event.key == pygame.K_n:
                            game.show_extraction_prompt = False
                elif game.state == GameState.COMBAT and game.turn_phase == "PLAYER" and game.combat_sub_state == "SELECT_ACTION":
                    if event.key == pygame.K_UP:
                        game.combat_menu_selection = (game.combat_menu_selection - 1) % len(game.combat_menu_options)
                    elif event.key == pygame.K_DOWN:
                        game.combat_menu_selection = (game.combat_menu_selection + 1) % len(game.combat_menu_options)
                    elif event.key == pygame.K_RETURN:
                        action_name = game.combat_menu_options[game.combat_menu_selection]
                        active_unit = game.active_party[game.turn_index]
                        if action_name == "Attack":
                            game.selected_action, game.combat_sub_state = "ATTACK", "SELECT_TARGET"
                        elif action_name == "Ability":
                            if active_unit.abilities and active_unit.current_mana >= active_unit.abilities[0].cost:
                                game.selected_action, game.combat_sub_state = active_unit.abilities[0], "SELECT_TARGET"
                            else:
                                game.combat_log.append("Not enough mana or no ability!")
                        elif action_name == "Item":
                            game.selected_action, game.combat_sub_state = "SELECT_ITEM", "SELECT_FRIENDLY_TARGET"
                        elif action_name == "Recruit":
                            game.selected_action, game.combat_sub_state = "RECRUIT", "SELECT_TARGET"
                        elif action_name == "Retreat":
                            game.set_notification("Retreated!"); game.state = GameState.EXPLORATION

        if game.state == GameState.EXPLORATION and not game.show_extraction_prompt and not game.show_inventory_screen:
            now = pygame.time.get_ticks()
            if now - game.move_timer > game.move_cooldown:
                keys, moved = pygame.key.get_pressed(), False
                if keys[pygame.K_UP]:
                    game.move_player(0, -1); moved = True
                elif keys[pygame.K_DOWN]:
                    game.move_player(0, 1); moved = True
                elif keys[pygame.K_LEFT]:
                    game.move_player(-1, 0); moved = True
                elif keys[pygame.K_RIGHT]:
                    game.move_player(1, 0); moved = True
                if moved: game.move_timer = now

        if game.state == GameState.COMBAT and game.turn_phase == "PLAYER" and clicked:
            attacker = game.active_party[game.turn_index];
            action_taken = False;
            recruited_enemy_info = None
            if game.combat_sub_state == "SELECT_TARGET":
                for i, target in enumerate(game.enemy_party):
                    if target.rect.collidepoint(pygame.mouse.get_pos()) and target.is_alive():
                        if game.selected_action == "ATTACK":
                            game.combat_log.append(attacker.attack(target)); action_taken = True
                        elif game.selected_action == "RECRUIT":
                            chance = (1.0 - (target.current_health / target.max_health)) * 0.7
                            if random.random() < chance:
                                game.combat_log.append(f"Recruited {target.name}!"); game.sanctuary_roster.append(
                                    target); recruited_enemy_info = i
                            else:
                                game.combat_log.append(f"Failed to recruit {target.name}!")
                            action_taken = True
                        elif isinstance(game.selected_action, Ability):
                            if attacker.current_mana >= game.selected_action.cost: attacker.current_mana -= game.selected_action.cost; game.combat_log.append(
                                attacker.attack(target, game.selected_action.power)); action_taken = True
            elif game.combat_sub_state == "SELECT_FRIENDLY_TARGET":
                for target in game.active_party:
                    if target.rect.collidepoint(pygame.mouse.get_pos()) and target.is_alive():
                        if game.selected_action == "USE_HEAL_POTION":
                            if game.inventory['Healing Potion'] > 0: game.inventory[
                                'Healing Potion'] -= 1; game.combat_log.append(target.heal(40)); action_taken = True
                        elif game.selected_action == "USE_MANA_POTION":
                            if game.inventory['Mana Potion'] > 0: game.inventory[
                                'Mana Potion'] -= 1; game.combat_log.append(
                                target.restore_mana(20)); action_taken = True

            if recruited_enemy_info is not None: game.enemy_party.pop(recruited_enemy_info)
            if action_taken:
                if any(u.is_alive() for u in game.enemy_party): game.next_turn()

        WIN.fill(DARK_GREY)
        if game.state == GameState.MAIN_MENU:
            draw_text("Dungeon Recruiter", TITLE_FONT, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, center=True)
            if draw_button(pygame.Rect(SCREEN_WIDTH / 2 - 125, SCREEN_HEIGHT / 2, 250, 50), "Start Game", PLAYER_COLOR,
                           GREEN): game.state = GameState.SANCTUARY
        elif game.state == GameState.SANCTUARY:
            draw_text("Sanctuary", TITLE_FONT, WHITE, SCREEN_WIDTH / 2, 50, center=True);
            col1_x, col2_x, col3_x = 50, 480, 980
            pygame.draw.line(WIN, GREY, (col2_x - 30, 140), (col2_x - 30, SCREEN_HEIGHT - 150), 2);
            pygame.draw.line(WIN, GREY, (col3_x - 30, 140), (col3_x - 30, SCREEN_HEIGHT - 150), 2)
            draw_text("Your Roster", FONT_BOLD, WHITE, col1_x, 150)
            for i, unit in enumerate(game.sanctuary_roster):
                y_pos, color = 200 + i * 35, GOLD if unit == game.selected_unit_for_management else WHITE
                unit_rect = draw_text(f"{unit.name} (Lvl {unit.level})", FONT, color, col1_x + 10, y_pos)
                if clicked and unit_rect and unit_rect.collidepoint(
                    pygame.mouse.get_pos()): game.selected_unit_for_management = unit
            if game.selected_unit_for_management:
                unit = game.selected_unit_for_management;
                draw_text(f"Details: {unit.name}", FONT_BOLD, WHITE, col2_x, 150)
                draw_text(f"HP: {unit.max_health}, ATK: {unit.attack_val}, DEF: {unit.defense_val}", FONT, WHITE,
                          col2_x, 190)
                draw_text(f"Skill Points: {unit.skill_points}", FONT, GOLD, col2_x, 220)
                draw_text("Skill Tree (Click to upgrade)", FONT_BOLD, WHITE, col2_x, 270)
                for i, skill in enumerate(unit.skill_tree.skills):
                    y_pos = 310 + i * 45
                    is_disabled = unit.skill_points == 0 or skill.unlocked;
                    button_text = f"{skill.name} - {skill.description}" + (" (Unlocked)" if skill.unlocked else "")
                    if draw_button(pygame.Rect(col2_x, y_pos, 450, 40), button_text, GREY, LIGHT_GREY, False,
                                   is_disabled):
                        unit.skill_points -= 1;
                        skill.apply(unit);
                        game.set_notification(f"{unit.name} learned {skill.name}!")
                if game.inventory.get('EXP Booster', 0) > 0:
                    if draw_button(pygame.Rect(col2_x, SCREEN_HEIGHT - 100, 250, 40),
                                   f"Use EXP Booster ({game.inventory['EXP Booster']})", GREEN, GOLD):
                        game.inventory['EXP Booster'] -= 1;
                        unit.gain_exp(100, game)
            draw_text("Inventory", FONT_BOLD, WHITE, col3_x, 150)
            y_inv = 200
            for item, count in game.inventory.items(): draw_text(f"{item}: {count}", FONT, WHITE, col3_x + 10,
                                                                 y_inv); y_inv += 35
            draw_text("Gear Stash", FONT_BOLD, WHITE, col3_x, 350)
            for i, gear in enumerate(game.gear_stash):
                if game.selected_unit_for_management and draw_button(pygame.Rect(col3_x, 400 + i * 45, 250, 40),
                                                                     f"Equip {gear.name}", GREY, LIGHT_GREY):
                    game.selected_unit_for_management.equip(gear, game.gear_stash);
                    game.gear_stash.remove(gear);
                    time.sleep(0.2)
            if draw_button(pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 80, 250, 50), "Enter Dungeon", PLAYER_COLOR,
                           GREEN): game.enter_dungeon()
        elif game.state == GameState.EXPLORATION:
            cam_x, cam_y = SCREEN_WIDTH / 2 - game.player_map_pos[0] * TILE_SIZE, SCREEN_HEIGHT / 2 - \
                           game.player_map_pos[1] * TILE_SIZE
            for y, row in enumerate(game.dungeon_map):
                for x, tile in enumerate(row):
                    rect = pygame.Rect(x * TILE_SIZE + cam_x, y * TILE_SIZE + cam_y, TILE_SIZE, TILE_SIZE)
                    if tile == 'W':
                        pygame.draw.rect(WIN, WALL_COLOR, rect)
                    else:
                        pygame.draw.rect(WIN, FLOOR_COLOR, rect)
                    if tile == 'E':
                        pygame.draw.rect(WIN, ENEMY_COLOR, rect)
                    elif tile == 'S':
                        pygame.draw.rect(WIN, ELITE_ENEMY_COLOR, rect)
                    elif tile == 'X':
                        pygame.draw.rect(WIN, EXIT_COLOR, rect)
                    elif tile == 'T':
                        pygame.draw.rect(WIN, CHEST_COLOR, rect)
            pygame.draw.rect(WIN, PLAYER_COLOR,
                             pygame.Rect(SCREEN_WIDTH / 2 - TILE_SIZE / 2, SCREEN_HEIGHT / 2 - TILE_SIZE / 2, TILE_SIZE,
                                         TILE_SIZE))
            if game.show_extraction_prompt:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA);
                s.fill(OVERLAY_BG);
                WIN.blit(s, (0, 0))
                draw_text("Extract to Sanctuary?", FONT_BOLD, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                          center=True);
                draw_text("Press [Y] for Yes or [N] for No", FONT, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                          center=True)
            if game.show_inventory_screen:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA);
                s.fill(OVERLAY_BG);
                WIN.blit(s, (0, 0))
                draw_text("PARTY & INVENTORY", TITLE_FONT, WHITE, SCREEN_WIDTH / 2, 100, center=True)
                draw_text("Current Party", FONT_BOLD, WHITE, SCREEN_WIDTH / 4, 200, center=True)
                for i, unit in enumerate(game.dungeon_party):
                    y_p = 250 + i * 80
                    draw_text(f"{unit.name} Lvl.{unit.level}", FONT, WHITE, SCREEN_WIDTH / 4, y_p, center=True)
                    draw_health_bar(SCREEN_WIDTH / 4 - 100, y_p + 25, 200, 15, unit.current_health, unit.max_health,
                                    GREEN)
                    if isinstance(unit, Enemy) and draw_button(pygame.Rect(SCREEN_WIDTH / 4 - 75, y_p + 45, 150, 30),
                                                               "Send Home", GREY, LIGHT_GREY):
                        if unit in game.dungeon_party: game.dungeon_party.remove(unit); game.set_notification(
                            f"{unit.name} sent home safely!"); break
                draw_text("Items", FONT_BOLD, WHITE, SCREEN_WIDTH * 3 / 4, 200, center=True);
                y_i = 250
                if game.inventory.get('Healing Potion', 0) > 0 and draw_button(
                        pygame.Rect(SCREEN_WIDTH * 3 / 4 - 100, y_i, 200, 40),
                        f"Use Heal ({game.inventory['Healing Potion']})", GREEN, GOLD):
                    if game.player.current_health < game.player.max_health: game.inventory[
                        'Healing Potion'] -= 1; game.player.heal(40); game.set_notification("Used Healing Potion.")
                if game.inventory.get('Mana Potion', 0) > 0 and draw_button(
                        pygame.Rect(SCREEN_WIDTH * 3 / 4 - 100, y_i + 50, 200, 40),
                        f"Use Mana ({game.inventory['Mana Potion']})", MANA_BLUE, LIGHT_GREY):
                    if game.player.current_mana < game.player.max_mana: game.inventory[
                        'Mana Potion'] -= 1; game.player.restore_mana(20); game.set_notification("Used Mana Potion.")
            if game.notification_timer > 0: draw_text(game.notification, FONT_BOLD, GOLD, SCREEN_WIDTH / 2, 50,
                                                      center=True); game.notification_timer -= 1
            if game.combat_sub_state == "SELECT_FRIENDLY_TARGET":  # Using item out of combat would need more logic here
                pass
        elif game.state == GameState.COMBAT:
            WIN.fill(DARK_GREY);
            all_units = game.active_party + game.enemy_party
            for unit in all_units:
                if unit.is_alive():
                    pygame.draw.rect(WIN, GREY, unit.rect);
                    name_color = WHITE if isinstance(unit, Player) else game.difficulty_colors.get(unit.rarity,
                                                                                                   ENEMY_COLOR)
                    draw_text(f"{unit.name} (Lvl. {unit.level})", FONT_BOLD, name_color, unit.rect.centerx,
                              unit.rect.top - 25, center=True)
                    draw_health_bar(unit.rect.left, unit.rect.bottom + 5, unit.rect.width, 15, unit.current_health,
                                    unit.max_health, GREEN)
                    draw_health_bar(unit.rect.left, unit.rect.bottom + 25, unit.rect.width, 10, unit.current_mana,
                                    unit.max_mana, MANA_BLUE)
            log_y = SCREEN_HEIGHT - 30
            for i, msg in enumerate(reversed(game.combat_log[-5:])): draw_text(msg, FONT, WHITE, 20, log_y - i * 25)
            if not any(u.is_alive() for u in game.enemy_party):
                draw_text("VICTORY!", TITLE_FONT, GOLD, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, center=True);
                pygame.display.update();
                time.sleep(2)
                for unit in game.active_party:
                    if isinstance(unit, Enemy) and unit.is_alive():
                        if unit.gain_exp(50 * game.dungeon_level, game): pass
                game.state = GameState.EXPLORATION
            elif not any(u.is_alive() for u in game.active_party):
                draw_text("DEFEAT...", TITLE_FONT, ENEMY_COLOR, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, center=True);
                pygame.display.update();
                time.sleep(2)
                game.state = GameState.SANCTUARY
            elif game.turn_phase == "PLAYER":
                active_unit = game.active_party[game.turn_index];
                pygame.draw.rect(WIN, GOLD, active_unit.rect.inflate(6, 6), 4)
                if game.combat_sub_state == "SELECT_ACTION":
                    menu_x = active_unit.rect.left - 150 if active_unit.rect.centerx > SCREEN_WIDTH / 2 else active_unit.rect.right + 15
                    for i, option_name in enumerate(game.combat_menu_options):
                        rect = pygame.Rect(menu_x, active_unit.rect.top + i * 50, 120, 40);
                        is_selected = (i == game.combat_menu_selection)
                        is_disabled = option_name == "Ability" and not active_unit.abilities
                        if draw_button(rect, option_name, GREY, LIGHT_GREY, is_selected, is_disabled):
                            if option_name == "Attack":
                                game.selected_action, game.combat_sub_state = "ATTACK", "SELECT_TARGET"
                            elif option_name == "Ability" and not is_disabled:
                                game.selected_action, game.combat_sub_state = active_unit.abilities[0], "SELECT_TARGET"
                            elif option_name == "Item":
                                game.selected_action, game.combat_sub_state = "SELECT_ITEM", "SELECT_FRIENDLY_TARGET"
                            elif option_name == "Recruit":
                                game.selected_action, game.combat_sub_state = "RECRUIT", "SELECT_TARGET"
                            elif option_name == "Retreat":
                                game.state = GameState.EXPLORATION
                elif game.combat_sub_state == "SELECT_TARGET":
                    draw_text(f"Select an Enemy Target", FONT_BOLD, ENEMY_COLOR, SCREEN_WIDTH / 2, 50, center=True)
                elif game.combat_sub_state == "SELECT_FRIENDLY_TARGET":
                    if game.selected_action == "SELECT_ITEM":
                        menu_x = active_unit.rect.left - 150 if active_unit.rect.centerx > SCREEN_WIDTH / 2 else active_unit.rect.right + 15
                        if game.inventory['Healing Potion'] > 0 and draw_button(
                            pygame.Rect(menu_x, active_unit.rect.top, 180, 40),
                            f"Heal Potion ({game.inventory['Healing Potion']})", GREEN,
                            GOLD): game.selected_action = "USE_HEAL_POTION"
                        if game.inventory['Mana Potion'] > 0 and draw_button(
                            pygame.Rect(menu_x, active_unit.rect.top + 50, 180, 40),
                            f"Mana Potion ({game.inventory['Mana Potion']})", MANA_BLUE,
                            LIGHT_GREY): game.selected_action = "USE_MANA_POTION"
                    else:
                        draw_text("Select a Friendly Target", FONT_BOLD, PLAYER_COLOR, SCREEN_WIDTH / 2, 50,
                                  center=True)
            elif game.turn_phase == "ENEMY":
                pygame.display.update();
                time.sleep(1);
                enemy_unit = game.enemy_party[game.turn_index]
                if enemy_unit.is_alive():
                    target = random.choice([p for p in game.active_party if p.is_alive()]);
                    game.combat_log.append(enemy_unit.attack(target))
                if any(u.is_alive() for u in game.active_party): game.next_turn()
        pygame.display.update()