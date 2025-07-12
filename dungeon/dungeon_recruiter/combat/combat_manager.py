import random

class CombatManager:
    def __init__(self, player_party, enemy_party):
        self.player_party = player_party
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
            damage = max(1, ability.power + user.attack - target.defense)
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

    def attempt_recruit(self, player, target):
        """
        Attempt to recruit a weakened enemy.
        """
        if target.current_health > target.max_health * 0.5:
            msg = f"{target.name} is too strong to recruit!"
            self.battle_log.append(msg)
            print(msg)
            return False

        chance = min(90, 30 + player.recruiting * 5)
        roll = random.randint(1, 100)
        if roll <= chance:
            msg = f"{player.name} successfully recruited {target.name}!"
            self.battle_log.append(msg)
            print(msg)
            return True
        else:
            msg = f"{player.name}'s recruit attempt failed!"
            self.battle_log.append(msg)
            print(msg)
            return False

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

