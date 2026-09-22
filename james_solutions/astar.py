import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from maze import neighbors, show, run

# a*, but a lzay implimentation. its basically bfs, but it uses manhatten distance to tie break
# note that knowing where the goal is is not assumed for all situations!


def manhattan(square, goal):
    # manhattan distance - how many steps it'd take if there were no walls
    return abs(square[0] - goal[0]) + abs(square[1] - goal[1])


def solve(grid, start, goal):

    def score(path):
        # this is the real A* logic: score a possible path by predicted len: path len + distance
        steps_taken = len(path)
        steps_left = manhattan(path[-1], goal)
        return(steps_taken + steps_left)

    hydra_heads = [[start]]  # all not-finished paths
    visited = {start} # keep track of visited. same reason we added it to random walk..

    while hydra_heads:
        # bfs would just grow the shortest head here
        path = min(hydra_heads, key=score)
        hydra_heads.remove(path)

        if path[-1] == goal:
            return path

        # add a new hydra head for every possible path
        for n in neighbors(grid, path[-1]):
            if n not in visited:
                visited.add(n)
                hydra_heads.append(path + [n])

    return []


run(solve)
