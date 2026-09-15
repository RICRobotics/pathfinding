from maze import neighbors, show, run


def solve(grid, start, goal):

    # must return a list of squares going from start to goal, like [(1, 1), (2, 1), (3, 1), ...]

    # squares are (row, col). things you can use:
    # neighbors(grid, square)  ->  list of open squares next to it (up, down, left, right)
    # grid[row][col]           ->  '#' wall, ' ' open, 'S' start, 'G' goal
    # show(grid, path)

    show(grid, [])
    print(neighbors(grid, (1, 1)))

    return []


run(solve)
