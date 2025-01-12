import numpy as np
from utac.core.types import Board, SubBoard


def cast_to_board(subboard: SubBoard) -> Board:
    board = np.zeros((9, 9), dtype=np.int8)
    for i in range(3):
        for j in range(3):
            if subboard.board[i, j] != 0:
                row_start = subboard.start_row + (i * 3)
                col_start = subboard.start_col + (j * 3)
                board[row_start : row_start + 3, col_start : col_start + 3] = (
                    subboard.board[i, j]
                )
    return board