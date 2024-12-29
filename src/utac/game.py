from .types import Board, SubBoard
from .utils import get_subboard, check_subboard_terminal, check_subboard_winner, move_to_index, print_board, index_to_move, subboard_coord_to_index, index_to_subboard_coord, index_to_board_coord

import numpy as np

from typing import Literal

class UtacState:
    def __init__(self, current_subboard_index: int = 4):
        self.boardX: Board = np.zeros((9, 9), dtype=np.bool_)
        self.boardO: Board = np.zeros((9, 9), dtype=np.bool_)

        self.main_boardX: SubBoard = np.zeros((3, 3), dtype=np.bool_)
        self.main_boardO: SubBoard = np.zeros((3, 3), dtype=np.bool_)
        self.main_boardDraw: SubBoard = np.zeros((3, 3), dtype=np.bool_)
        
        self.winner: Literal["X", "O", "Draw", "None"] = "None"
        self.current_player: Literal["X", "O"] = "X"
        self.game_over: bool = False

        self.current_subboard_index: int = current_subboard_index

    def __str__(self):
        return f"Current Player: {self.current_player}\nCurrent Subboard: {self.current_subboard_index}\nWinner: {self.winner}\nGame Over: {self.game_over}"
    
    def print(self) -> None:
        print_board(self.boardX, self.boardO)
        print(str(self))

    def get_legal_moves(self) -> list[tuple[int, int, int]]:
        legal_moves: list[tuple[int, int, int]] = []
        start = self.current_subboard_index
        stop = self.current_subboard_index + 1
        if self.current_subboard_index == -1:
            start = 0
            stop = 9
        for i in range(start, stop):
            subboardX: SubBoard = get_subboard(self.boardX, i)
            subboardO: SubBoard = get_subboard(self.boardO, i)
            if check_subboard_terminal(subboardX, subboardO):
                continue
            for j in range(3):
                for k in range(3):
                    if subboardX[j, k] == False and subboardO[j, k] == False:
                        legal_moves.append((i, j, k))
        return legal_moves
    
    def get_legal_moves_index(self) -> list[int]:
        return [move_to_index(move) for move in self.get_legal_moves()]
    
    def make_move(self, move: tuple[int, int, int]) -> None:
        move_index: int = move_to_index(move)
        subboard_index: int = move[0]
        subboard_move: tuple[int, int] = (move[1], move[2])
        board_coord: tuple[int, int] = index_to_board_coord(move_index)
        if self.current_player == "X":
            self.boardX[board_coord] = True
        else:
            self.boardO[board_coord] = True

        subboardX: SubBoard = get_subboard(self.boardX, subboard_index)
        subboardO: SubBoard = get_subboard(self.boardO, subboard_index)

        self.current_subboard_index = subboard_coord_to_index(subboard_move)

        if check_subboard_terminal(subboardX, subboardO):

            subboard_coord = index_to_subboard_coord(subboard_index)
            if check_subboard_winner(subboardX):
                self.main_boardX[subboard_coord] = True
            elif check_subboard_winner(subboardO):
                self.main_boardO[subboard_coord] = True
            else:
                self.main_boardDraw[subboard_coord] = True

        if check_subboard_winner(self.main_boardX):
            self.winner = "X"
            self.game_over = True
        elif check_subboard_winner(self.main_boardO):
            self.winner = "O"
            self.game_over = True
        else:
            merged_main_board: SubBoard = np.logical_or(np.logical_or(self.main_boardX, self.main_boardO), self.main_boardDraw)
            if np.all(merged_main_board == True):
                self.winner = "Draw"
                self.game_over = True

        self.current_player = "O" if self.current_player == "X" else "X"

        if check_subboard_terminal(get_subboard(self.boardX, self.current_subboard_index), get_subboard(self.boardO, self.current_subboard_index)):
            self.current_subboard_index = -1

    def make_move_index(self, move_index: int) -> None:
        move: tuple[int, int, int] = index_to_move(move_index)
        self.make_move(move)

