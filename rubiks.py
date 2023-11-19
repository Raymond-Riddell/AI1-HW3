# rubiks.py
# Solve a 3x3 Rubik's cube using A* search.

import argparse
from re import L
from graphics import *
import pdb
from queue import PriorityQueue

parser = argparse.ArgumentParser(description="Solving a Rubik's Cube with A* Search")
parser.add_argument('-s', '--state', help="text file containing initial state of the cube, encoded as a sequence of integers")

def main(args):
    # Initialize dictionary of parameters
    params = {
        'colors': ["#b71234",
                   "#0046ad",
                   "#ffffff",
                   "#009b48",
                   "#ffd500",
                   "#ff5800"],
        'n': 3,
        'pixels': 45,
        'thickness': 4}

    # Make list to store individual square colors
    # HINT: If the user entered an initial state via command line argument, you
    # should modify this code so that the current_state is *not* the solved
    # cube, but rather the colors of the initial state.
    # ***MODIFY CODE HERE*** (7 lines)
    current_state = []

    # pointer to current color in the string of colors corresponding to each square in the cube
    color_idx = 0 

    # if a state is given
    if args.state:

        # read the colors from the inputted file
        colors_list = list(read_file(args.state)[0])

        # iterate through each face of the cube
        for i in range(6):
            side = [i] * params['n'] ** 2 # create the ith face of the cube

            # recolor the cube by reading the "colors_list" using a pointer
            for j in range(len(side)):
                side[j] = colors_list[color_idx]
                color_idx += 1
            # append each square in the ith face to the current state 
            for e in side:
                current_state.append(int(e))
    
    # in the event that a state is not given
    else:
        # color each side of the cube, with each side having a unique color
        for i in range(6):
            current_state += [i] * params['n'] ** 2

    # ***DO NOT MODIFY THE FOLLOWING 2 LINES***
    initial_state = current_state.copy()  # for resetting the cube
    previous_state = current_state.copy()  # for undoing user actions

    # Create GUI
    gui = guisetup(params)
    recolor(gui, current_state, params)  # in case the initial state is mixed

    # Wait for user interaction
    while True:
        key = gui.checkKey()
        if key:
            # print(current_state)
            if key == "Escape":  # quit the program
                break

            elif key == 'p':  # debug the program
                pdb.set_trace()

            elif key == "Ctrl+r":
                # Reset the cube to its initial state
                print('Resetting cube to initial state')
                current_state = initial_state.copy()
                previous_state = initial_state.copy()
                recolor(gui, current_state, params)

            elif key == "Ctrl+z":
                # Undo the last user action
                print('Undoing last user action')
                current_state = previous_state.copy()
                recolor(gui, current_state, params)

            elif key.upper() in 'UDLRBF':
                # Rotate one of the cube faces clockwise
                previous_state = current_state.copy()
                face = key.upper()
                direction = 'CW'
                print("Rotating", face, "face", direction)
                txt = gui.items[-1]
                txt.setText("Rotating " + face + " face " + direction)
                rotate(current_state, face, direction)
                recolor(gui, current_state, params)

            elif key[:6] == 'Shift+' and key[6].upper() in 'UDLRBF':
                # Rotate one of the cube faces counterclockwise
                previous_state = current_state.copy()
                face = key[6].upper()
                direction = 'CCW'
                print("Rotating", face, "face", direction)
                txt = gui.items[-1]
                txt.setText("Rotating " + face + " face " + direction)
                rotate(current_state, face, direction)
                recolor(gui, current_state, params)

            elif key == 'a':
                # Solve the cube using A* search
                path, cnt = astar(current_state, params)
                print(f'Paths searched: {cnt - 1}')
                print(f'final path: {path}')

            elif key == 'h':
                # Print the current heuristic cost
                print(f"Current heuristic cost = {cost('', current_state)}")

    gui.close()

