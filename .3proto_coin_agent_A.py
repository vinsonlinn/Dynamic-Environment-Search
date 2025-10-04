from collections import deque
# .3proto_coin_agent_A
# -*- coding: utf-8 -*-

"""
current idea: go to either closest coin or goal
fixed two lines in BFS
"""
def logic_A(cur_map, cur_position, cur_coins, cur_car_positions, penalty_k):

    # Get 5 closest coins
    """
    target_coins = []
    highest_distance = float('-inf')
    for coin in cur_coins:
        manhat_dis = abs(cur_position[0] - coin[0]) + abs(cur_position[1] - coin[1])
        if (len(target_coins) < 5):
            target_coins.append(coin)
            if (manhat_dis > highest_distance):
                max_distance = manhat_dis
        elif (manhat_dis < highest_distance)
    """
    goal_coords = find_tile(cur_map, "goal")
    #print(goal_coords)
    

    path_to_goal = BFS(cur_map, cur_coins, cur_position, goal_coords)
    #print(path_to_goal)

    return path_to_goal[0]


def find_tile(cur_map, tile_to_find):
    for i, row in enumerate(cur_map):
        for j, element in enumerate(row):
            if element == tile_to_find:
                return (i, j)

def BFS(cur_map, cur_coins, start, goal):
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

        if cur_coordinate == goal:
            return path
        for coin in cur_coins: # if there is a closer coin, go to it
            if cur_coordinate == coin: #and len(path) < 10:
                return path
        if cur_coordinate not in visited:
            visited.add(cur_coordinate)
            for move, (direction_x, direction_y) in possible_moves.items():
                neighbor_coord = (cur_x + direction_x, cur_y + direction_y)
                if not (0 <= neighbor_coord[0] < len(cur_map) and 0 <= neighbor_coord[1] < len(cur_map[0])): # check if neighbor is out of bounds
                    continue               
                if cur_map[neighbor_coord[0]][neighbor_coord[1]] != "wall": # if it is a road we can move there
                    queue.append((neighbor_coord, path + [move]))



