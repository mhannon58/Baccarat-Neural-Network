import baccarat_deck as bac_deck
from gym import Env
from gym import spaces
import numpy as np
import random


class BaccaratEnv(Env):
    def __init__(self):
        self.deck = bac_deck.bac_deck(4)
        self.action_space = spaces.Dict({"action": spaces.Discrete(3), "stake": spaces.Discrete(9, start = 1)})
        self.observation_space = spaces.Sequence(spaces.Discrete(3))
        self.deck = bac_deck.bac_deck(4)
        self.balance = 5000
        self.state = tuple()
        
    
    def get_obs(self):
        return spaces.Dict({"prev_output": self.prev_grid})

    def reset(self, seed = None, option = None):
        super().reset(seed=seed)

        self.deck = bac_deck.bac_deck(4)
        self.deck.shuffle_deck()

        self.state = tuple()
        self.state = pad_sequence(self.state)
        self.balance = 5000

        return self.state, self.balance

    def step(self, action):

        if type(action) == int:
            a = int(action/9)
            b = action%9 + 1
            result, reward = bet_and_play(self.deck, a, b * 100)
        else:
            result, reward = bet_and_play(self.deck, action["action"], action["stake"] * 100)


        self.balance += reward

        terminated = False
        if self.balance < 0 or  self.balance > 10000 or len(self.deck.deck) < 16:
            terminated = True

        result = (result,)
        self.state = self.state[1:] + result

        return self.state, reward, terminated, self.balance
    
    def render(self):
        pass

    def close(self):
        pass


tableu = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1], 
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], 
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0], 
        [0 ,0 ,0 ,0 ,0, 0, 1, 1, 0, 0], 
        [0 ,0 ,0 ,0 ,0, 0, 0, 0, 0 ,0]]


def pad_sequence(input):
    while len(input) < 10:
        input = input + (-1,)
    
    return input

def print_hands(b, b_val, p, p_val):
    for e in b:
        print(e.name)
    print(b_val)
    for e in p:
        print(e.name)
    print(p_val)
    print("\n")


def play_hand(myDeck):
    
    banker_hand = list()
    player_hand = list()
    p_val = 0
    b_val = 0

    for i in range(2):

        banker_card = myDeck.give_first_card()
        player_card = myDeck.give_first_card()
        b_val += banker_card.value
        p_val += player_card.value
        banker_hand.append(banker_card)
        player_hand.append(player_card)
        p_val = p_val%10
        b_val = b_val%10
    
    #print_hands(banker_hand, b_val, player_hand, p_val)

    if p_val >= 8 or b_val >= 8:
        if p_val > b_val:
            return 1
        elif p_val < b_val:
            return 2
        else:
            return 0
    elif p_val >= 6:
        if b_val <= 5:

            banker_card = myDeck.give_first_card()
            b_val += banker_card.value
            banker_hand.append(banker_card)
            b_val = b_val%10
    else:
        player_card = myDeck.give_first_card()
        p_val += player_card.value
        player_hand.append(player_card)
        p_val = p_val%10

        if tableu[b_val][p_val]:
            banker_card = myDeck.give_first_card()
            b_val += banker_card.value
            banker_hand.append(banker_card)
            b_val = b_val%10
    
    #print_hands(banker_hand, b_val, player_hand, p_val)

    if p_val > b_val:
        return 1
    elif p_val < b_val:
        return 2
    else:
        return 0


def bet_and_play(myDeck, bet, stake):
    output = play_hand(myDeck)

    if bet == output:
        if bet == 1:
            return (output, stake )
        elif bet == 2:
            return (output, stake * .95)
        else:
            return (output, stake * 8)
    
    return (output, -1 * stake)


env = BaccaratEnv()

print(env.action_space.sample())