def astar(state, params, verbose=False):
    '''Run A* search on the cube based on its current state and return the solution path.'''
    print('Running A* search...')
    # ***ENTER CODE HERE*** (20-25 lines)
    cnt = 0
    
    initial_state = state.copy()
    priority = "udlrbfUDLRBF"
    # starting_node = priority[0] # path
    starting_node = ""

    # nodes here are [cost, path] pairs 
    queue = [[cost(starting_node, simulate(initial_state, starting_node)), starting_node]] # [cost(path), path]
    visited = []
    final_path = ""


    while True:

        cnt += 1

        # pop the current node off the queue
        curr_cost, curr_path = queue.pop()

        # generate the current state of the game for the given path
        curr_state = simulate(initial_state, curr_path)

        # check if this state is the solution
        if is_solved(curr_state, params):
            final_path = curr_path
            break
        
        # generate all children for the given state of the game
        # First we generate the cost of the ith child node. Given that the cost function takes in a path, and a game state (list),
        # we have to use the simulate function to find out what the child state would be if performed the new set of moves, which are defined by 
        # concatonating the current path with the newest move
        children = [[cost(curr_path + move, simulate(initial_state, curr_path + move)), curr_path + move] for move in priority]

        # check if we have visited each child, and if not, add them to the visited and add them to the queue
        for child in children:
            if child not in visited:
                visited.append(child)
                queue.insert(0, child)

        # sort the queue
        queue = sorted(queue.copy(), key=lambda pair : pair[0], reverse=True)


    return final_path, cnt

def cost(node, state):
    '''Compute the cost g(node)+h(node) for a given set of moves (node) leading to a cube state.
    Let g(node) be the number of moves it took to get to the state.
    Let h(node) be the average number of incorrect square colors on the cube. For h(node)=0, all colors will match the center color of that face, which never moves.
    '''
    # ***MODIFY CODE HERE*** (1 line)
    g = len(node)
    h = 0

    for i in range(6):
        center_color = state[(i * 9) + 4]
        for j in range(9):
            if state[(i * 9) + j] != center_color:
                h += 1

    h /= 6

    return g + h

def drawface(gui, x0, y0, c, n, w, t):
    '''Draw an individual face of the cube. Requires GraphWin object, starting (x,y) position of the top-left corner of the face, face color, number of squares per row/column, pixel width of each square, and border thickness.'''
    for i in range(n):
        for j in range(n):
            x = x0 + j * w
            y = y0 + i * w
            square = Rectangle(Point(x, y), Point(x + w, y + w))
            square.setFill(c)
            square.setWidth(t)
            square.draw(gui)

def guisetup(params):
    '''Create graphical user interface for Rubik's Cube with n rows and columns.'''

    # Extract relevant parameters
    n = params['n']
    clr = params['colors']
    px = params['pixels']
    t = params['thickness']

    # Draw graphics window
    wid = (4 * n + 2) * px  # +2 for the margin
    hei = (3 * n + 2) * px  # +2 for the margin
    gui = GraphWin("Rubik's Cube", wid, hei)

    # Draw cube faces
    drawface(gui, (n + 1) * px, px, clr[0], n, px, t)  # upper
    drawface(gui, px, (n + 1) * px, clr[1], n, px, t)  # left
    drawface(gui, (n + 1) * px, (n + 1) * px, clr[2], n, px, t)  # front
    drawface(gui, (2 * n + 1) * px, (n + 1) * px, clr[3], n, px, t)  # right
    drawface(gui, (3 * n + 1) * px, (n + 1) * px, clr[4], n, px, t)  # back
    drawface(gui, (n + 1) * px, (2 * n + 1) * px, clr[5], n, px, t)  # down

    # Add text instructions
    txt = Text(Point(15, 20), "Press U/D/L/R/B/F to rotate a cube face CW (hold Shift for CCW)")
    txt._reconfig("anchor", "w")
    txt.setSize(12)
    txt.draw(gui)

    # Add text to be used to display user actions
    txt = Text(Point(15, hei - 20), "")
    txt._reconfig("anchor", "w")
    txt.setSize(12)
    txt.setFill("red")
    txt.draw(gui)

    # Return gui object and list of cube square color indices
    return gui

