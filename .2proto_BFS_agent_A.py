from collections import deque

# -*- coding: utf-8 -*-
def logic_A(cur_map, cur_position, cur_coins, cur_car_positions, penalty_k):

    """
    current idea:
    BFS to goal
    """
    goal_coords = find_tile(cur_map, "goal")
    #print(goal_coords)

    path_to_goal = BFS(cur_map, cur_position, goal_coords)
    #print(path_to_goal)

    return path_to_goal[0]


def find_tile(cur_map, tile_to_find):
    for i, row in enumerate(cur_map):
        for j, element in enumerate(row):
            if element == tile_to_find:
                return (i, j)

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
                if cur_map[neighbor_coord[0]][neighbor_coord[1]] != "wall": # if it is a road we can move there
                    queue.append((neighbor_coord, path + [move]))



