# Easy21
Implementing Easy21 with Q-learning and policy iteration.

## Environment introduction
The rule the game Easy21 is defined as follows:
* Each draw from the from the deck results in a value between 1 and 10 (uniformly distributed) with a color of red (probability 1/3) or black (probability 2/3).
* At the start of the game both the player and the dealer draw one black card.
* Each turn the player may either stick or hit. If the player hits then he/she draws another card from the deck. If the player sticks he/she receives no further cards.
* The values of the player's cards are added (black cards) or subtracted (red cards). If the player's sum exceeds 21, or bec omes less than 1, then he/she goes “bust" and loses the game (reward 1).
* If the player sticks then the dealer starts taking turns. The dealer always sticks on any sum of 16 or greater, and hits otherwise. If the dealer goes “bust”, then the player wins (reward+1); Otherwise the outcome and reward is
computed as follows: the player wins (reward+1) if player’s sum is larger than the dealer’s the dealer’s sum; the player loses (reward sum; the player loses (reward --1) if the player’s sum is smaller 1) if the player’s sum is smaller than the dealer’sthan the dealer’s sum; the reward is 0 if the sum; the reward is 0 if the two sums are the same.two sums are the same.
* Assumption: The game is played with an infinite deck of cards (i.e. cards are sampled with replacement). 

## Q-learning
The Q-learning algorithm is a value-based off-policy algorithm in reinforcement learning. Its essence is to obtain a Q table through learning. Q table is Q(state,action), which reflects the expectation of gaining benefits by taking action actions under a certain state line. The environment will return the corresponding reward R based on the agent's action feedback, so the main idea of the algorithm is to construct a Q-table to store the Q value of State and Action, and then select the action that can obtain the greatest benefit based on the Q value.
Besides, ε-greedy is used to make the agent choose the action which results in a larger Q value most time and otherwise, randomly choose an action.

The episode is set as 10000. By experiments, when ε is set as 0.8 and learning rate α is set as 0.001, the winning rate reaches the highest.

The optimal state-value function is as follows.

![image](https://github.com/Serberusy/Easy21/blob/main/img/e08-a001-1.png)

The policy table is as follows(the yellow block presents hit, and the blue block presents stick).

![image](https://github.com/Serberusy/Easy21/blob/main/img/e08-a001-2.png)

## Policy Iteration
The key of the strategy iteration algorithm is to update the value function of each state through continuous trials to achieve the purpose of selecting actions based on the value function. For each state, its value represents how large the possiblity of winning in the current state is. If the state value is large, choosing an action from another state and transferring to that state is a good choice, otherwise it will be far from the ideal result.

The strategy iteration algorithm is mainly composed of two parts: strategy evaluation and strategy improvement. The value function of the state will be updated in the process of strategy evaluation. Starting from an initial strategy, the strategy is continuously evaluated, improved, re-evaluated, and improved until the strategy converges.

Set the reward descending rate γ as 0.15, the optimal state-value function is as follows.

And the policy table is as follows.
