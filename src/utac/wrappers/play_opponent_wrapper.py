import gymnasium as gym
from gymnasium import spaces
import numpy as np


class PlayOpponentWrapper(gym.Wrapper):
    """A wrapper that allows playing against an opponent."""
    
    def __init__(self, env: gym.Env, opponent=None):
        """Initialize the wrapper.
        
        Args:
            env: The environment to wrap
            opponent: A function that takes an observation and returns an action,
                     or None for human input
        """
        super().__init__(env)

        assert opponent is not None, "Opponent must be provided"
        self.opponent = opponent
        
    def reset(self, seed=None, options=None):
        observation, info = super().reset(seed=seed, options=options)

        if np.random.random() < 0.5:
            action = self.opponent.get_action(observation)
            observation, _, _, _, info = super().step(action)
        return observation, info
        
    def step(self, action):
        observation, reward, terminated, truncated, info = super().step(action)
        
        if not terminated and not truncated:
            action = self.opponent.get_action(observation)
            observation, reward, terminated, truncated, info = super().step(action)
            reward = -reward
        return observation, reward, terminated, truncated, info


class RandomOpponent:
    def get_action(self, observation):
        action_mask = observation[0].flatten()
        legal_moves_indices = np.where(action_mask == 1)[0]
        return np.random.choice(legal_moves_indices)

