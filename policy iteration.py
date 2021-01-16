import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from environment import Easy21Env, ACTIONS,DECK,COLOR_PROBS,TERMINAL_STATE, draw_card,DEALER_RANGE, PLAYER_RANGE

COLOR = ("red","black")

MAX_EPISODES = 1000

GAMMA = 1
THETA = 0.2


class PolicyIteration:
    def __init__(self, env):
        self.env = env

    def policy_evaluation(self, policy):
        V = np.zeros((len(DEALER_RANGE), len(PLAYER_RANGE)))

        delta = float("inf")

        while delta > THETA:
            delta = 0
            for d_s in DEALER_RANGE:
                for p_s in PLAYER_RANGE:
                    v = V[d_s-1][p_s-1]
                    V[d_s - 1][p_s - 1]=0
                    action1 = policy[d_s-1][p_s-1]

                    if action1==0:      #继续抽牌，以下为所有可能抽到的牌情况
                        for color in COLOR:
                            for value in DECK:
                                self.env.reset(d_s, p_s)
                                state2, reward = self.env.step(action1, value, color)
                                if state2 == TERMINAL_STATE:
                                    V_s = 0
                                else:
                                    V_s = V[state2[0] - 1][state2[1] - 1]
                                V[d_s - 1][p_s - 1] += 0.1 * COLOR_PROBS[color]*(reward + GAMMA * V_s)

                    elif action1 == 1:           #stick,不再抽牌
                        tmp = 0
                        for i in range(500):
                            env.reset(d_s, p_s)
                            state2, reward = self.env.step(action1)
                            tmp += reward
                        V[d_s - 1][p_s - 1] = tmp/500
                    delta = max(delta, abs(v - V[d_s - 1][p_s - 1]))
            print(delta)

        return V

    def next_best_action(self, dealer_state, player_state, V):
        action_values = np.zeros(len(ACTIONS))
        #hit
        for color in COLOR:
            for value in DECK:
                self.env.reset(dealer_state, player_state)
                state2, reward = self.env.step(0, value, color)
                if state2 == TERMINAL_STATE:
                    V_s = 0
                else:
                    V_s = V[state2[0] - 1][state2[1] - 1]
                action_values[0] += 0.1 * COLOR_PROBS[color]*(reward + GAMMA * V_s)

        #stick
        tmp = 0
        for i in range(500):
            env.reset(dealer_state, player_state)
            state2, reward = self.env.step(1)
            tmp += reward
        action_values[1] = tmp/500
        return np.argmax(action_values)

    def policy_improvement(self):
        policy = np.zeros((len(DEALER_RANGE), len(PLAYER_RANGE)))
        for i in DEALER_RANGE:
            for j in PLAYER_RANGE:
                policy[i-1][j-1] = np.random.choice(ACTIONS)

        is_stable = False
        episode = 0

        while episode< MAX_EPISODES:
            is_stable = True
            V = self.policy_evaluation(policy)

            for d_s in DEALER_RANGE:
                for p_s in PLAYER_RANGE:
                    old_action = policy[d_s-1][p_s-1]
                    best_action = self.next_best_action(d_s, p_s, V)
                    policy[d_s-1][p_s-1] = best_action
                    if old_action != best_action:
                        is_stable = False
            episode += 1
            print(episode)
            rate = self.test(policy)
            f = open("testPI02-1.txt", "a")                 #数据写入文档方便分析
            f.write(str(episode)+"\t"+str(rate)+"\n")
            f.close()
            if is_stable:
                break
        return policy, V

    def test(self, policy):
        win = 0
        for i in range(10000):
            self.env.reset()
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
            # total_reward += reward
        return win / 10000


def create_surf_plot(X, Y, Z, fig_idx=1):
    fig = plt.figure(fig_idx)
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    return surf


if __name__ == "__main__":
    env = Easy21Env()
    agent = PolicyIteration(env)
    policy, V = agent.policy_improvement()

    X, Y = np.mgrid[DEALER_RANGE, PLAYER_RANGE]

    surf = create_surf_plot(X, Y, V)            #画三维图
    plt.title("V")
    plt.ylabel('player sum', size=18)
    plt.xlabel('dealer showing', size=18)

    plt.figure(figsize=(11, 5))         #画policy表
    sns.heatmap(policy, linewidths=0.05, cmap='YlGnBu')

    plt.show()

