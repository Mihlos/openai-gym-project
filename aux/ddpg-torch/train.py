import gym
import torch
import numpy as np

import matplotlib.pyplot as plt

from ddpg_agent import Agent

env = gym.make('LunarLanderContinuous-v2')
#env = gym.make('BipedalWalker-v2')
#env = gym.make('BipedalWalkerHardcore-v2')

obs_len = env.observation_space.shape[0]
act_len = env.action_space.shape[0]

agent = Agent(state_size=obs_len, action_size=act_len, random_seed=0)

def ddpg(episodes, step, render, trained, noise):
    if trained:
        print('CARGANDO MODELOS...')
        agent.actor_local.load_state_dict(torch.load('checkpoint_actor.pth', map_location="cpu"))
        agent.critic_local.load_state_dict(torch.load('checkpoint_critic.pth', map_location="cpu"))
        agent.actor_target.load_state_dict(torch.load('checkpoint_actor.pth', map_location="cpu"))
        agent.critic_target.load_state_dict(torch.load('checkpoint_critic.pth', map_location="cpu"))

    reward_list = []

    for i in range(episodes):
        obs = env.reset()
        score = 0
        for t in range(step):
            if render:
                env.render()
            action = agent.act(obs, noise)
            next_state, reward, done, info = env.step(action[0])
            #agent.step(obs, action, reward, next_state, done)
            # squeeze elimina una dimension del array.
            obs = next_state.squeeze()
            score += reward

            if done:
                print('Reward: {} | Episode: {}/{}'.format(score, i, episodes))
                break

        reward_list.append(score)

        if score >= 250:
            print('Task Solved')
            torch.save(agent.actor_local.state_dict(), 'checkpoint_actor_solved'+score+'.pth')
            torch.save(agent.critic_local.state_dict(), 'checkpoint_critic_solved'+score+'.pth')
            torch.save(agent.actor_target.state_dict(), 'checkpoint_actor_t_solved'+score+'.pth')
            torch.save(agent.critic_target.state_dict(), 'checkpoint_critic_t_solved'+score+'.pth')
            break

    torch.save(agent.actor_local.state_dict(), 'checkpoint_actor.pth')
    torch.save(agent.critic_local.state_dict(), 'checkpoint_critic.pth')
    torch.save(agent.actor_target.state_dict(), 'checkpoint_actor_t.pth')
    torch.save(agent.critic_target.state_dict(), 'checkpoint_critic_t.pth')

    print('Training saved...')
    return reward_list

def plot_scores(scores):
    fig = plt.figure()
    plt.plot(np.arange(1, len(scores) + 1), scores)
    plt.ylabel('Score')
    plt.xlabel('Episode #')
    plt.show()

if __name__=='__main__':
    scores = ddpg(episodes=100, step=2000, render=1 ,trained=1, noise=0)
    plot_scores(scores)
    