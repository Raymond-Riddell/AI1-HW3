# pancakes.py
# Flipping pancakes with greedy best-first search (GBFS).

import pdb
import argparse
from graphics import *
from matplotlib import cm
import pdb
from queue import PriorityQueue
import random
import time

parser = argparse.ArgumentParser(description="Use greedy best-first search (GBFS) to optimally flip a stack of pancakes")
parser.add_argument('-n', '--num', metavar='pancakes', type=int, help="number of pancakes", default=8)
parser.add_argument('--seed', type=int, help="seed for randomly arranging pancakes initially")

def main(args):
    # Parse inputs
    n = args.num  # number of pancakes
    stack = list(range(n))
    if args.seed is not None:  # randomly shuffle the pancakes initially
        random.shuffle(stack)

    # Make the graphical user interface
    gui = guisetup(stack)

    # Use the graphical user interface
    while True:
        key = gui.checkKey()
        if key:
            if key == "Escape":  # quit the program
                break
            elif key == 'd':  # debug the program
                pdb.set_trace()
            elif key == 'g':  # run greedy best-first search
                path = gbfs(gui, stack)
            elif key in [str(i) for i in range(1, n + 1)]:  # manually flip some of the pancakes
                flip(gui, stack, int(key))

    gui.close()

def guisetup(stack):
    '''Create graphical user interface for a stack of n pancakes.'''
    n = len(stack)  # number of pancakes in the stack
    thickness = 12  # thickness of each pancake, in pixels
    margin = 40
    wid = margin * 2 + 30 * max(n + 1, 9)  # each successive pancake gets 30 px wider
    hei = margin * 2 + n * thickness  # top/bottom margins of 40 px + 12 px per pancake
    gui = GraphWin("Pancakes", wid, hei)

    cx = wid / 2  # center of width
    # cmap = cm.get_cmap('YlOrBr', n + 1)

    # Draw pancakes
    # ***ENTER CODE HERE*** (10 lines)
    pan_x_coefficient = 15 
    pancake_list = [[x, -1] for x in range(0, n)]
    for pan in range(n):

        # find midpoint of board
        mid = wid // 2

        # find x components 
        x_comp = pan_x_coefficient + 15
        pan_x_coefficient += 15

        
        # pan_start += 12
        # y_comp = pan_start + 40

        # make line object (the actual pancake)

        pancake = Line(Point(-x_comp + mid, 0), Point(x_comp + mid, 0))
        pancake.setWidth(thickness)
        pancake_list[pan][1] = pancake 

    pancake_map = dict()
    for tup in pancake_list:
        pancake_map[tup[0]] = tup[1]

    pan_start = 0
    for pan in stack:
        pan_start += 12
        y_comp = pan_start + 40
        pancake = pancake_map[pan]
        pancake.move(0, y_comp)
        pancake.draw(gui)

        # pancake.draw(gui)


    # width = height of win // n pancakes
    # length of pancake = 

    # Add text objects for instructions and status updates
    instructions = Text(Point(10, hei - 12), "Press a # to flip pancakes, 'g' to run GBFS, Escape to quit")
    instructions._reconfig("anchor", "w")
    instructions.setSize(8)
    instructions.draw(gui)

    status = Text(Point(cx, 20), "")
    status._reconfig("anchor", "center")
    status.setSize(12)
    status.draw(gui)

    # Return gui object
    return gui

def flip(gui, stack, p):
    '''Flip p pancakes in an ordered stack.'''
    print("Flipping", p, "pancakes" if p > 1 else "pancake")

    # Get graphics objects from GUI
    obj = gui.items
    pancakes = obj[:-2]
    status = obj[-1]

    # Update status text on GUI
    status.setText(f"Flipping {p} pancake{'s' if p > 1 else ''}")

    # Move pancakes around in the GUI
    # ***ENTER CODE HERE*** (5 lines)
    # thickness = pancakes[0].config['width']  # may be a helpful variable :)

    # Update the stack (which is separate from the graphics objects)
    # ***ENTER CODE HERE*** (2 lines)

    return stack

def cost(stack):
    '''Compute the cost h(stack) for a given stack of pancakes.
    Here, we define cost as the number of pancakes in the wrong position.'''
    # ***MODIFY CODE HERE*** (2 lines)
    h = 0
    return h

def gbfs(gui, stack):
    '''Run greedy best-first search on a stack of pancakes and return the solution path.'''
    print("Running greedy best-first search...")

    # Get graphics objects from GUI
    obj = gui.items
    pancakes = obj[:-2]
    status = obj[-1]

    # Update status text on GUI
    status.setText(f"Running greedy best-first search...")
    time.sleep(0.5)

    # ***MODIFY CODE HERE*** (20-25 lines)
    cnt = 0

    print(f'searched {cnt} paths')
    print('solution:', '')
    status.setText("...search is complete")

def simulate(stack, path):
    '''Simulate the flipping of pancakes to determine the resulting stack.'''
    fakestack = stack.copy()  # make a copy so we don't actually change the real stack
    for action in path:
        try:
            p = int(action)  # how many pancakes are we trying to flip?
            for i in range(1, p // 2 + 1):
                fakestack[-i], fakestack[- (p - i + 1)] = fakestack[-(p - i + 1)], fakestack[-i]
        except:
            print("INVALID ACTION: Check code")

    return fakestack

if __name__ == "__main__":
    main(parser.parse_args())
