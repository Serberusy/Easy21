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
* Assumption: The game is played with an infinite deck of cards (i.e. cards are sampled with replacement)