def rotate(state, face, direction='CW'):
    '''Rotate the cube face (U/D/L/R/B/F) in a given direction (CW/CCW).'''
    if face == 'U':
        src = [9, 10, 11, 18, 19, 20, 27, 28, 29, 36, 37, 38, 0, 1, 2, 5, 8, 7, 6, 3]
        if direction == 'CW':
            dst = [36, 37, 38, 9, 10, 11, 18, 19, 20, 27, 28, 29, 2, 5, 8, 7, 6, 3, 0, 1]
        elif direction == 'CCW':
            dst = [18, 19, 20, 27, 28, 29, 36, 37, 38, 9, 10, 11, 6, 3, 0, 1, 2, 5, 8, 7]

    elif face == 'D':
        src = [45, 46, 47, 50, 53, 52, 51, 48, 15, 16, 17, 24, 25, 26, 33, 34, 35, 42, 43, 44]
        if direction == 'CW':
            dst = [47, 50, 53, 52, 51, 48, 45, 46, 24, 25, 26, 33, 34, 35, 42, 43, 44, 15, 16, 17]
        elif direction == 'CCW':
            dst = [51, 48, 45, 46, 47, 50, 53, 52, 42, 43, 44, 15, 16, 17, 24, 25, 26, 33, 34, 35]

    elif face == 'L':
        src = [0, 3, 6, 18, 21, 24, 45, 48, 51, 38, 41, 44, 9, 10, 11, 12, 14, 15, 16, 17]
        if direction == 'CW':
            dst = [18, 21, 24, 45, 48, 51, 44, 41, 38, 6, 3, 0, 11, 14, 17, 10, 16, 9, 12, 15]
        elif direction == 'CCW':
            dst = [44, 41, 38, 0, 3, 6, 18, 21, 24, 51, 48, 45, 15, 12, 9, 16, 10, 17, 14, 11]

    elif face == 'R':
        src = [2, 5, 8, 20, 23, 26, 47, 50, 53, 36, 39, 42, 27, 28, 29, 30, 32, 33, 34, 35]
        if direction == 'CW':
            dst = [42, 39, 36, 2, 5, 8, 20, 23, 26, 53, 50, 47, 29, 32, 35, 28, 34, 27, 30, 33]
        elif direction == 'CCW':
            dst = [20, 23, 26, 47, 50, 53, 42, 39, 36, 8, 5, 2, 33, 30, 27, 34, 28, 35, 32, 29]

    elif face == 'B':
        src = [36, 37, 38, 41, 44, 43, 42, 39, 2, 1, 0, 9, 12, 15, 51, 52, 53, 35, 32, 29]
        if direction == 'CW':
            dst = [38, 41, 44, 43, 42, 39, 36, 37, 9, 12, 15, 51, 52, 53, 35, 32, 29, 2, 1, 0]
        elif direction == 'CCW':
            dst = [42, 39, 36, 37, 38, 41, 44, 43, 35, 32, 29, 2, 1, 0, 9, 12, 15, 51, 52, 53]

    elif face == 'F':
        src = [18, 19, 20, 23, 26, 25, 24, 21, 6, 7, 8, 27, 30, 33, 47, 46, 45, 17, 14, 11]
        if direction == 'CW':
            dst = [20, 23, 26, 25, 24, 21, 18, 19, 27, 30, 33, 47, 46, 45, 17, 14, 11, 6, 7, 8]
        elif direction == 'CCW':
            dst = [24, 21, 18, 19, 20, 23, 26, 25, 17, 14, 11, 6, 7, 8, 27, 30, 33, 47, 46, 45]

    temp = state.copy()
    for i, j in zip(src, dst):
        state[j] = temp[i]

def recolor(gui, state, params):
    '''Recolor the cube in the GUI.'''

    # Get graphics objects from GUI
    obj = gui.items
    squares = obj[:-1]

    # Extract relevant parameters
    n = params['n']
    c = params['colors']

    # Update colors
    for i in range(len(state)):
        squares[i].setFill(c[state[i]])

def simulate(state, node):
    '''Simulate rotating the cube from an input state to determine resulting state. 
    The input node is a sequence of rotations.'''
    s = state.copy()  # copy the state so that we don't change the actual cube!
    # ***ENTER CODE HERE***  (4 lines)

    for move in node:
        if move == move.upper():
            rotate(s, move, direction="CCW")
        else:
            rotate(s, move.upper(), direction="CW")


    return s

def is_solved(state, params):
    '''Takes a cube state as a 1D list, and determines if the cube is solved'''
    
    # create a solved cube
    solved = []
    for i in range(6):
        solved += [i] * params['n'] ** 2
    
    # check the solved state with the given state
    return state == solved


def read_file(file_name):
    '''Takes the name of a file, and returns the contents of the file as a list, where each element is a line in the file'''
    with open(file_name, 'r') as file:
        return file.readlines()

if __name__ == '__main__':
    main(parser.parse_args())
