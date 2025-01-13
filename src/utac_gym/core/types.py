from typing import List, TYPE_CHECKING
from dataclasses import dataclass

@dataclass
class GAMESTATE:
    """Type hints for the C++ GAMESTATE struct bindings"""
    occ: List[int]  # Array of 9 occupancy bitboards for each sub-board
    board: List[int]  # Array of 9 board state bitboards for each sub-board
    game_occ: int  # Game occupancy bitboard
    main_occ: int  # Main game occupancy bitboard
    main_board: int  # Main game board state bitboard
    side: int  # Current player/side to move (initialized to 1)
    last_square: int  # Last played square (initialized to -1)

if not TYPE_CHECKING:
    from utac_gym._core import GAMESTATE as CPPGAMESTATE
    GAMESTATE = CPPGAMESTATE

__all__ = ["GAMESTATE"]
