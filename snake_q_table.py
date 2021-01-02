import snake_game as sg
import numpy as np

# Game
sg.init()
snake = sg.Snake()

# Train
q_table = np.zeros((4, 8, 20, 20, 3), dtype=int)
DISCOUNT_RATE = 0.999
LEARNING_RATE = 0.1
epsilon = 1
epsilon_min = 0
max_iter = 1000000
epsilon_decay_val = (epsilon-epsilon_min) / (max_iter)
converged = False

show_every = 100
ep_count = 0

while snake.play and not converged:
    # Reset
    over = False
    action_count = 0
    state = snake.reset()

    # Start episode
    while not over:
        if np.random.random() > epsilon:
            action = np.argmax(q_table[state[0]][state[1]][state[2][0]][state[2][1]])
        else:
            action = np.random.randint(0, 2)
        over, new_state, reward = snake.step(action)
        action_count += 1
        if not over:
            max_future_q = np.max(q_table[new_state[0]][new_state[1]][new_state[2][0]][new_state[2][1]])

            current_q = q_table[state[0]][state[1]][state[2][0]][state[2][1]][action]

            # if action_count > 100:
            #    reward -= 100

            new_q = current_q + LEARNING_RATE * (reward + DISCOUNT_RATE * max_future_q - current_q)

            q_table[state[0]][state[1]][state[2][0]][state[2][1]][action] = new_q

        elif over:
            q_table[state[0]][state[1]][state[2][0]][state[2][1]][action] = reward

        state = new_state

    # Episode end
    ep_count += 1
    epsilon = max(epsilon - epsilon_decay_val, epsilon_min)

    # Game info
    if ep_count % show_every == 0:
        print(epsilon)

# Training end
# np.save("q_table.npy", q_table)
