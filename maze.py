# shared stuff for the maze solvers - no need to touch
# in your own file:
#     from maze import neighbors, run
#     def solve(grid, start, goal): ...
#     run(solve)

def neighbors(grid, square):
    row, col = square
    result = []
    # just check each of up, down, left right, and if in bounds and not wall, save
    for r, c in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if 0 <= r < len(grid) and 0 <= c < len(grid[r]) and grid[r][c] != "#":
            result.append((r, c))
    return result


def load(text):
    """turn maze text into a grid (a list of rows) and find S and G"""
    grid = [list(line) for line in text.strip("\n").split("\n")]
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                start = (row, col)
            if grid[row][col] == "G":
                goal = (row, col)
    return grid, start, goal


def show(grid, path):
    # prints the grid - ignore
    for row in range(len(grid)):
        line = ""
        for col in range(len(grid[row])):
            if (row, col) in path and grid[row][col] == " ":
                line += "."
            else:
                line += grid[row][col]
        print(line)


MAZE = """
########
#S   # #
# ## # #
#  #   #
## # # #
#    # #
# ##  G#
########
"""

def run(solve):
    grid, start, goal = load(MAZE)
    path = solve(grid, start, goal)
    show(grid, path)
    solved = True
    for i in range(len(path)-1):
        if path[i+1] not in neighbors(grid, path[i]):
            solved = False
            break
    if path[0] != start or path[-1] != goal: solved = False
    print("solved" if solved else "not solved")
    print(len(path))
