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
        current_player = self.state.current_player
        self.state.make_move(action)

        terminated = self.state.is_terminal()

        # Reward: 1 for win, 0 for ongoing, -1 for invalid/loss
        reward: int
        winner = self.state.terminal_value()
        if not terminated:
            reward = 0
        elif winner == 0:
            reward = 1e-4
        else:
            reward = 1 if winner == current_player else -1

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "text":
            self.state.print()

    def _render_frame(self):
        # Implement rendering logic here if needed
        pass

    def close(self):
        pass
