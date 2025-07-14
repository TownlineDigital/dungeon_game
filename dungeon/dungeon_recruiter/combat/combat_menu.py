import pygame

class PlayerActionMenu:
    def __init__(self):
        self.actions = ["Attack", "Abilities", "Recruit", "Flee"]
        self.selected_index = 0
        self.visible = False
        self.cooldown = 0

        # 🔸 Submenu state
        self.ability_menu_visible = False
        self.abilities = []
        self.selected_ability_index = 0

    def show(self):
        self.visible = True
        self.selected_index = 0
        self.ability_menu_visible = False

    def hide(self):
        self.visible = False
        self.ability_menu_visible = False

    def enter_ability_menu(self, abilities):
        print("[DEBUG] Entering ability menu")
        self.ability_menu_visible = True
        self.abilities = abilities
        self.selected_ability_index = 0

    def exit_ability_menu(self):
        self.ability_menu_visible = False
        self.abilities = []
        self.selected_ability_index = 0

    def update_input(self, keys, now):
        if not self.visible or now - self.cooldown < 150:
            return None

        if self.ability_menu_visible:
            if keys[pygame.K_UP]:
                self.selected_ability_index = (self.selected_ability_index - 1) % len(self.abilities)
                self.cooldown = now
            elif keys[pygame.K_DOWN]:
                self.selected_ability_index = (self.selected_ability_index + 1) % len(self.abilities)
                self.cooldown = now
            elif keys[pygame.K_RETURN]:
                self.cooldown = now
                return f"Ability:{self.abilities[self.selected_ability_index].name}"
            elif keys[pygame.K_ESCAPE]:
                self.exit_ability_menu()
                self.cooldown = now
        else:
            if keys[pygame.K_UP]:
                self.selected_index = (self.selected_index - 1) % len(self.actions)
                self.cooldown = now
            elif keys[pygame.K_DOWN]:
                self.selected_index = (self.selected_index + 1) % len(self.actions)
                self.cooldown = now
            elif keys[pygame.K_RETURN]:
                action = self.actions[self.selected_index]
                self.cooldown = now
                return action

        return None