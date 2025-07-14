import pygame

class CombatInputHandler:
    def __init__(self, combat_manager, action_menu):
        self.combat_manager = combat_manager
        self.action_menu = action_menu
        self.mode = "action_menu"  # or "target_select"
        self.pending_action = None
        self.selected_target_index = 0
        self.cooldown = 0
        self.selected_ability = None

    def update(self, keys, now):
        if self.mode == "action_menu":
            action = self.action_menu.update_input(keys, now)
            if self.action_menu.ability_menu_visible:
                # Navigate ability submenu
                abilities = self.action_menu.abilities
                if keys[pygame.K_UP]:
                    self.action_menu.selected_ability_index = (self.action_menu.selected_ability_index - 1) % len(
                        abilities)
                    self.cooldown = now
                elif keys[pygame.K_DOWN]:
                    self.action_menu.selected_ability_index = (self.action_menu.selected_ability_index + 1) % len(
                        abilities)
                    self.cooldown = now
                elif keys[pygame.K_RETURN]:
                    self.selected_ability = abilities[self.action_menu.selected_ability_index]
                    self.pending_action = "Abilities"
                    self.mode = "target_select"
                    self.action_menu.ability_menu_visible = False
                    self.selected_target_index = 0
                    self.cooldown = now
                elif keys[pygame.K_ESCAPE]:
                    self.action_menu.ability_menu_visible = False
                    self.cooldown = now
                return

            if action is None:
                return

            current_unit = self.combat_manager.get_current_unit()

            if action == "Attack":
                self.pending_action = "Attack"
                self.mode = "target_select"
                self.selected_target_index = 0


            elif action == "Abilities":
                print(f"[Debug] {current_unit.name} abilities: {getattr(current_unit, 'abilities', None)}")
                print("[Debug] 'Abilities' option selected.")

                # Show ability submenu for current unit
                if hasattr(current_unit, "abilities") and current_unit.abilities:
                    self.action_menu.enter_ability_menu(current_unit.abilities)
                    return
                else:
                    print(f"[Info] {current_unit.name} has no abilities.")
                    self.reset()

            elif action.startswith("Ability:"):
                ability_name = action.split("Ability:")[1].strip()
                self.selected_ability = None

                # Try to find the matching ability
                for ability in current_unit.abilities:
                    if ability.name == ability_name:
                        self.selected_ability = ability
                        break

                if self.selected_ability is not None:
                    self.pending_action = "Abilities"
                    self.mode = "target_select"
                    self.selected_target_index = 0
                else:
                    print(f"[Error] Ability '{ability_name}' not found on {current_unit.name}")
                    self.reset()

            elif action == "Recruit":
                self.combat_manager.attempt_recruit()
                self.combat_manager.advance_turn()

            elif action == "Flee":
                self.combat_manager.attempt_flee()
                self.combat_manager.advance_turn()
            # action = self.action_menu.update_input(keys, now)
            # if action:
            #     if action in ["Attack", "Abilities"]:
            #         self.pending_action = action
            #         self.mode = "target_select"
            #         self.selected_target_index = 0
            #     elif action == "Recruit":
            #         self.combat_manager.attempt_recruit()
            #         self.combat_manager.advance_turn()
            #     elif action == "Flee":
            #         self.combat_manager.attempt_flee()
            #         self.combat_manager.advance_turn()
        elif self.mode == "target_select":
            return self.handle_target_select(keys, now)

    def handle_ability_select(self, keys, now):
        unit = self.combat_manager.get_current_unit()
        abilities = unit.abilities

        if keys[pygame.K_UP]:
            self.selected_ability_index = (self.selected_ability_index - 1) % len(abilities)
            self.cooldown = now
        elif keys[pygame.K_DOWN]:
            self.selected_ability_index = (self.selected_ability_index + 1) % len(abilities)
            self.cooldown = now
        elif keys[pygame.K_RETURN]:
            self.selected_ability = abilities[self.selected_ability_index]
            self.mode = "target_select"
            self.cooldown = now
        elif keys[pygame.K_ESCAPE]:
            self.mode = "action_menu"
            self.pending_action = None
            self.cooldown = now

    def handle_target_select(self, keys, now):
        if now - self.cooldown < 150:
            return

        enemies = self.combat_manager.get_living_targets(self.combat_manager.enemy_party)

        if not enemies:
            print("[Debug] No valid targets remaining.")
            self.reset()
            return

        if keys[pygame.K_LEFT]:
            self.selected_target_index = (self.selected_target_index - 1) % len(enemies)
            self.cooldown = now
        elif keys[pygame.K_RIGHT]:
            self.selected_target_index = (self.selected_target_index + 1) % len(enemies)
            self.cooldown = now
        elif keys[pygame.K_RETURN]:
            target = enemies[self.selected_target_index]
            current = self.combat_manager.get_current_unit()

            if self.pending_action == "Attack":
                self.combat_manager.perform_attack(current, target)
            elif self.pending_action == "Abilities":
                self.combat_manager.use_ability(current, self.selected_ability, target)

            self.reset()
            self.combat_manager.advance_turn()

        elif keys[pygame.K_ESCAPE]:
            self.reset()

    def reset(self):
        self.mode = "action_menu"
        self.pending_action = None
        self.selected_target_index = 0
        self.selected_ability = None
        self.cooldown = 0

        self.action_menu.ability_menu_visible = False
        self.action_menu.abilities = []




# import random
# from game_state import GameState
#
# def handle_player_action(action, game, combat_manager, combat_menu):
#     """
#     Executes the chosen action during a player's turn.
#     `action`: str, one of the combat menu options.
#     """
#     current_unit = combat_manager.get_current_unit()
#
#     if action == "Attack":
#         # Target the first alive enemy for now
#         targets = combat_manager.get_living_targets(game.enemy_party)
#         if targets:
#             target = targets[0]
#             combat_manager.perform_attack(current_unit, target)
#
#     elif action == "Abilities":
#         game.set_notification(f"{current_unit.name} tries to use an ability... (WIP)")
#
#     elif action == "Recruit":
#         # Simple recruit chance for now
#         targets = combat_manager.get_living_targets(game.enemy_party)
#         if targets:
#             target = targets[0]
#             success_chance = current_unit.recruiting / 100  # e.g. 20 = 20%
#             if random.random() < success_chance:
#                 game.set_notification(f"You recruited {target.name}!")
#                 game.sanctuary_roster.append(target)
#                 target.current_health = 0  # remove from battle
#             else:
#                 game.set_notification("Recruit attempt failed!")
#
#     elif action == "Flee":
#         game.set_notification("You fled the battle!")
#         game.state = GameState.EXPLORATION
#         return  # Skip advance turn to exit
#
#     # End the turn after a valid action
#     combat_manager.advance_turn()
#     combat_menu.hide()