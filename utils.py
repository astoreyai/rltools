# utils.py
import imageio
import numpy as np
import os

def create_gif(env, model, max_steps=200, seed=1, folder='gifs', filename='agent_behavior'):
    obs = env.reset(seed=seed)
    images = []
    
    for _ in range(max_steps):
        action, _ = model.predict(obs)
        obs, _, done, _ = env.step(action)
        img = env.render(mode='rgb_array')
        images.append(img)
        if done:
            break

    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Save as GIF
    imageio.mimsave(f'{folder}/{filename}.gif', [np.array(img) for img in images], fps=30)

def evaluate(env, agent, episodes=50, max_steps=200, gamma=1.0, seed=1):
    """
    Evaluates a given agent in the specified environment.
    """
    total_rewards = []
    for ep in range(episodes):
        obs = env.reset(seed=seed)
        episode_reward = 0
        for _ in range(max_steps):
            action, _ = agent.predict(obs)
            obs, reward, done, info = env.step(action)
            episode_reward += reward
            if done:
                break
        total_rewards.append(episode_reward)

    avg_reward = np.mean(total_rewards)
    return avg_reward

def sb3_evaluation_curves(path='./logs/'):
    """
    Display training curves for SB3 models using evaluation logs.
    """
    # You can extend this function to parse and plot evaluation metrics
    pass
