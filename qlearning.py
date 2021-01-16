import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import cm
from environment import Easy21Env, TERMINAL_STATE, DEALER_RANGE, PLAYER_RANGE, ACTIONS


EPSILON = 0.9  # 贪婪度 greedy
ALPHA = 0.001     # 学习率
GAMMA = 1    # 奖励递减值
MAX_EPISODES = 100000   # 最大回合数
STATE_SPACE_SHAPE = (len(DEALER_RANGE), len(PLAYER_RANGE), len(ACTIONS))


def epsilon_greedy_policy(Q, state, epsilon):
    dealer, player = state
    if np.random.rand() > epsilon:
        action = np.random.choice(ACTIONS)
    else:
        action = np.argmax(Q[dealer - 1, player - 1, :])
    return action


def learn():
    env = Easy21Env()
    Q = np.zeros(STATE_SPACE_SHAPE)

    for episode in range(MAX_EPISODES):
        print(episode)
        env.reset()
        state1 = env.observe()

        while state1 != TERMINAL_STATE:
            action1 = epsilon_greedy_policy(Q, state1, EPSILON)
            state2, reward = env.step(action1)

            dealer1, player1 = state1
            idx1 = (dealer1 - 1, player1 - 1, action1)
            Q1 = Q[idx1]

            if state2 != TERMINAL_STATE:
                dealer2, player2 = state2
                q_target = reward + GAMMA * Q[dealer2 - 1, player2 - 1, :].max()
            else:
                q_target = reward

            Q[idx1] += ALPHA * (q_target-Q1)
            state1 = state2

        if episode % 1000 == 0 or episode == MAX_EPISODES-1:   #每1000回合测试一次
            policy = np.argmax(Q, axis=2)
            rate = test(policy)
            f = open("testQ-e09-a0001.txt", "a")            #数据输出到文档
            f.write(str(episode) + "\t" + str(rate) + "\n")
            f.close()
    return Q


def create_surf_plot(X, Y, Z, fig_idx=1):
    fig = plt.figure(fig_idx)
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    return surf


def test(policy):
    env = Easy21Env()
    win = 0
    for i in range(10000):
        env.reset()
        state1 = env.observe()

        while True:
            d_s, p_s = state1
            action1 = policy[d_s - 1][p_s - 1]
            state2, reward = env.step(action1)
            if state2 == TERMINAL_STATE:
                break
            state1 = state2
        if reward == 1:
            win += 1
    return win / 10000


if __name__ == "__main__":
    Q = learn()
    V = np.max(Q, axis=2)
    policy = np.argmax(Q, axis=2)
    X, Y = np.mgrid[DEALER_RANGE, PLAYER_RANGE]

    surf = create_surf_plot(X, Y, V)        # 画三维图
    plt.title("V*")
    plt.ylabel('player sum', size=18)
    plt.xlabel('dealer showing', size=18)

    plt.figure(figsize=(11, 5))
    sns.heatmap(policy, linewidths=0.05, cmap='YlGnBu')         # 画policy表
    plt.show()

