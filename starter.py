from maze import neighbors, show, run
import random

def randPath(grid, start, goal):
    path = [start]
    while True:
        valid = neighbors(grid, path[len(path)-1])
        move = valid[random.randint(0, len(valid) - 1)]
        path.append(move)
        if (move == goal):
            break
    
    return path

# Finds the goal like a plant would
def rootPath(grid, start, goal):
    poses = []
    posesRemaining = []
    depth = 0
    traversed = []

    posesRemaining.append(1)
    poses.append([start])

    path = []

    pathFound = False

    done = False
    while (not done):
        if (depth < 0):
            done = True
            continue

        index = posesRemaining[depth] - 1
        pos = poses[depth][index]

        traversed.append(pos)

        if (pos == goal):
            pathFound = True

        if (pathFound):
            path.insert(0, pos)
            depth -= 1
            continue

        
        
        valid = neighbors(grid, pos)
        
        for traversed_place in traversed:
            for potential_place in valid:
                if (traversed_place == potential_place):
                    valid.remove(potential_place)

        if (valid):
            depth += 1
            if len(poses) < depth+1:
                poses.append(valid)
            else:
                poses[depth] = valid

            if len(posesRemaining) < depth+1:
                posesRemaining.append(len(valid))
            else:
                posesRemaining[depth] = len(valid)
            
        elif index > 0:
            posesRemaining[depth] -= 1
        else:
            depth -= 1

    return path

class PosInfo:
    pos = (0, 0)
    origin = -1
    def __init__(self, pos, origin):
        self.pos = pos
        self.origin = origin

# Finds the goal like a tentacle would
def rootRandPath(grid, start, goal):
    poses = []
    posesRemainingIndex = []
    depth = 0
    traversed = []

    posesRemainingIndex.append([0])
    poses.append([PosInfo(start, -1)])

    path = []

    pathFound = False

    done = False
    loop = 0
    while (not done):
        loop += 1
        #print(depth)
        if (depth < 0):
            done = True
            continue

        if len(posesRemainingIndex[depth]) <= 0:
            depth -= 1
            continue

        remainingIndex = random.randint(0, len(posesRemainingIndex[depth])-1)
        
        index = posesRemainingIndex[depth].pop(remainingIndex)

        position = poses[depth][index]
        #print(position.pos)

        traversed.append(position.pos)

        if (position.pos == goal):
            pathFound = True

        if (pathFound):
            done = True
            while (True):
                path.insert(0, position.pos)
                if (position.origin >= 0):
                    depth -= 1
                    position = poses[depth][position.origin]
                else:
                    break
            break

        
        
        valid = neighbors(grid, position.pos)
        
        for traversed_place in traversed:
            for potential_place in valid:
                if (traversed_place == potential_place):
                    valid.remove(potential_place)

        if (valid):

            #print("(",loop, ",", depth, ",", index, ") and ", position.pos, " also ", position.origin)
            #print(valid)

            depth += 1
            if len(poses) <= depth:
                poses.append([])
            poses[depth] = []
            
            for potential_place in valid:
                poses[depth].append(PosInfo(potential_place, index))

            if len(posesRemainingIndex) <= depth:
                posesRemainingIndex.append([])
            posesRemainingIndex[depth] = list(range(0,len(valid)))

            #print(depth,posesRemainingIndex[depth],"|", valid)


    return path

# FInds the goal by flooding the grid
def fillPath(grid, start, goal):
    poses = []
    posesRemaining = []
    depth = 0
    traversed = [start]

    posesRemaining.append(1)
    poses.append([PosInfo(start, -1)])
    
    path = []

    pathFound = False

    done = False

    loop = 0

    while (not done):
        loop += 1
        index = posesRemaining[depth] - 1
        position = poses[depth][index]

        if (position.pos == goal):
            pathFound = True

        if (pathFound):
            done = True
            while (True):
                path.insert(0, position.pos)
                if (position.origin >= 0):
                    depth -= 1
                    position = poses[depth][position.origin]
                else:
                    break
            break
        
        valid = neighbors(grid, position.pos)

        valid = valid[::-1]
        
        for traversed_place in traversed:
            for potential_place in valid:
                if (traversed_place == potential_place):
                    valid.remove(potential_place)

        if (valid):
            depth += 1
            if (len(poses) <= depth):
                poses.append([])

            for potential_place in valid:

                poses[depth].append(PosInfo(potential_place, index))
                traversed.append(potential_place)

            if (len(posesRemaining) <= depth):
                posesRemaining.append(0)

            posesRemaining[depth] = len(poses[depth])

            depth -= 1
            
            #print("(",loop, ",", depth, ",", index, ") and ", position.pos, " also ", position.origin)
            #print(valid)
            
        posesRemaining[depth] -= 1

        if (posesRemaining[depth] <= 0):
            depth += 1

        if (len(posesRemaining) <= depth):
            done = True
            break

    return path

