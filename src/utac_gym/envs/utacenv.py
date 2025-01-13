import gymnasium as gym
from gymnasium import spaces
import numpy as np

import utac_gym
from utac_gym.core.types import Board, SubBoard
from .utils import cast_to_board

from utac_gym.core.gamestate import GameState


class UtacEnv(gym.Env):
    metadata = {"render_modes": ["text"]}

    def __init__(self, render_mode=None):
        # Observation space: 3 binary planes of 9x9
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(2, 9, 9), dtype=np.int8
        )

        # Action space: 81 possible moves (9x9 grid)
        self.action_space = spaces.Discrete(81)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.state: GameState = None

    def _get_obs(self):
        obs = self.state.get_obs()
        return np.array(obs).reshape(2, 9, 9)

    def _get_info(self):
        info = {
            "state": self.state,
        }

        return info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Initialize new game state
        self.state = GameState()

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        self.state.make_move(action)

        terminated = self.state.is_terminal()

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
