import snake_game as sg
import numpy as np

# Game
sg.init()
snake = sg.Snake()

# Train
q_table = np.zeros((4, 8, 20, 20, 3), dtype=int)
DISCOUNT_RATE = 0.999
LEARNING_RATE = 0.9
epsilon = 0
epsilon_min = 0
max_iter = 1000
epsilon_decay_val = (epsilon-epsilon_min) / (max_iter)
converged = False

last_show = 100

while snake.play and not converged:
    # Reset
    over = False
    state = snake.reset()
    while not over:
        if np.random.random() > epsilon:
            action = np.argmax(q_table[state[0]][state[1]][state[2][0]][state[2][1]])
        else:
            action = np.random.randint(0, 2)
        over, new_state, reward = snake.step(action)
        if not over:
            max_future_q = np.max(q_table[new_state[0]][new_state[1]][new_state[2][0]][new_state[2][1]])

            current_q = q_table[state[0]][state[1]][state[2][0]][state[2][1]][action]

            new_q = current_q + LEARNING_RATE * (reward + DISCOUNT_RATE * max_future_q - current_q)

            q_table[state[0]][state[1]][state[2][0]][state[2][1]][action] = new_q

        elif over:
            q_table[state[0]][state[1]][state[2][0]][state[2][1]][action] = reward
        state = new_state
    epsilon = max(epsilon - epsilon_decay_val, epsilon_min)
np.save("q_table.npy", q_table)
