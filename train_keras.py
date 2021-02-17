import snake_game as sg
import numpy as np
import os
import random
from collections import deque
from tensorflow import keras
from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.mixed_precision import experimental as mp


os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'


GOAL = 10
BUFFER_SIZE = 100000
MIN_BUFFER_SIZE = 20000
BATCH_SIZE = 32
DISCOUNT_RATE = 0.99
LEARNING_RATE = 0.0001
EPSILON = 1
MIN_EPSILON = 0.01
EPSILON_DECAY = .00000495
# EPSILON_DECAY = 1
TARGET_NET_UPDATE_FREQUENCY = 1000

REPLAY_BUFFER = deque(maxlen=BUFFER_SIZE)
SAMPLES = list()

TRAIN_COUNT = 1
FRAME = 1
EPISODE = 1


class MyCallback(keras.callbacks.Callback):

    def on_epoch_end(self, epoch, logs=None):
        if logs.get('accuracy') > 0.95:
            print("Reached 95% accuracy so cancelling training!")
            self.model.stop_training = True


def get_model():
    inputs = keras.Input(shape=(400,), name='input')
    dense1 = Dense(1024, activation='relu', name='dense_1')
    x = dense1(inputs)
    dense2 = Dense(1024, activation='relu', name='dense_2')
    x = dense2(x)
    dense3 = Dense(512, activation='relu', name='dense_3')
    x = dense3(x)
    dense4 = Dense(128, activation='relu', name='dense_4')
    x = dense4(x)
    x = Dense(4, name='dense_logits')(x)
    outputs = Activation('linear', dtype='float32',
                         name='predictions')(x)
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE),
                  metrics=["accuracy"])
    return model


def keras_train():
    SAMPLES = random.sample(REPLAY_BUFFER, BATCH_SIZE)
    current_states = np.array([item[0] for item in SAMPLES])
    new_current_state = np.array([item[2] for item in SAMPLES])
    current_qs_list = []
    future_qs_list = []
    current_qs_list = main_nn.predict(current_states)
    future_qs_list = target_nn.predict(new_current_state)

    X = []
    Y = []
    for index, (state, action, n_state, reward, done) in enumerate(SAMPLES):
        if not done:
            new_q = reward + DISCOUNT_RATE * np.max(future_qs_list[index])
        else:
            new_q = reward

        current_qs = current_qs_list[index]
        current_qs[action] = new_q

        X.append(state)
        Y.append(current_qs)
    main_nn.fit(np.array(X), np.array(Y), epochs=20,
                batch_size=BATCH_SIZE, shuffle=False,
                verbose=0, callbacks=[callbacks])


policy = mp.Policy('mixed_float16', loss_scale='dynamic')
mp.set_policy(policy)


sg.init()
game = sg.Snake()

main_nn = get_model()
target_nn = get_model()
target_nn.set_weights(main_nn.get_weights())
callbacks = MyCallback()
show_every = 10
ep_reward = 0
play = True
action = None


while play:
    nn_state = game.reset()
    terminal = False
    while not terminal:
        FRAME += 1
        if np.random.random() < EPSILON:
            action = np.random.randint(0, 3)
        else:
            action = np.argmax(main_nn.predict(np.expand_dims(nn_state,
                                                              axis=0)))
        terminal, new_nn_state, r, play = game.step(action=action)
        REPLAY_BUFFER.append([nn_state, action, new_nn_state, r, terminal])
        nn_state = new_nn_state
        EPSILON = max(EPSILON - EPSILON_DECAY, MIN_EPSILON)

        if not play:
            terminal = True

        if len(REPLAY_BUFFER) > MIN_BUFFER_SIZE:
            keras_train()
            TRAIN_COUNT += 1

        if FRAME % TARGET_NET_UPDATE_FREQUENCY == 0 and \
                len(REPLAY_BUFFER) > MIN_BUFFER_SIZE:
            target_nn.set_weights(main_nn.get_weights())
            print("target_net update!!!")
    
    if EPISODE % show_every == 0:
        print("ep:", EPSILON, "frame:", FRAME)
    EPISODE += 1
    

print("Training done congrat!!!")
# main_nn.save("main")
# target_nn.save("target")
