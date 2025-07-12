from dungeon_recruiter.units.unit import Unit

class CombatUnit(Unit):
    def __init__(self, unit):
        super().__init__(
            unit.name,
            unit.base_max_health,
            unit.base_max_mana,
            unit.base_attack,
            unit.base_defense
        )

        # Copy over equipped gear and properties
        self.weapon = unit.weapon
        self.armor = unit.armor
        self.abilities = unit.abilities
        self.level = unit.level

        self.update_stats()

        # Combat-specific state
        self.status_effects = []       # List of {name, turns, effect}
        self.acted_this_turn = False   # Has the unit already acted?
        self.is_player = hasattr(unit, "recruiting")  # True if player/recruit, False if enemy

    def start_turn(self):
        self.acted_this_turn = False
        self._process_status_effects()

    def apply_status_effect(self, name, effect_func, turns):
        """Apply a new status effect."""
        self.status_effects.append({
            "name": name,
            "turns": turns,
            "effect_func": effect_func
        })

    def _process_status_effects(self):
        for effect in self.status_effects:
            effect["effect_func"](self)
            effect["turns"] -= 1
        self.status_effects = [e for e in self.status_effects if e["turns"] > 0]

    def take_turn(self, target):
        # Placeholder basic logic
        if self.abilities:
            return self.attack(target)
        else:
            return f"{self.name} skips their turn."