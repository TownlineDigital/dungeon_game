import pygame

class CombatInputHandler:
    def __init__(self, combat_manager, action_menu, game):
        self.combat_manager = combat_manager
        self.action_menu = action_menu
        self.game = game
        self.mode = "action_menu"  # or "target_select"
        self.pending_action = None
        self.selected_target_index = 0
        self.cooldown = 0
        self.selected_ability = None

    def update(self, keys, now):
        if self.mode == "target_select":
            self.handle_target_select(keys, now)
            return

        if self.mode == "action_menu":
            if self.action_menu.ability_menu_visible:
                if now - self.cooldown < 200:
                    return

                abilities = self.action_menu.abilities
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.action_menu.selected_ability_index = (self.action_menu.selected_ability_index - 1) % len(
                        abilities)
                    self.cooldown = now
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.action_menu.selected_ability_index = (self.action_menu.selected_ability_index + 1) % len(
                        abilities)
                    self.cooldown = now
                elif keys[pygame.K_RETURN] and abilities:
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

            action = self.action_menu.update_input(keys, now)
            if action is None:
                return

            current_unit = self.combat_manager.get_current_unit()

            if action == "Attack":
                self.pending_action = "Attack"
                self.mode = "target_select"
                self.selected_target_index = 0

            elif action == "Abilities":
                if hasattr(current_unit, "abilities") and current_unit.abilities:
                    self.action_menu.enter_ability_menu(current_unit.abilities)
                else:
                    self.reset()

            elif action.startswith("Ability:"):
                ability_name = action.split("Ability:")[1].strip()
                self.selected_ability = None

                for ability in current_unit.abilities:
                    if ability.name == ability_name:
                        self.selected_ability = ability
                        break

                if self.selected_ability is not None:
                    self.pending_action = "Abilities"
                    self.mode = "target_select"
                    self.selected_target_index = 0
                else:
                    print(f"[Error] Ability '{ability_name}' not found.")
                    self.reset()



            elif action == "Recruit":
                current_unit = self.combat_manager.get_current_unit()
                enemies = self.combat_manager.get_living_targets(self.combat_manager.enemy_party)

                if enemies:
                    target = enemies[0]  # Automatically try to recruit the first available target
                    self.combat_manager.attempt_recruit(current_unit, target, self.game)
                else:
                    print("[Recruit] No enemies to recruit.")
                self.reset()  # ✅ Reset the input handler to clean up the state
                self.combat_manager.advance_turn()
                self.combat_manager.end_combat_if_no_enemies(self.game)
            elif action == "Flee":
                # self.combat_manager.attempt_flee()
                self.combat_manager.advance_turn()



    def handle_ability_select(self, keys, now):
        unit = self.combat_manager.get_current_unit()
        abilities = unit.abilities

        if now - self.cooldown >200:
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

            self.combat_manager.advance_turn()
            self.reset()
            self.mode = "action_menu"  # ✅ Return to action menu
            self.cooldown = now

            self.combat_manager.end_combat_if_no_enemies(self.game)


        elif keys[pygame.K_ESCAPE]:
            self.reset()
            self.mode = "action_menu"  # ✅ Return to action menu on cancel
            self.cooldown = now

    def reset(self):
        self.mode = "action_menu"
        self.pending_action = None
        self.selected_target_index = 0
        self.selected_ability = None
        self.cooldown = 0

        self.action_menu.ability_menu_visible = False
        self.action_menu.abilities = []

