import gymnasium as gym
import utac
import random

env = gym.make("utac-v0", render_mode="text")
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
