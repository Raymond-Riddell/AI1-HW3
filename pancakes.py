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
from collections import deque

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
                stack = flip(gui, stack, int(key))

    gui.close()

def guisetup(stack):
    '''Create graphical user interface for a stack of n pancakes.'''
    n = len(stack)  # number of pancakes in the stack
    thickness = 12  # thickness of each pancake, in pixels
    margin = 40
    wid = margin * 2 + 30 * max(n + 1, 9)  # each successive pancake gets 30 px wider
    hei = margin * 2 + n * thickness  # top/bottom margins of 40 px + 12 px per pancake
    cx = wid / 2  # center of width
    gui = GraphWin("Pancakes", wid, hei)

    # Draw pancakes
    # ***ENTER CODE HERE*** (10 lines)

    draw_pancakes(gui, stack, n)

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

def flip(gui, stack, p, update_gui=True):
    '''Flip p pancakes in an ordered stack.'''
    print("Flipping", p, "pancakes" if p > 1 else "pancake")

    stack = flip_stack(stack, p)
    if update_gui:
        draw_pancakes(gui, stack, len(stack))
    return stack

def flip_stack(stack, p):
    temp = []

    stack_copy = stack.copy()
    for i in range(p):
        temp.insert(0, stack_copy.pop(0))

    for i in range(len(temp)):
        stack_copy.insert(0, temp.pop())
    return stack_copy


    # Move pancakes around in the GUI
    # ***ENTER CODE HERE*** (5 lines)
    # thickness = pancakes[0].config['width']  # may be a helpful variable :)

    # Update the stack (which is separate from the graphics objects)
    # ***ENTER CODE HERE*** (2 lines)

    return stack

def calc_cost(stack):
    '''Compute the cost h(stack) for a given stack of pancakes.
    Here, we define cost as the number of pancakes in the wrong position.'''
    # ***MODIFY CODE HERE*** (2 lines)
    h = 0
    lst = [a for a in range(len(stack))]
    for i in range(len(stack)):
        h += 1 if lst[i] != stack[i] else 0
    return h

def gbfs(gui, stack):
    '''Run greedy best-first search on a stack of pancakes and return the solution path.'''
    print("Running greedy best-first search...")

    # Get graphics objects from GUI
    objects = gui.items
    status = None
    for obj in objects:
        if type(obj) == Text and obj.getText() != "Press a # to flip pancakes, 'g' to run GBFS, Escape to quit":
            status = obj
            break


    # Update status text on GUI
    status.setText(f"Running greedy best-first search...")
    time.sleep(0.5)

    # ***MODIFY CODE HERE*** (20-25 lines)
    path, cnt  = search(stack, "", calc_cost(stack), 0)
    

    print(f'searched {cnt} paths')
    print(f'solution: {path}')
    status.setText("...search is complete")


def search(state, path, cost, count):

    initial_state = state.copy()
    
    # in --> [] out -->
    path = ""
    cnt = 0
    backpointers = dict()
    id = 0
    visited = {id:state.copy()} # {id : stack} a look up table for all vistited states

    # queue consists of ids corresponding to state, and a cost associated with the h(state)
    queue = deque([[id, calc_cost(visited[id])]])  # items are [id(), h(state)]
    id += 1

    while True:
        cnt += 1

        node_id, node_cost = queue.pop()
        node = visited[node_id].copy() # node is a stack of pancakes (integers), and represents the current state
        if node_cost == 0:

            path = ""
            parent_id = backpointers[node_id]
            parent = visited[parent_id]
            path += str(find_move(node, parent))
            while parent != initial_state:
                child_id = backpointers[parent_id]
                child = visited[child_id]
                move = find_move(child, parent)
                path += str(move)
                parent_id = backpointers[parent]
                parent = visited[parent_id]

            return path, cnt

        moves = [a for a in range(2, len(node) + 1)]

        for move in moves:
            child = flip_stack(node.copy(), move)
            child_cost = calc_cost(child)

            if child not in visited.values():
                child_id = id
                id += 1
                queue.appendleft([child_id, child_cost])
                visited[child_id] = child
                backpointers[child_id] = node_id


        # sort the queue
        queue = deque(sorted(queue, key=lambda pair : pair[1], reverse=True))

        print(cnt)


def find_children(state):

    children = []

    pass
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

def draw_pancakes(gui, stack, n):


    # Draw pancakes
    # ***ENTER CODE HERE*** (10 lines)
    cmap = cm.get_cmap('YlOrBr', n + 1)
    colors = [cmap.__call__(i) for i in range(n)]
    old_lines = [obj for obj in gui.items if type(obj) == Line]
    for line in old_lines:
        line.undraw()

    thickness = 12  # thickness of each pancake, in pixels
    margin = 40
    wid = margin * 2 + 30 * max(n + 1, 9)  # each successive pancake gets 30 px wider
    hei = margin * 2 + n * thickness  # top/bottom margins of 40 px + 12 px per pancake
    pan_x_coefficient = 15 
    pancake_list = [[x, None] for x in range(n)]
    for pan in range(n):

        # find midpoint of board
        mid = wid // 2

        # find x components 
        x_comp = pan_x_coefficient + 15
        pan_x_coefficient += 15

        # make line object (the actual pancake)
        pancake = Line(Point(-x_comp + mid, 0), Point(x_comp + mid, 0))
        pancake.setFill(color_rgb(*[int(a*100)*2 for a in colors[pan][:-1]]))
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


def find_move(state1, state2):
    '''Looks at two board states, and determines how many pancakes need to be flipped to produce the other state'''
    count_same = 0
    i = len(state1) - 1

    if state1 == state2:
        return 0

    while state1[i] == state2[i]:
        count_same += 1
        i -= 1

    return len(state1) - count_same
        


def make_path(backpointers, goal_state):
    
    path = ""

    # find parent of goal state 


if __name__ == "__main__":
    main(parser.parse_args())
