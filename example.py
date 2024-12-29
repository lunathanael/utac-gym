import utac

game = utac.UtacState()

while not game.game_over:
    game.print()
    move = game.get_legal_moves_index()[0]
    game.make_move_index(move)

game.print()
