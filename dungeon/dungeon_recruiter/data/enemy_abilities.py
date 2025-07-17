from dungeon_recruiter.combat.ability import Ability

enemy_abilities = {
    "Slime": [
        Ability(
            name="Slap",
            mana_cost=0,
            damage=5,
            description="A weak but bouncy slap."
        ),
        Ability(
            name="Sticky Goo",
            mana_cost=3,
            damage=0,
            effect="Slow",
            description="Reduces the target’s speed for 3 turns."
        ),
        Ability(
            name="Gelatinous Shield",
            mana_cost=4,
            damage=0,
            effect="Defense Up",
            description="Raises defense for 2 turns."
        ),
    ],
    "Dark Mage": [
        Ability(
            name="Shadow Bolt",
            mana_cost=5,
            damage=15,
            description="Launches a bolt of dark energy."
        ),
        Ability(
            name="Weaken",
            mana_cost=4,
            damage=0,
            effect="Attack Down",
            description="Reduces the target's attack for 3 turns."
        ),
        Ability(
            name="Drain Life",
            mana_cost=6,
            damage=10,
            healing=5,
            description="Deals damage and heals for half the damage dealt."
        ),
    ],
    "Goblin": [
        Ability(
            name="Slash",
            mana_cost=2,
            damage=10,
            description="A wild slash with a rusty dagger."
        ),
        Ability(
            name="Poison Dagger",
            mana_cost=4,
            damage=6,
            effect="Poison",
            description="Inflicts poison for 3 turns."
        ),
        Ability(
            name="Taunt",
            mana_cost=2,
            damage=0,
            effect="Aggro",
            description="Forces target to attack the goblin next turn."
        ),
    ]
}

print(enemy_abilities["Goblin"])