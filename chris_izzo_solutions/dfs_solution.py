from maze import neighbors, run

    # must return a list of squares going from start to goal, like [(1, 1), (2, 1), (3, 1), ...]

    # squares are (row, col). things you can use:
    # neighbors(grid, square)  ->  list of open squares next to it (up, down, left, right)
    # grid[row][col]           ->  '#' wall, ' ' open, 'S' start, 'G' goal
    # show(grid, path)

def solve(grid, start, goal):
    path = solveRec([], set(), grid, start, goal)[0]
    path.append(start)
    path.reverse()
    return path

def solveRec(path, visited, grid, start, goal):
    visited.add(start)
    adj = neighbors(grid, start)
    if goal in adj:
        return [goal], goal
    for sq in adj:
        if sq in visited: 
            continue
        path, end = solveRec(path, visited, grid, sq, goal)
        if end == goal:
            path.append(sq)
            return path, end 
    return None, None

run(solve)
