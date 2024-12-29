import utac
import random

game = utac.UtacState()

while not game.game_over:
    game.print()
    legal_moves = game.get_legal_moves_index()
    move = random.choice(legal_moves)
    game.make_move_index(move)

game.print()
