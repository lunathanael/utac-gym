import numpy as np
from utac_gym.core.types import Board, SubBoard


def cast_to_board(subboard: SubBoard) -> Board:
    board = np.zeros((9, 9), dtype=np.int8)
    for i in range(3):
        for j in range(3):
            row_start = i * 3
            col_start = j * 3
            board[row_start : row_start + 3, col_start : col_start + 3] = (
                subboard[i, j]
            )
    return board