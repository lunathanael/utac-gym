import gymnasium as gym
import utac_gym
from utac_gym.wrappers import PlayOpponentWrapper, RandomOpponent
import random

env = gym.make("utac-v0", render_mode="text")
env = PlayOpponentWrapper(env, opponent=RandomOpponent())
observation, info = env.reset()

terminated = False
truncated = False

while not (terminated or truncated):
    # Random agent
    legal_moves_indices = info["legal_move_indices"]
    action = random.choice(legal_moves_indices)
    
    # Step environment
    observation, reward, terminated, truncated, info = env.step(action)
    
    # Render the game state
    env.render()

env.close()
