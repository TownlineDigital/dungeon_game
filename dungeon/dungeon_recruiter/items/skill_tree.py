class Skill:
    def __init__(self, name, description, effects):
        self.name = name
        self.description = description
        self.effects = effects
        self.unlocked = False

    def apply(self, unit):
        if self.unlocked:
            return
        for stat, value in self.effects.items():
            base_stat = f"base_{stat}"
            setattr(unit, base_stat, getattr(unit, base_stat) + value)
        unit.update_stats()
        self.unlocked = True


class SkillTree:
    def __init__(self, rarity):
        self.skills = []
        if rarity == "Common":
            self.skills.append(Skill("Toughness I", "+15 HP", {"max_health": 15}))
        elif rarity == "Elite":
            self.skills.append(Skill("Toughness II", "+30 HP", {"max_health": 30}))
            self.skills.append(Skill("Strength I", "+5 ATK", {"attack": 5}))
