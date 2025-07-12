class Gear:
    def __init__(self, name, gear_type, stat_boosts):
        self.name = name
        self.type = gear_type
        self.stats = stat_boosts

    def __str__(self):
        return self.name