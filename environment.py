import numpy as np

DECK = range(1, 11)
ACTIONS = (HIT, STICK) = (0, 1)

DEALER_RANGE = range(1, 11) #dealer从一开始抽出牌，到player stick都没有新牌，player stick后无action也无state改变
PLAYER_RANGE = range(1, 22)


TERMINAL_STATE = "TERMINAL"
COLOR_PROBS = { 'red': 1/3, 'black': 2/3 }
COLOR_COEFFS = { 'red': -1, 'black': 1 }


def draw_card(color=None):
    value = np.random.choice(DECK)
    if color is None:
        colors, probs = zip(*COLOR_PROBS.items())
        color = np.random.choice(colors, p=probs)
    return { 'value': value, 'color': color }


def bust(x):
    return x < 1 or x > 21


class Easy21Env:
    def __init__(self):
        self.reset()

    def reset(self, dealer=None, player=None):
        if dealer is None:
            dealer = draw_card()['value']
        self.dealer = dealer
        if player is None:
            player = draw_card()['value']
        self.player = player

    def observe(self):
        if not (self.dealer in DEALER_RANGE and self.player in PLAYER_RANGE):
            return TERMINAL_STATE
        return np.array((self.dealer, self.player))

    def step(self, action, value=None, color=None):
        if action == HIT:
            if value is None and color is None:
                card = draw_card()
                self.player += COLOR_COEFFS[card['color']] * card['value']
            else:
                self.player += COLOR_COEFFS[color]* value

            if bust(self.player):
                next_state, reward = TERMINAL_STATE, -1
            else:
                next_state, reward = (self.dealer, self.player), 0
        elif action == STICK:
            while 0 < self.dealer < 16:
                card = draw_card()
                self.dealer += COLOR_COEFFS[card['color']] * card['value']

            next_state = TERMINAL_STATE
            if bust(self.dealer):
                reward = 1
            else:
                reward = int(self.player > self.dealer) - int(self.player < self.dealer)
        else:
            raise ValueError("Action not in action space")

        return np.array(next_state), reward

