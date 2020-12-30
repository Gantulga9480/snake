import numpy as np


class ValueFunction:

    def __init__(self, size, snake, rewards, update_rate):
        self.size = size
        self.table = np.zeros((size, size))
        self.tail = snake[0]
        self.food = snake[1]
        self.out_reward = rewards[0]
        self.food_reward = rewards[1]
        self.empty_reward = rewards[2]
        self.update_rate = update_rate

    def reset(self, board):
        self.init_table(board)
        self.update(board, reset=True)

    def update(self, board, reset=False, ur=None):
        if ur is None:
            pass
        else:
            self.update_rate = ur   
        start_table = self.table.copy()
        temp_value = start_table.copy()
        itr = 0
        if reset:
            itr = self.update_rate
        else:
            itr = 1
        for _ in range(itr):
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] == self.tail:
                        temp_value[i][j] = self.out_reward
                    elif board[i][j] == self.food:
                        temp_value[i][j] = self.food_reward
                    else:
                        temp_value[i][j] = self.getStateVal([i, j])
            self.table = temp_value.copy()
            temp_value = start_table.copy()

    def getAction(self, state):
        next_state = [[state[0]-1, state[1]], [state[0]+1, state[1]],
                      [state[0], state[1]-1], [state[0], state[1]+1]]
        vals = list()
        for i, item in enumerate(next_state):
            try:
                if item[0] >= 0 and item[1] >= 0:
                    vals.append(self.table[item[0]][item[1]])
                else:
                    vals.append(self.out_reward)
            except IndexError:
                vals.append(self.out_reward)
        return np.argmax(vals)

    def getStateVal(self, state):
        next_state = [[state[0]-1, state[1]], [state[0], state[1]+1],
                      [state[0], state[1]-1], [state[0]+1, state[1]]]
        vals = list()
        for i, item in enumerate(next_state):
            try:
                if item[0] >= 0 and item[1] >= 0:
                    vals.append(self.empty_reward + 
                                self.table[item[0]][item[1]])
                else:
                    pass
            except IndexError:
                pass
        return max(vals)

    def init_table(self, board):
        self.table = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == self.tail:
                    self.table[i][j] = self.out_reward
                elif board[i][j] == self.food:
                    self.table[i][j] = self.food_reward
