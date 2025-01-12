import gymnasium as gym
import numpy as np


class InfoWrapper(gym.Wrapper):
    """
    A wrapper that adds additional information to the info dictionary.
    Follows the standard gymnasium wrapper pattern.
    """

    def __init__(self, env):
        """Initialize the wrapper with a UtacEnv instance."""
        super().__init__(env)

    def _get_extended_info(self, info):
        """Add additional information to the info dictionary."""
        # Get the main boards status
        main_boardX = self.env.state.main_boardX
        main_boardO = self.env.state.main_boardO
        main_boardDraw = self.env.state.main_boardDraw

        # Count subboards won by each player and draws
        x_subboards = np.sum(main_boardX)
        o_subboards = np.sum(main_boardO)
        drawn_subboards = np.sum(main_boardDraw)

        # Add new information to the info dictionary
        extended_info = {
            **info,  # Include all original info
            "subboards_won_X": int(x_subboards),
            "subboards_won_O": int(o_subboards),
            "subboards_drawn": int(drawn_subboards),
            "remaining_subboards": 9 - (x_subboards + o_subboards + drawn_subboards),
        }
        
        return extended_info

    def reset(self, seed=None, options=None):
        """Reset the environment and add extended info."""
        obs, info = self.env.reset(seed=seed, options=options)
        return obs, self._get_extended_info(info)

    def step(self, action):
        """Step the environment and add extended info."""
        obs, reward, terminated, truncated, info = self.env.step(action)
        return obs, reward, terminated, truncated, self._get_extended_info(info) 