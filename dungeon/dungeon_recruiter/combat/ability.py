class Ability:
    def __init__(self, name, mana_cost, damage=0, description="", effect=None, healing=0):
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage  # Direct damage amount
        self.description = description
        self.effect = effect  # e.g. "Poison", "Slow", etc.
        self.healing = healing  # Amount of HP to heal

    def __repr__(self):
        return f"<Ability {self.name} ({self.effect_type}, {self.power} MP:{self.mana_cost})>"