# Finds all paths and stores the winning ones
# time complexity is O(2^n * n) where n is the number of branches so really bad in open spaces
def rootCoolPath(grid, start, goal):
    poses = []
    posesRemainingIndex = []
    depth = 0
    traversed = []

    posesRemainingIndex.append([0])
    poses.append([PosInfo(start, -1)])

    paths = []

    pathFound = False

    done = False
    loop = 0
    pathsFound = 0
    pathDescent = False
    pathDescentPos = 0
    while (not done):
        loop += 1

        if (pathsFound >= 1000):
            done = True
            break

        if (depth < 0):
            done = True
            continue

        if len(posesRemainingIndex[depth]) <= 0:
            depth -= 1
            if (len(traversed) > 0):
                traversed.pop()
            continue

        remainingIndex = 0
        
        index = posesRemainingIndex[depth].pop(remainingIndex)

        position = poses[depth][index]
        #print(position.pos)
        #print("(",loop, ",", depth, ",", index, ") and ", position.pos, " also ", position.origin)
        
        traversed.append(position.pos)

        #show(grid, traversed)

        if (position.pos == goal):
            pathFound = True

        if (pathFound):
            traversed.pop()
            #print("path found")
            pathsFound += 1
            path = []
            pathDepth = depth

            while (True):
                path.insert(0, position.pos)
                if (position.origin >= 0):
                    pathDepth -= 1
                    position = poses[pathDepth][position.origin]
                else:
                    paths.append(path)
                    break
            pathFound = False
            #print(path)
            #show(grid, path)

            continue

        
        
        valid = neighbors(grid, position.pos)
        
        for traversed_place in traversed:
            for potential_place in valid:
                if (traversed_place == potential_place):
                    valid.remove(potential_place)

        if (valid):
            #print(valid)

            depth += 1
            if len(poses) <= depth:
                poses.append([])
            poses[depth] = []
            
            for potential_place in valid:
                poses[depth].append(PosInfo(potential_place, index))

            if len(posesRemainingIndex) <= depth:
                posesRemainingIndex.append([])
            posesRemainingIndex[depth] = list(range(0,len(valid)))

            #print(depth,posesRemainingIndex[depth],"|", valid)
        else:
            traversed.pop()
            #print("dead end")

    if (len(paths) <= 0):
        return []

    #pathIndex = random.randint(0, len(paths)-1)
    finalPath = []
    for path in paths:
        for pos in path:
            if pos not in finalPath:
                finalPath.append(pos)
    
    print(len(paths))
    return finalPath

# Actually really dumb
def randSmartPath(grid, start, goal):
    path = [start]
    for i in range(0, 10000):
        valid = neighbors(grid, path[len(path)-1])
        for j in range(0, len(path)-1):
            for place in valid:
                if (place == path[j]):
                    valid.remove(place)
        if (len(valid) <= 0):
            path = []
            break
        move = valid[random.randint(0, len(valid) - 1)]
        path.append(move)
        if (move == goal):
            break
    
    return path

# combines the efficiencies of multiple paths into one path
# can be used on a single path if there are self intersections (randPath)
def pathOptimizer(paths, grid, start, goal):
    #paths = []
    #pathsCount = 5
    #for i in range(pathsCount):
        #paths.append(randPath(grid, start, goal))
    traversed = []
    potential_traversed = []
    #pathIndex = [0] * len(paths)
    index = 0
    choosenPath = -1
    done = False
    dontAdd = True
    loop = 0
    #for path in paths:
        #show(grid, path)
    while not done:
        loop += 1
        dontAdd = False
        for i in range(len(paths)):
            for j in range(len(traversed)):
                if paths[i][index] == goal:
                    choosenPath = i
                    done = True
                    break
                elif (paths[i][index] == traversed[j].pos):
                    #print("compare start")
                    #print(i,index,loop)
                    #print(traversed[j].pos)

                    travPos = []
                    travInd = []
                    for trav in traversed:
                        travPos.append(trav.pos)
                        travInd.append(trav.origin)

                    #print(len(traversed))
                    #print(travPos)
                    #print(travInd)

                    bumpedPathIndex = traversed[j].origin[0] #There could be multiple paths at this pos, but if that is the case, they must all be the same length, so it doesn't matter which you choose
                    bumpedPosIndex = paths[bumpedPathIndex].index(traversed[j].pos)
                    
                    #show(grid, paths[i][:index+1])
                    #show(grid, paths[bumpedPathIndex][:bumpedPosIndex+1])
                    #show(grid, paths[bumpedPathIndex][:index+1])

                    if (bumpedPosIndex == index):
                        #print("skipped")
                        continue
                    
                    paths[i] = paths[bumpedPathIndex][:bumpedPosIndex+1] + paths[i][index+1:]
                    distance = index - bumpedPosIndex
                    #print("new path")
                    #show(grid, paths[i])

                    traversed = []
                    for k in range(len(paths)):
                        for l in range(bumpedPosIndex+1):
                            potential_traversed.append(PosInfo(paths[k][l],k))
                    
                    index = bumpedPosIndex
                    dontAdd = True
                    break

            if not dontAdd:
                potential_traversed.append(PosInfo(paths[i][index], i))
            if (done):
                break
        if (done):
            break
        for potential in potential_traversed:
            inTraversed = False
            for j in range(len(traversed)):
                if (potential.pos == traversed[j].pos):
                    traversed[j].origin.append(potential.origin)
                    inTraversed = True
                    break
            if (not inTraversed):
                traversed.append(PosInfo(potential.pos, [potential.origin]))
        potential_traversed = []
        index += 1
        #if (loop >= 10000):
            #break

    #for path in paths:
        #show(grid, path)
    
    if choosenPath >= 0:
        return paths[choosenPath]
    return []

def solve(grid, start, goal):

    # must return a list of squares going from start to goal, like [(1, 1), (2, 1), (3, 1), ...]

    # squares are (row, col). things you can use:
    # neighbors(grid, square)  ->  list of open squares next to it (up, down, left, right)
    # grid[row][col]           ->  '#' wall, ' ' open, 'S' start, 'G' goal
    # show(grid, path)
    paths = []
    pathsCount = 10
    for i in range(pathsCount):
        paths.append(rootRandPath(grid, start, goal))
    #one randPath and one rootRandPath give suprisingly optimized results
    #paths.append(randPath(grid, start, goal))

    path = pathOptimizer(paths,grid, start, goal)#rootRandPath(grid, start, goal)
    #show(grid, path)

    #show(grid, [])
    #print(neighbors(grid, (1, 1)))

    return path


run(solve)
