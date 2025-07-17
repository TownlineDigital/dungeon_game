class PartyManager:
    def __init__(self):
        self.active_party = []
        self.sanctuary = []
        self.max_active_size = 3

    def add_unit(self, unit):
        if len(self.active_party) < self.max_active_size:
            self.active_party.append(unit)
            return "active"
        else:
            unit.current_health = unit.max_health
            unit.current_mana = unit.max_mana
            self.sanctuary.append(unit)
            return "sanctuary"

    def remove_unit(self, unit):
        if unit in self.active_party:
            self.active_party.remove(unit)
        if unit in self.sanctuary:
            self.sanctuary.remove(unit)

    def get_all_unity(self):
        return self.active_party + self.sanctuary

    def clone_team_for_combat(self):
        return [unity.clone() for unity in self.active_party]