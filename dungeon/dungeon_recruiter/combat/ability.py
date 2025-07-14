class Ability:
    def __init__(self, name, mana_cost, damage=0, description="", effect=None, effect_type=None, healing=0):
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage  # Direct damage amount
        self.description = description
        self.effect = effect  # e.g. "Poison", "Slow", etc.
        self.effect_type = effect_type
        self.healing = healing  # Amount of HP to heal

    def __repr__(self):
        return f"<Ability {self.name} (DMG: {self.damage}, Effect: {self.effect}, Type: {self.effect_type}, Heal: {self.healing}, MP: {self.mana_cost})>"
