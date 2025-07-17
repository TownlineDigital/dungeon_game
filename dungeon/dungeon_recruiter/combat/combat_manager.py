import random
from game_state import GameState

class CombatManager:
    def __init__(self, party_manager, enemy_party):
        self.party_manager = party_manager
        self.player_party = party_manager.active_party
        self.enemy_party = enemy_party
        self.all_units = player_party + enemy_party

        # Sort by initiative (speed)
        self.turn_order = sorted(self.all_units, key=lambda u: u.speed, reverse=True)
        self.current_turn_index = 0
        self.battle_log = []

        print("[COMBAT] Turn order:")
        for unit in self.turn_order:
            print(f" - {unit.name} (Speed: {unit.speed})")

    def get_current_unit(self):
        if self.turn_order:
            return self.turn_order[self.current_turn_index]
        return None

    def advance_turn(self):
        """
        Move to the next living unit's turn.
        """
        start_index = self.current_turn_index
        while True:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
            current = self.get_current_unit()
            if current and current.current_health > 0:
                break
            if self.current_turn_index == start_index:
                break

    def is_battle_over(self):
        """
        Check if either party has been wiped out.
        """
        players_alive = any(u.current_health > 0 for u in self.player_party)
        enemies_alive = any(u.current_health > 0 for u in self.enemy_party)
        print(f"[Check] Players alive: {players_alive}, Enemies alive: {enemies_alive}")
        return not players_alive or not enemies_alive

    def get_living_targets(self, party):
        return [u for u in party if u.current_health > 0]

    def perform_attack(self, attacker, target):
        if attacker.current_health <= 0:
            return
        damage = max(1, attacker.attack_val - target.defense_val)
        target.current_health -= damage
        target.current_health = max(0, target.current_health)
        result = f"{attacker.name} hits {target.name} for {damage} damage!"
        self.battle_log.append(result)
        print(result)

    def use_ability(self, user, ability, target):
        """
        Executes a combat ability.
        """
        if user.current_health <= 0:
            return

        if user.current_mana < ability.mana_cost:
            self.battle_log.append(f"{user.name} tried to use {ability.name}, but didn't have enough mana!")
            print(f"[ABILITY] {user.name} lacks mana for {ability.name}")
            return

        user.current_mana -= ability.mana_cost

        if ability.effect_type == "damage":
            damage = max(1, ability.damage + user.attack_val - target.defense_val)
            target.current_health = max(0, target.current_health - damage)
            self.battle_log.append(f"{user.name} used {ability.name} on {target.name} for {damage} damage!")
            print(f"[ABILITY] {user.name} used {ability.name} on {target.name} ({damage} dmg)")

        elif ability.effect_type == "heal":
            healing = ability.power
            target.current_health = min(target.max_health, target.current_health + healing)
            self.battle_log.append(f"{user.name} used {ability.name} to heal {target.name} for {healing}!")
            print(f"[ABILITY] {user.name} healed {target.name} with {ability.name} ({healing} hp)")

        # Add more types: buff, debuff, revive, etc.

        self.advance_turn()

    def attempt_recruit(self, player, target, game):
        """
        Attempt to recruit a weakened enemy and manage where they go.
        """
        if not target or target.current_health <= 0:
            msg = "You can't recruit that enemy."
            self.battle_log.append(msg)
            print(f"[Recruit] {msg}")
            self.advance_turn()
            return

        if target.current_health > target.max_health * 0.5:
            msg = f"{target.name} is too strong to recruit!"
            self.battle_log.append(msg)
            print(f"[Recruit] {msg}")
            self.advance_turn()
            return

        chance = min(90, 30 + player.recruiting * 5)
        roll = random.randint(1, 100)
        print(f"[Recruit] Roll: {roll}, Chance: {chance}")

        if roll <= chance:
            msg = f"{player.name} successfully recruited {target.name}!"
            self.battle_log.append(msg)
            print(f"[Recruit] {msg}")

            # Remove from combat
            if target in self.enemy_party:
                self.enemy_party.remove(target)
            if target in self.turn_order:
                self.turn_order.remove(target)

            # 🔁 Always use clone:
            new_ally = target.clone()
            game.party_manager.add_unit(new_ally)

            if game.party_manager.can_add_to_active():
                game.party_manager.add_to_active(new_ally)
                print(f"[Recruit] {target.name} added to active party.")
            else:
                game.party_manager.add_to_sanctuary(new_ally)
                print(f"[Recruit] {target.name} added to sanctuary.")
        else:
            msg = f"{player.name}'s recruit attempt failed!"
            self.battle_log.append(msg)
            print(f"[Recruit] {msg}")

        self.advance_turn()

    # def attempt_recruit(self, player, target, game):
    #     """
    #     Attempt to recruit a weakened enemy and manage where they go.
    #     """
    #     if not target or target.current_health <= 0:
    #         msg = "You can't recruit that enemy."
    #         self.battle_log.append(msg)
    #         print(f"[Recruit] {msg}")
    #         self.advance_turn()
    #         return
    #
    #     if target.current_health > target.max_health * 0.5:
    #         msg = f"{target.name} is too strong to recruit!"
    #         self.battle_log.append(msg)
    #         print(f"[Recruit] {msg}")
    #         self.advance_turn()
    #         return
    #
    #     chance = min(90, 30 + player.recruiting * 5)
    #     roll = random.randint(1, 100)
    #     print(f"[Recruit] Roll: {roll}, Chance: {chance}")
    #
    #     if roll <= chance:
    #         msg = f"{player.name} successfully recruited {target.name}!"
    #         self.battle_log.append(msg)
    #         print(f"[Recruit] {msg}")
    #
    #         # Remove from combat
    #         if target in self.enemy_party:
    #             self.enemy_party.remove(target)
    #         if target in self.turn_order:
    #             self.turn_order.remove(target)
    #
    #         # Add to active party or sanctuary
    #         if len(game.active_party) < 3:  # adjust team size limit as needed
    #             new_ally = target.clone()
    #             game.active_party.append(new_ally)
    #             print(f"[Recruit] {target.name} added to active party.")
    #         else:
    #             game.sanctuary_roster.append(target)
    #             print(f"[Recruit] {target.name} added to sanctuary.")
    #
    #     else:
    #         msg = f"{player.name}'s recruit attempt failed!"
    #         self.battle_log.append(msg)
    #         print(f"[Recruit] {msg}")
    #
    #     self.advance_turn()

    def retreat(self, player):
        """
        Attempt to flee from combat.
        """
        flee_chance = min(85, 30 + player.speed * 5)
        roll = random.randint(1, 100)
        if roll <= flee_chance:
            msg = f"{player.name} successfully retreated from battle!"
            self.battle_log.append(msg)
            print(msg)
            return True
        else:
            msg = f"{player.name} tried to flee but failed!"
            self.battle_log.append(msg)
            print(msg)
            return False

    def take_turn(self):
        """
        Executes the current unit's turn.
        For enemies: pick a random target and attack.
        For players: wait for input via menu.
        """
        current = self.get_current_unit()
        if not current or current.current_health <= 0:
            self.advance_turn()
            return

        if current in self.enemy_party:
            targets = self.get_living_targets(self.player_party)
            if targets:
                target = random.choice(targets)
                self.perform_attack(current, target)
                self.advance_turn()
        else:
            print(f"[ACTION] Waiting for player action: {current.name}")
            # UI-driven input should handle player's choice (attack, ability, etc.)

    def end_combat_if_no_enemies(self, game):
        living_enemies = self.get_living_targets(self.enemy_party)

        if not living_enemies:
            print("[Combat] All enemies defeated!")

            # Calculate total XP (simple example)
            total_xp = sum(enemy.max_health for enemy in self.enemy_party)  # or any logic you prefer
            # game.player.xp += total_xp
            print(f"[Combat] {game.player.name} gained {total_xp} XP!")

            # Optional: Level-up check here

            # Reset combat-related state
            self.enemy_party.clear()
            self.turn_order.clear()
            self.battle_log.clear()
            game.player_party = game.party_manager.refresh_combat_party()


            # Return to exploration
            game.state = GameState.EXPLORATION
            game.set_notification("Combat ended. Back to exploring!")