import argparse
import snake_game as sg

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--description")
parser.add_argument("-c", "--colorful", action="store_true")
parser.add_argument("-sv", "--show_val", action="store_true")
parser.add_argument("-ur", "--update_rate", type=int)

args = parser.parse_args()

sg.init(args.description)
game = sg.Snake(colorful=args.colorful, num=args.show_val,
                update_rate=args.update_rate)

for episode in range(10000):
    state = game.reset()
    game.v.reset(game.board.copy())
    done = False
    while not done:
        action = game.v.getAction(state)
        done, state, _ = game.step(action=action)
