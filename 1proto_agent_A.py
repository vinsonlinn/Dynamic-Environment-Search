from collections import deque

# -*- coding: utf-8 -*-
def logic_A(cur_map, cur_position, cur_coins, cur_car_positions, penalty_k):
    # Define possible moves
    possible_moves = {
        'W': (cur_position[0], cur_position[1] - 1),  # move up
        'A': (cur_position[0] - 1, cur_position[1]),  # move left
        'S': (cur_position[0], cur_position[1] + 1),  # move down
        'D': (cur_position[0] + 1, cur_position[1]),  # move right
        #'I': cur_position  # stay in place
    }

    # Step 1: Check if near goal (prioritize goal if near)
    for move, (new_x, new_y) in possible_moves.items():
        if cur_map[new_x][new_y] == 'goal':
            return move

    # Step 2: Avoid collisions with cars
    for move, (new_x, new_y) in list(possible_moves.items()):
        if (new_x, new_y) in cur_car_positions:
            del possible_moves[move]  # Invalid move due to car
        if (cur_map[new_x][new_y] == "wall"):
            del possible_moves[move]

    # Step 3: Collect coins if possible
    closest_coin = None
    min_distance = float('inf')
    for coin in cur_coins:
        distance = abs(coin[0] - cur_position[0]) + abs(coin[1] - cur_position[1])
        if distance < min_distance:
            min_distance = distance
            closest_coin = coin

    for i, row in enumerate(cur_map):
        for j, element in enumerate(row):
            if element == "goal":
                closest_coin = (i, j)


    if closest_coin:
        # Find path to closest coin, and prioritize coin collection
        min_distance = float('inf')
        best_move = 'I'
        for move, (new_x, new_y) in possible_moves.items():
            distance = abs(closest_coin[0] - new_x) + abs(closest_coin[1] - new_y)
            if distance < min_distance:
                min_distance = distance
                best_move = move
        print (best_move)
        return best_move
            
    print (closest_coin)

    # Step 4: Make move towards a safe road
    for move, (new_x, new_y) in possible_moves.items():
        if cur_map[new_x][new_y] == 'road' and (new_x, new_y) not in cur_car_positions:
            return move

    # Step 5: If no other option, stay in place
    return 'I'

"""
current idea:
A* search
"""


def BFS(cur_map, start, goal):
    possible_moves = {
        'W': (0, - 1),  # move up
        'A': (- 1, 0),  # move left
        'S': (0,  1),  # move down
        'D': ( 1, 0),  # move right
    }

    # make queue - queue should be next node and path to node
    #   initial queue is start location and path is start
    # create a visited set

    queue = deque([(start, [])])  # Queue of (coords, path-list of coords) tuples
    visited = set()
    
    while queue:
        cur_coordinate, path = queue.popleft()
        cur_x = cur_coordinate[0]
        cur_y = cur_coordinate[1]
        if cur_coordinate == goal:
            return path
        elif cur_coordinate not in visited:
            visited.add(cur_coordinate)
            for move, (direction_x, direction_y) in possible_moves.items():
                neighbor_coord = (cur_x + direction_x, cur_y + direction_y)
                if not (0 <= neighbor_coord[0] < len(cur_map) and 0 <= neighbor_coord[1] < len(cur_map[0])): # check if neighbor is out of bounds
                    continue
                if cur_map[neighbor_coord[0]][neighbor_coord[1]] == "road": # if it is a road we can move there
                    queue.push((neighbor_coord, path + [move]))



