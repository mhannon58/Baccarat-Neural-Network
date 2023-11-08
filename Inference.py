import gym
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy
import random

model = torch.jit.load('./Baccarat_Model_1')
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

from baccarat import BaccaratEnv


env = BaccaratEnv()



for i in range(100):
    state = tuple()
    for i in range(10):
        state += (random.randint(0,2),)
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    action = model(state).max(1)[1].view(1, 1)

    print(action)




'''
state, info = env.reset()
state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
for t in count():
    action = model(state).max(1)[1].view(1, 1)
    
    observation, reward, terminated, info = env.step(action.item())
    print(info)
    reward = torch.tensor([reward], device=device)
    done = terminated 

    if terminated:
        next_state = None
    else:
        next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

    # Store the transition in memory

    # Move to the next state
    state = next_state
'''