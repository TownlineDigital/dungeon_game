from dungeon_recruiter.combat.ability import Ability


player_abilities = {
    "Knight": [
        Ability(
            name="Shield Bash",
            mana_cost=3,
            damage=6,
            effect_type="damage",
            effect="Stun",
            description="Bashes enemy with shield, may stun for 1 turn."
        ),
        Ability(
            name="Defender's Resolve",
            mana_cost=4,
            damage=0,
            effect_type="buff",
            effect="Defense Up",
            description="Raises own defense significantly for 2 turns."
        ),
    ],
    "Mage": [
        Ability(
            name="Fireball",
            mana_cost=5,
            damage=12,
            effect_type="damage",
            description="A fiery projectile that deals area damage."
        ),
        Ability(
            name="Magic Barrier",
            mana_cost=4,
            damage=0,
            effect_type="buff",
            effect="Magic Resist Up",
            description="Increases magical resistance for 3 turns."
        ),
    ],
    "Rogue": [
        Ability(
            name="Backstab",
            mana_cost=3,
            damage=10,
            effect_type="damage",
            effect="Critical",
            description="Deals double damage if used first in combat."
        ),
        Ability(
            name="Smoke Bomb",
            mana_cost=2,
            damage=0,
            effect_type="buff",
            effect="Evasion Up",
            description="Increases evasion for 2 turns."
        ),
    ],
    "Cleric": [
        Ability(
            name="Heal",
            mana_cost=4,
            damage=0,
            healing=15,
            effect_type="heal",
            description="Restores health to an ally."
        ),
        Ability(
            name="Blessing",
            mana_cost=3,
            damage=0,
            effect_type="buff",
            effect="Attack Up",
            description="Boosts ally's attack power for 2 turns."
        ),
    ],
    "Barbarian": [
        Ability(
            name="Rage Strike",
            mana_cost=4,
            damage=14,
            effect_type="damage",
            effect="Self Damage",
            description="Deals heavy damage but hurts self slightly."
        ),
        Ability(
            name="War Cry",
            mana_cost=2,
            damage=0,
            effect_type="buff",
            effect="Team Attack Up",
            description="Raises the entire party's attack for 1 turn."
        ),
    ]
}