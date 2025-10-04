from collections import deque
import json
import heapq
import os

# -*- coding: utf-8 -*-

"""
current idea: add a one off coin
if there is an easy coin to get we get it
do this by remembering the path and calculating if it is worth getting
"""


class Node:
    def __init__(self, position, parent=None, move=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.move = move # move to get here from parent
        self.g = g  # Cost from start node
        self.h = h  # Heuristic cost to goal
        self.f = g + h  # Total cost function


    def __lt__(self, other):
        return self.f < other.f
    

def logic_A(cur_map, cur_position, cur_coins, cur_car_positions, penalty_k):

    file_path = 'previous_moves.json'
    if os.path.exists(file_path):

        with open('previous_moves.json', 'r') as file:
            content = file.read()
            if content.strip():  # Check if the file is not empty
            
                iteration, intended_path = json.loads(content)
                #print("iteration: " + str(iteration))
                #print(intended_path)
                if iteration < len(intended_path):
                    save_moves((iteration + 1, intended_path))
                    return intended_path[iteration]
                



    goal_coords = find_tile(cur_map, "goal")

    

    path_to_goal, future_coin_list = A_star(cur_map, cur_coins, cur_car_positions, penalty_k, cur_position, goal_coords)

    
    new_coins = cur_coins.copy()
    count = 0
    for i in range(cur_position[0] - 3, cur_position[0] + 3):
        for j in range(cur_position[1] - 3, cur_position[1] + 3):
            if (i, j) in cur_coins:
                count = count + 1
    if count < 3:
        for coin in future_coin_list:
            new_coins.remove(coin)
        NA, path_to_nearest_coin = BFS(cur_map, new_coins, cur_car_positions, cur_position)
        if (len(path_to_nearest_coin) * penalty_k * 2) < 9:
            """
            reverse = []
            for i in path_to_nearest_coin:
                if i == 'W':
                    reverse.append('S')
                if i == 'S':
                    reverse.append('W')
                if i == 'A':
                    reverse.append('D')
                if i == 'D':
                    reverse.append('A')
            """
            save_moves((1, path_to_nearest_coin))


            return path_to_nearest_coin[0]
        

    return path_to_goal[1]



def find_tile(cur_map, tile_to_find):
    for i, row in enumerate(cur_map):
        for j, element in enumerate(row):
            if element == tile_to_find:
                return (i, j)
            


def save_moves(moves):
    # Store the moves into a JSON file
    with open('previous_moves.json', 'w') as file:
        json.dump(moves, file)


def A_star(cur_map, cur_coins, cur_car_positions, penalty, start, goal):
    possible_moves = {
        'W': (0, - 1),  # move up
        'A': (- 1, 0),  # move left
        'S': (0,  1),  # move down
        'D': ( 1, 0),  # move right
        'I': (0, 0)
    }

    open_list = []
    visited = set()
    heapq.heappush(open_list, Node(start, None, None, 0, 0))
    
    while open_list:
        current_node = heapq.heappop(open_list)

        cur_coordinate = current_node.position
        cur_x, cur_y = cur_coordinate

        if cur_coordinate == goal:
            path = []
            future_coin_list = []
            while current_node:
                path.append(current_node.move)
                if current_node.position in cur_coins:
                    future_coin_list.append(current_node.position)
                current_node = current_node.parent
            return path[::-1], future_coin_list  # Return reversed path
        for coin in cur_coins: # if there is a closer coin, go to it
            if cur_coordinate == coin: #and len(path) < 10:
                path = []
                while current_node:
                    path.append(current_node.move)
                    current_node = current_node.parent
                return path[::-1]  # Return reversed path"""

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
                    h = heuristic(cur_map, cur_coins, cur_car_positions, neighbor_coord, penalty, goal)
                    g = current_node.g + penalty
                    if neighbor_coord in cur_coins:
                        g = g - 10
                    neighbor_node = Node(neighbor_coord, current_node, move, g, h)
                    heapq.heappush(open_list, neighbor_node)


def heuristic(cur_map, cur_coins, cur_car_positions, position, penalty, goal):
    # Manhattan distance (can be changed depending on the problem)
    #h =  abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    coin_location, path_to_coin = BFS(cur_map, cur_coins, cur_car_positions, position)
    h_second_coin = penalty * len(path_to_coin) - 10
    new_coins = cur_coins.copy()
    #h_single_coin_back = 100
    #if (penalty * len(path_to_coin) * 2) < 10:
    #    h_single_coin_back = -1000
    depth = 0

    for i in range(depth):
        new_coins.remove(coin_location)
        coin_location, path_to_second_coin = BFS(cur_map, new_coins, cur_car_positions, coin_location)
    
        h_second_coin = h_second_coin + (penalty * len(path_to_second_coin) - 10)
    #NA, path_to_second_coin = BFS(cur_map, cur_coins, cur_car_positions, coin_location)
    #h_single_coin = penalty * len(path_to_coin) - 10 + penalty * len(path_to_second_coin)
    return h_second_coin


def BFS(cur_map, goals, cur_car_positions, start):
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
        cur_x , cur_y= cur_coordinate


        if cur_coordinate in goals:
            return cur_coordinate, path

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
