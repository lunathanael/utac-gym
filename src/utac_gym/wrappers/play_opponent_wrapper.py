import gymnasium as gym
from gymnasium import spaces
import numpy as np
import torch

from utac_gym.core import UtacState


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
            observation = np.expand_dims(observation, axis=0).astype(np.float32)
            observation = torch.tensor(observation)
            action = self.opponent.get_action(observation, info=info)
            action = int(action)
            observation, _, _, _, info = super().step(action)

        self.score = 0
        return observation, info
        
    def step(self, action):
        observation, reward, terminated, truncated, info = super().step(action)
        if not terminated and not truncated:
            observation = np.expand_dims(observation, axis=0).astype(np.float32)
            observation = torch.tensor(observation)
            action = self.opponent.get_action(observation, info=info)
            action = int(action)
            observation, reward, terminated, truncated, info = super().step(action)
            reward = -reward

        self.score += reward
        if "final_info" in info:
            info["final_info"]["r"] = self.score
        return observation, reward, terminated, truncated, info


class RandomOpponent:
    def get_action(self, observation, info):
        action_mask = info["legal_move_indices"]
        return np.random.choice(action_mask)

class MCTSNode:
    def __init__(self, state: UtacState, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = {}
        self.visits = 0
        self.value = 0.0
        self.untried_actions = state.get_legal_moves_index()

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def select_child(self, c_param=1.414):
        # UCB1 formula for node selection
        return max(self.children.values(),
                  key=lambda child: child.value / (child.visits + 1e-8) +
                  c_param * np.sqrt(np.log(self.visits + 1) / (child.visits + 1e-8)))

class MCTSOpponent:
    def __init__(self, num_simulations=10, num_rollouts=10):
        self.num_simulations = num_simulations
        self.num_rollouts = num_rollouts

    def get_action(self, observation, info):
        root_state: UtacState = info["state"].copy()
        root = MCTSNode(root_state)

        for _ in range(self.num_simulations):
            node = root
            state = root_state.copy()

            # Selection
            while not state.game_over and node.is_fully_expanded():
                node = node.select_child()
                state.make_move_index(node.parent_action)

            # Expansion
            if not state.game_over and node.untried_actions:
                action = np.random.choice(node.untried_actions)
                node.untried_actions.remove(action)
                state.make_move_index(action)
                node = MCTSNode(state.copy(), parent=node, parent_action=action)
                node.parent.children[action] = node

            # Simulation
            value = 0
            for _ in range(self.num_rollouts):
                state_for_rollout = state.copy()
                while not state_for_rollout.game_over:
                    possible_moves = state_for_rollout.get_legal_moves_index()
                    action = np.random.choice(possible_moves)
                    state_for_rollout.make_move_index(action)
                if state_for_rollout.winner == root_state.current_player:
                    value += 1
                elif state_for_rollout.winner == "Draw":
                    value += 0.5
            value = value / self.num_rollouts

            # Backpropagation
            while node is not None:
                node.visits += 1
                node.value += value
                node = node.parent

        # Choose the action with the most visits
        return max(root.children.items(), 
                  key=lambda item: item[1].visits)[0]