from dungeon_recruiter.game import Game
from game_state import GameState
from dungeon_recruiter.combat.combat_manager import CombatManager
from dungeon_recruiter.combat.combat_menu import PlayerActionMenu
from dungeon_recruiter.combat.combat_input_handler import CombatInputHandler

def initialize_game():
    game = Game()
    game.state = GameState.CHARACTER_SELECT

    combat_menu = PlayerActionMenu()
    combat_manager = CombatManager(game.party_manager.active_party, game.enemy_party)

    combat_input = CombatInputHandler(combat_manager, combat_menu, game)

    # Store references so they can be attached to the game object if needed
    game.combat_menu = combat_menu
    game.combat_manager = combat_manager
    game.combat_input_handler = combat_input

    return game