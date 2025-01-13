import utac_gym
import random

game = utac_gym.GameState()

while not game.is_terminal():
    game.print()
    legal_moves = game.get_valid_moves()
    move = random.choice(legal_moves)
    game.make_move(move)

game.print()
