

import time
from random import choice
from BaseAI import BaseAI

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
vecIndex = [UP, DOWN, LEFT, RIGHT]

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        max_move = None
        max_utility = float('-inf')

    
        start_time = time.time()

        depth = 3

        for move in moves:
            if time.time() - start_time > 0.2:
                break

            
            child_grid = move[1]  
            utility = self.expectiminimax(child_grid, depth, start_time, False, float('-inf'), float('inf'))

            if utility > max_utility:
                max_move = move[0]  
                max_utility = utility

        return max_move if max_move is not None else choice(vecIndex)


    def expectiminimax(self, grid, depth, start_time, is_max, alpha, beta):
        if depth == 0 or time.time() - start_time > 0.2:
            return self.heuristic(grid)

        if is_max:
            max_utility = float('-inf')
            moves = [move for move, _ in grid.getAvailableMoves()]
            for move in moves:
                child_grid = grid.clone()
                if child_grid.move(move):
                    utility = self.expectiminimax(child_grid, depth - 1, start_time, False, alpha, beta)
                    max_utility = max(max_utility, utility)
                    alpha = max(alpha, utility)

                    if beta <= alpha:
                        break  

            return max_utility
        else:
            cells = grid.getAvailableCells()
            if not cells:
                return float('inf')  

            tile_probabilities = {2: 0.9, 4: 0.1}
            avg_utility = 0
            num_cells = len(cells)
            for value, prob in tile_probabilities.items():
                for cell in cells:
                    child_grid = grid.clone()
                    child_grid.insertTile(cell, value)
                    utility = self.expectiminimax(child_grid, depth - 1, start_time, True, alpha, beta)
                    avg_utility += utility * prob
                    
                    if is_max:
                        alpha = max(alpha, utility)
                    else:
                        beta = min(beta, utility)

                    if beta <= alpha:
                        break  

            return avg_utility / num_cells


    def heuristic(self, grid):
        
        weights = {
            'max_tile': 1.0,
            'smoothness': 0.75,
            'free_tiles': 3.5,
            'merge_potential': 1.75,
            'monotonicity': 2.25,
            'max_tile_in_corner': 3.5,
            'tile_gradient': 1.25,
            'penalize_blocked_tiles': 1.25,
            'higher_value_corner_tile': 2.5,
            'edge_maximization': 2.75,
            }

       
        max_tile = grid.getMaxTile()
        smoothness = self.calculate_smoothness(grid)
        free_tiles = len(grid.getAvailableCells())
        merge_potential = self.calculate_merge_potential(grid)
        monotonicity = self.calculate_monotonicity(grid)
        max_tile_in_corner = self.is_max_tile_in_corner(grid, max_tile)
        tile_gradient = self.calculate_tile_gradient(grid)
        penalize_blocked_tiles = self.penalize_blocked_tiles(grid)
        edge_maximization = self.calculate_edge_maximization(grid)

        
        heuristic_score = (
            weights['max_tile'] * max_tile +
            weights['smoothness'] * smoothness +
            weights['free_tiles'] * free_tiles +
            weights['merge_potential'] * merge_potential +
            weights['monotonicity'] * monotonicity +
            weights['max_tile_in_corner'] * max_tile_in_corner +
            weights['tile_gradient'] * tile_gradient +
            weights['penalize_blocked_tiles'] * penalize_blocked_tiles +
            weights['edge_maximization'] * edge_maximization
        )

        return heuristic_score

 
    def calculate_monotonicity(self, grid):
        
        
       
        weights = [0, 0]

        for x in range(grid.size):
            row = [grid.map[x][y] for y in range(grid.size)]
            weights[0] += self.check_line_monotonicity(row)

       
        for y in range(grid.size):
            col = [grid.map[x][y] for x in range(grid.size)]
            weights[1] += self.check_line_monotonicity(col)

        
        return min(weights)

    def check_line_monotonicity(self, line):
        
        
        current = 0
        next = current + 1
        while next < len(line):
            while next < len(line) and line[next] == 0:
                next += 1
            if next >= len(line): next -= 1
            currentValue = line[current]
            nextValue = line[next]
            if currentValue > nextValue:
                return nextValue - currentValue
            elif nextValue > currentValue:
                return currentValue - nextValue
            current = next
            next += 1
            
        return 0
    
    
    def calculate_smoothness(self, grid):
        UP_VEC = (-1, 0)
        DOWN_VEC = (1, 0)
        LEFT_VEC = (0, -1)
        RIGHT_VEC = (0, 1)
        directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC)
        
        smoothness = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] != 0:
                    value = grid.map[x][y]
                    for d in directionVectors:
                        target_x = x + d[0]
                        target_y = y + d[1]
                        while grid.crossBound((target_x, target_y)) and grid.map[target_x][target_y] == 0:
                            target_x += d[0]
                            target_y += d[1]
                        if grid.crossBound((target_x, target_y)):
                            target_value = grid.map[target_x][target_y]
                            smoothness -= abs(value - target_value)
        return smoothness

    def is_max_tile_in_corner(self, grid, max_tile):
       
        corners = [(0, 0), (0, grid.size-1), (grid.size-1, 0), (grid.size-1, grid.size-1)]
        for corner in corners:
            if grid.getCellValue(corner) == max_tile:
                return 1  
        return 0  
    
    def calculate_merge_potential(self, grid):
        UP_VEC = (-1, 0)
        DOWN_VEC = (1, 0)
        LEFT_VEC = (0, -1)
        RIGHT_VEC = (0, 1)
        directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC)
        
        
        merge_potential = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] != 0:
                    for d in directionVectors:
                        vector_x, vector_y = d
                        adj_x, adj_y = x + vector_x, y + vector_y
                        if grid.crossBound((adj_x, adj_y)):
                            if grid.map[x][y] == grid.map[adj_x][adj_y]:
                                merge_potential += 1
        return merge_potential
    
    def calculate_tile_gradient(self, grid):
        
        gradient = [
            [15, 14, 13, 12],
            [8, 9, 10, 11],
            [7, 6, 5, 4],
            [0, 1, 2, 3]
        ]
        score = 0
        for x in range(grid.size):
            for y in range(grid.size):
                score += grid.map[x][y] * gradient[x][y]
        return score

    def penalize_blocked_tiles(self, grid):
        UP_VEC = (-1, 0)
        DOWN_VEC = (1, 0)
        LEFT_VEC = (0, -1)
        RIGHT_VEC = (0, 1)
        directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC)
        
        penalty = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] != 0:
                    for d in directionVectors:
                        vector_x, vector_y = d
                        adj_x, adj_y = x + vector_x, y + vector_y
                        if grid.crossBound((adj_x, adj_y)):
                            adj_value = grid.map[adj_x][adj_y]
                            if adj_value < grid.map[x][y]:
                                penalty += grid.map[x][y] - adj_value
        return penalty


    def calculate_edge_maximization(self, grid):
       
        max_tile = grid.getMaxTile()
        edge_tiles = []
        for i in range(grid.size):
            edge_tiles.extend([grid.map[0][i], grid.map[grid.size-1][i], grid.map[i][0], grid.map[i][grid.size-1]])
        max_edge_tile = max(edge_tiles)
        return 1 if max_edge_tile == max_tile else 0

