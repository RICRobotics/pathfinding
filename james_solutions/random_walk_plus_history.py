from maze import neighbors, show, run


def solve(grid, start, goal):

    # must return a list of squares going from start to goal, like [(1, 1), (2, 1), (3, 1), ...]

    # squares are (row, col). things you can use:
    # neighbors(grid, square)  ->  list of open squares next to it (up, down, left, right)
    # grid[row][col]           ->  '#' wall, ' ' open, 'S' start, 'G' goal
    # show(grid, path)

    import random

    path = [start]
    visited = {start}

    while path[-1] != goal:
        # add a step before random choice: only choose a step if it hasn't been visited yet..
        options = [n for n in neighbors(grid, path[-1])]
        options = [n for n in options if n not in visited]
        
        if not options:
            return []
        
        # better history implimentation
        # if not options:
        #     path.pop() # dead end, so back track
        #     if not path: # if theres no other option:
        #         return []
        #     continue # you need to do this so that you dont sample from the old options
            
        
        next_move = random.choice(options)

        visited.add(next_move)
        path.append(next_move)

    return path


run(solve)
