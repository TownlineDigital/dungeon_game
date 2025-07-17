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
        if now - self.cooldown < 200:
            return None

        if self.ability_menu_visible:
            # Handle ability submenu only
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.selected_ability_index = (self.selected_ability_index - 1) % len(self.abilities)
                self.cooldown = now
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.selected_ability_index = (self.selected_ability_index + 1) % len(self.abilities)
                self.cooldown = now
            elif keys[pygame.K_RETURN]:
                self.cooldown = now
                return f"Ability:{self.abilities[self.selected_ability_index].name}"
            elif keys[pygame.K_ESCAPE]:
                self.exit_ability_menu()
                self.cooldown = now
            return None  # Exit after processing ability input

        # If we're not in ability menu, process main action menu
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.selected_index = (self.selected_index - 1) % len(self.actions)
            self.cooldown = now
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.selected_index = (self.selected_index + 1) % len(self.actions)
            self.cooldown = now
        elif keys[pygame.K_RETURN]:
            action = self.actions[self.selected_index]
            self.cooldown = now
            return action

        return None

    # def update_input(self, keys, now):
    #     # if not self.visible or now - self.cooldown < 150:
    #     #     return None
    #     if now - self.cooldown > 200:
    #
    #         # Navigation (arrow keys and WASD)
    #         if keys[pygame.K_UP] or keys[pygame.K_w]:
    #             self.selected_index = (self.selected_index - 1) % len(self.actions)
    #             self.cooldown = now
    #         if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    #             self.selected_index = (self.selected_index + 1) % len(self.actions)
    #             self.cooldown = now
    #
    #         # Select action
    #         if keys[pygame.K_RETURN]:
    #             self.cooldown = now
    #             return self.actions[self.selected_index]
    #
    #         return None
    #
    #         if self.ability_menu_visible:
    #             if keys[pygame.K_UP] or keys[pygame.K_w]:
    #                 self.selected_ability_index = (self.selected_ability_index - 1) % len(self.abilities)
    #                 self.cooldown = now
    #             elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
    #                 self.selected_ability_index = (self.selected_ability_index + 1) % len(self.abilities)
    #                 self.cooldown = now
    #             elif keys[pygame.K_RETURN]:
    #                 self.cooldown = now
    #                 return f"Ability:{self.abilities[self.selected_ability_index].name}"
    #             elif keys[pygame.K_ESCAPE]:
    #                 self.exit_ability_menu()
    #                 self.cooldown = now
    #         else:
    #             if keys[pygame.K_UP]:
    #                 self.selected_index = (self.selected_index - 1) % len(self.actions)
    #                 self.cooldown = now
    #             elif keys[pygame.K_DOWN]:
    #                 self.selected_index = (self.selected_index + 1) % len(self.actions)
    #                 self.cooldown = now
    #             elif keys[pygame.K_RETURN]:
    #                 action = self.actions[self.selected_index]
    #                 self.cooldown = now
    #                 return action
    #
    #         return None