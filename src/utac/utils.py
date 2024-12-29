from .types import Board, SubBoard

import numpy as np

from typing import Literal

def get_subboard(board: Board, index: int) -> SubBoard:
    row = (index // 3) * 3
    col = (index % 3) * 3
    return board[row:row+3, col:col+3]

def check_subboard_winner(subboard: SubBoard) -> bool:
    for row in range(3):
        if np.all(subboard[row, :] == True):
            return True
    
    for col in range(3):
        if np.all(subboard[:, col] == True):
            return True
    
    if np.all(np.diag(subboard) == True):
        return True
        
    if np.all(np.diag(np.fliplr(subboard)) == True):
        return True
    
    return False

def check_subboard_terminal(subboardX: SubBoard, subboardO: SubBoard) -> bool:
    merged_subboard: SubBoard = np.logical_or(subboardX, subboardO)
    return check_subboard_winner(subboardX) or check_subboard_winner(subboardO) or np.all(merged_subboard == True)

def move_to_index(move: tuple[int, int, int]) -> int:
    return (move[0] % 3 * 3) + (move[0] // 3 * 27) + move[1] * 9 + move[2]

def index_to_move(index: int) -> tuple[int, int, int]:
    subboard_index = (index % 9) // 3 + (index // 27) * 3
    row = (index // 9) % 3
    col = index % 3
    return (subboard_index, row, col)

def index_to_board_coord(index: int) -> tuple[int, int]:
    return (index // 9, index % 9)

def print_board(boardX: Board, boardO: Board) -> None:
    for i in range(9):
        if i % 3 == 0:
            print("-" * 25)
        print("|", end=" ")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print("X" if boardX[i,j] else "O" if boardO[i,j] else ".", end=" ")
        print("|")
    print("-" * 25)



def subboard_coord_to_index(coord: tuple[int, int]) -> int:
    return coord[0] * 3 + coord[1]

def index_to_subboard_coord(index: int) -> tuple[int, int]:
    return (index // 3, index % 3)


