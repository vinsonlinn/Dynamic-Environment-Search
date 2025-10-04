from collections import deque
import json

# -*- coding: utf-8 -*-

"""
current idea: avoid cars - apparently this didn't add anything
fixed two lines in BFS

another idea: make it so that it does BFS of multiple coin pickups
want to compare multiple paths 
"""
def logic_A(cur_map, cur_position, cur_coins, cur_car_positions, penalty_k):
    possible_moves = {
        'W': (cur_position[0], cur_position[1] - 1),  # move up
        'A': (cur_position[0] - 1, cur_position[1]),  # move left
        'S': (cur_position[0], cur_position[1] + 1),  # move down
        'D': (cur_position[0] + 1, cur_position[1]),  # move right
        #'I': cur_position  # stay in place
    }

    goal_coords = find_tile(cur_map, "goal")
    #print(goal_coords)
    
    paths_to_goal = [[],[]]


    for i in range(2):
        new_coins = cur_coins.copy()
        destination = cur_position

        for j in range(10):
            suggested_path, destination = BFS(cur_map, new_coins, cur_car_positions, destination, goal_coords)
            paths_to_goal[i] = paths_to_goal[i] + suggested_path
            if (destination != goal_coords):
                if j == 0:
                    cur_coins.remove(destination)
                new_coins.remove(destination)

    #print(path_to_goal)
    #print ("path 1: " + ', '.join(paths_to_goal[0]))

    #print ("path 2: " + ', '.join(paths_to_goal[1]))

    try:
        with open('previous_moves.json', 'r') as file:
            previous_moves = json.load(file)
        print(f"Loaded previous moves: {previous_moves}")
        print("current position: " + str(cur_position))
    except (FileNotFoundError, json.JSONDecodeError):
        previous_moves = []
        print("No previous moves found.")
    
    print("next move: " + paths_to_goal[0][0])
    print("next move: " + str(possible_moves[paths_to_goal[0][0]]))
    print("next move: " + paths_to_goal[1][0])
    print("next move: " + str(possible_moves[paths_to_goal[1][0]]))
    previous_moves = tuple(previous_moves)
    if (previous_moves == possible_moves[paths_to_goal[0][0]]):
        final_move = paths_to_goal[1][0]
    elif (previous_moves == possible_moves[paths_to_goal[1][0]]):
        final_move = paths_to_goal[0][0]
    elif (len(paths_to_goal[0]) < len(paths_to_goal[1])):
        final_move = paths_to_goal[0][0]
    else:
        final_move = paths_to_goal[1][0]

    save_moves(cur_position)
    return final_move


def find_tile(cur_map, tile_to_find):
    for i, row in enumerate(cur_map):
        for j, element in enumerate(row):
            if element == tile_to_find:
                return (i, j)
            

def save_moves(moves):
    # Store the moves into a JSON file
    with open('previous_moves.json', 'w') as file:
        json.dump(moves, file)


def BFS(cur_map, cur_coins, cur_car_positions, start, goal):
    possible_moves = {
        'W': (0, - 1),  # move up
        'A': (- 1, 0),  # move left
        'S': (0,  1),  # move down
        'D': ( 1, 0),  # move right
        'I': (0, 0)
    }

    queue = deque([(start, [])])  # Queue of (coords, path-list of coords) tuples
    visited = set()
    
    while queue:
        cur_coordinate, path = queue.popleft()
        cur_x = cur_coordinate[0]
        cur_y = cur_coordinate[1]


        if cur_coordinate == goal and len(cur_coins) < 50:
            return path, cur_coordinate
        for coin in cur_coins: # if there is a closer coin, go to it
            if cur_coordinate == coin: #and len(path) < 10:
                return path, cur_coordinate
        if cur_coordinate not in visited:
            visited.add(cur_coordinate)
            for move, (direction_x, direction_y) in possible_moves.items():
                Flag_car = False
                neighbor_coord = (cur_x + direction_x, cur_y + direction_y)
                if not (0 <= neighbor_coord[0] < len(cur_map) and 0 <= neighbor_coord[1] < len(cur_map[0])): # check if neighbor is out of bounds
                    continue   

                for car in cur_car_positions:
                    if neighbor_coord == car:
                        Flag_car = True
                if cur_map[neighbor_coord[0]][neighbor_coord[1]] != "wall" and not Flag_car: # if it is a road we can move there
                    queue.append((neighbor_coord, path + [move]))



