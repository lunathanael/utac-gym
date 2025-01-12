import gymnasium as gym
from gymnasium import spaces
import numpy as np
import utac
from utac.core.types import Board, SubBoard
from .utils import cast_to_board
from utac.core.utils import move_to_index, index_to_board_coord


class UtacEnv(gym.Env):
    metadata = {"render_modes": ["text"]}

    def __init__(self, render_mode=None):
        # Observation space: 3 binary planes of 9x9
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(7, 9, 9), dtype=np.int8
        )

        # Action space: 81 possible moves (9x9 grid)
        self.action_space = spaces.Discrete(81)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.state: utac.UtacState = None

    def _get_obs(self):
        return self._get_features()
        # Convert UtacState to 3 binary planes
        boardX: Board = self.state.boardX.astype(np.int8)
        boardO: Board = self.state.boardO.astype(np.int8)

        current_subboard_index: int = self.state.current_subboard_index
        board_mask: Board = np.zeros((9, 9), dtype=np.int8)
        if current_subboard_index == -1:
            board_mask = np.ones((9, 9), dtype=np.int8)
        else:
            for i in range(3):
                for j in range(3):
                    move = (current_subboard_index, i, j)
                    move_index = move_to_index(move)
                    move_coord = index_to_board_coord(move_index)
                    board_mask[move_coord] = True

        if self.state.current_player == "O":
            boardX, boardO = boardO, boardX

        observation = np.stack([boardX, boardO, board_mask], axis=0)
        return observation

    def _get_features(self):
        # Convert UtacState to 3 binary planes
        boardX: Board = self.state.boardX.astype(np.int8)
        boardO: Board = self.state.boardO.astype(np.int8)
        main_boardX: SubBoard = self.state.main_boardX
        main_boardO: SubBoard = self.state.main_boardO
        main_boardDraw: SubBoard = self.state.main_boardDraw

        main_boardX = cast_to_board(main_boardX).astype(np.int8)
        main_boardO = cast_to_board(main_boardO).astype(np.int8)
        main_boardDraw = cast_to_board(main_boardDraw).astype(np.int8)

        current_subboard_index: int = self.state.current_subboard_index
        board_mask: Board = np.zeros((9, 9), dtype=np.int8)
        if current_subboard_index == -1:
            board_mask = np.ones((9, 9), dtype=np.int8)
        else:
            for i in range(3):
                for j in range(3):
                    move = (current_subboard_index, i, j)
                    move_index = move_to_index(move)
                    move_coord = index_to_board_coord(move_index)
                    board_mask[move_coord] = True

        action_mask = np.zeros((81,), dtype=np.int8)
        for action in self.state.get_legal_moves_index():
            action_mask[action] = 1
        action_mask = action_mask.reshape(9, 9)

        if self.state.current_player == "O":
            boardX, boardO = boardO, boardX
            main_boardX, main_boardO = main_boardO, main_boardX

        observation = np.stack(
            [action_mask, boardX, boardO, board_mask, main_boardX, main_boardO, main_boardDraw],
            axis=0,
        )
        return observation

    def _get_info(self):
        info = {
            "current_subboard_index": self.state.current_subboard_index,
            "current_player": self.state.current_player,
            "winner": self.state.winner,
            "game_over": self.state.game_over,
            "_legal_moves": self.state.get_legal_moves(),
            "legal_move_indices": self.state.get_legal_moves_index(),
        }

        if self.state.game_over:
            if self.state.winner == "Draw":
                raw_r = 0
            else:
                raw_r = -1 if self.state.winner == "O" else 1

            info["final_info"] = {
                "r" : self.score,
                "l" : self.length,
                "raw_r" : raw_r
            }

        return info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Initialize new game state
        self.state = utac.UtacState(current_subboard_index=-1)

        if np.random.random() < 0.5:
            self.state.make_move_index(np.random.choice(self.state.get_legal_moves_index(), 1)[0])

        observation = self._get_obs()
        info = self._get_info()

        self.score = 0
        self.length = 0

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        current_player = self.state.current_player
        try:
            self.state.make_move_index(action)
        except ValueError:
            self.score -= 5000
            self.state.game_over = True
            self.state.winner = "O" if current_player == "X" else "X"
            return self._get_obs(), -5000, True, False, self._get_info()
        

        if not self.state.game_over:
            self.state.make_move_index(np.random.choice(self.state.get_legal_moves_index(), 1)[0])

        # Check if game is over
        terminated = self.state.game_over

        # Reward: 1 for win, 0 for ongoing, -1 for invalid/loss
        reward: int
        if not terminated:
            reward = 0
        elif self.state.winner == current_player:
            reward = 1000
        elif self.state.winner == "Draw":
            reward = 0
        else:
            reward = -1000
        self.score += reward
        self.length += 1

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def apply_move_index(self, move_index: int):
        self.state.make_move_index(move_index)

    def render(self):
        if self.render_mode == "text":
            self.state.print()

    def _render_frame(self):
        # Implement rendering logic here if needed
        pass

    def close(self):
        pass

    def get_legal_actions(self):
        return self.state.get_legal_moves()

    def is_terminal(self):
        return self.state.game_over

    def clone(self):
        clone = UtacEnv()
        clone.state = self.state.copy()
        return clone

    @property
    def current_player(self):
        return self.state.current_player == "X"

    def get_reward(self, current_player: int):
        players = ["O", "X"]
        if self.state.winner not in ("X", "O"):
            return 0
        if self.state.winner == players[current_player]:
            return 1
        return -1
