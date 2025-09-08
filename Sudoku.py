import copy

import numpy
from nbformat.sign import algorithms

GROUP_ID = 'Group04'
ALGORITHM = 'bt'
PUZZLE_TYPE = 'easy'
PUZZLE_PATH = 'puzzles/Easy-P2.txt'

#prints the sudoku puzzle, used for debugging
def printPuzzle(puzzle):
    for row in range(9):
        for column in range(8):
            print(puzzle[row][column].value + ",", end = "")
        print(puzzle[row][8].value)
    print("\n")

#class for each tile on the board which holds information about the tile's position, value, if it is fixed or not, and its domain
class sudokuTile:
    def __init__(self, pos, val, layer):
        self.position = pos
        self.layer = layer
        self.value = val
        self.fixed = True
        if val == '?':
            self.fixed = False
            self.domain = ['1','2','3','4','5','6','7','8','9']
        else:
            self.domain = [val]

def checkPuzzle(p):
    #checks if puzzle passes row rule
    for row in range(9):
        nums = []
        for column in range(9):
            nums.append(p[row][column].value)
        newNums = [item for item in nums if item != "?"]
        setNums = set(newNums)
        if len(newNums) > len(setNums):
            #print("Fails to pass row rule")
            return False


    #checks if puzzle passes column rule
    for column in range(9):
        nums = []
        for row in range(9):
            nums.append(p[row][column].value)
        newNums = [item for item in nums if item != "?"]
        setNums = set(newNums)
        if len(newNums) > len(setNums):
            #print("Fails to pass column rule")
            return False

    #checks if puzzle passes 3x3 grid rules
    for i in range(3):
        for j in range(3):
            nums = []
            for row in range(0+(i*3), (i*3)+3):
                for column in range(0+(j*3), (j*3)+3):
                    nums.append(p[row][column].value)
            newNums = [item for item in nums if item != "?"]
            setNums = set(newNums)
            if len(newNums) > len(setNums):
                #print("Fails to pass 3x3 rule")
                return False

    return True

#Simple backtracking algorithm using a stack
def backTracking(puzzle):
    #setting up the stack with the inital possible values for the first tile
    stack = [(puzzle[0][0], d) for d in puzzle[0][0].domain]
    layer = 0
    steps = 0
    while len(stack) > 0:
        # pop the top value off of the stack, and set the given tile's value to the given value
        prevLayer = layer
        steps += 1
        action = stack.pop()
        tile = action[0]
        val = action[1]
        tile.value = val
        # if the value is valid for the puzzle, add all the possible values for the next position on the board to the stack
        if (checkPuzzle(puzzle)):
            layer = tile.layer + 1
            # puzzle has been solved
            if (layer == 81):
                break
            row = layer // 9
            col = layer % 9
            nextTile = puzzle[row][col]
            for d1 in nextTile.domain:
                stack.append((nextTile, d1))
        # if the value is not valid, set the tile back to an unknown, and don't continue searching that path (prune said branch)
        else:
            if (not tile.fixed):
                layer = tile.layer
                tile.value = '?'

        # when backtracking, cleanup all unfixed tiles by turning them back into unknowns
        if (prevLayer > layer):
            for i in range(layer + 1, prevLayer):
                row = i // 9
                col = i % 9
                resetTile = puzzle[row][col]
                if not (resetTile.fixed):
                    resetTile.value = '?'

            # fix for edge case where puzzle couldn't backtrack to '1' in the starting square
            if (len(stack) == 0 and puzzle[0][0].value == '?'):
                puzzle[0][0].value = '1'
                nextTile = puzzle[0][1]
                for d1 in nextTile.domain:
                    stack.append((nextTile, d1))
    return puzzle, steps

#Backtracking algorithm with one-step forward checking
def forwardChecking(puzzle):
    #setting up the stack with the inital possible values for the first tile
    stack = [(puzzle[0][0], d) for d in puzzle[0][0].domain]
    layer = 0
    steps = 0
    while len(stack) > 0:
        # pop the top value off of the stack, and set the given tile's value to the given value
        prevLayer = layer
        steps += 1
        action = stack.pop()
        tile = action[0]
        val = action[1]
        tile.value = val
        # if the value is valid for the puzzle, add all the possible values for the next position on the board to the stack
        if (checkPuzzle(puzzle)):
            layer = tile.layer + 1
            # puzzle has been solved
            if (layer == 81):
                break
            row = layer // 9
            col = layer % 9
            nextTile = puzzle[row][col]
            #Changed for forwardTracking-- edits the domain of the next tile if value of current one interferes(same row)
            if(tile.position[0] == nextTile.position[0]):
                checkedDomain = [num for num in nextTile.domain if num != val]
            else:
                checkedDomain = nextTile.domain
            #If there are no numbers in the new domain, the value for the given tile is not possible
            if(len(checkedDomain) == 0):
                layer = tile.layer
                if (not tile.fixed):
                    tile.value = '?'
            for d1 in checkedDomain:
                stack.append((nextTile, d1))
        # if the value is not valid, set the tile back to an unknown, and don't continue searching that path (prune said branch)
        else:
            layer = tile.layer
            if (not tile.fixed):
                tile.value = '?'

        # when backtracking, cleanup all unfixed tiles by turning them back into unknowns
        if (prevLayer > layer):
            for i in range(layer + 1, prevLayer):
                row = i // 9
                col = i % 9
                resetTile = puzzle[row][col]
                if not (resetTile.fixed):
                    resetTile.value = '?'

            # fix for edge case where puzzle couldn't backtrack to '1' in the starting square
            if (len(stack) == 0 and puzzle[0][0].value == '?'):
                puzzle[0][0].value = '1'
                nextTile = puzzle[0][1]
                for d1 in nextTile.domain:
                    stack.append((nextTile, d1))
    return puzzle, steps

if __name__ == "__main__":
    #Processes the sudoku file into a numpy array of sudokuTile objects
    arr = []
    layer = 0
    with open(PUZZLE_PATH, 'r') as file:
        firstLine = True
        rowNum = 0
        for line in file:
            colNum = 0
            processedLine = line.rstrip('\n')
            if(firstLine):
                row = processedLine[3:].split(",")
                firstLine = False
            else:
                row = processedLine.split(",")
            tileRow = []
            for num in row:
                tile = sudokuTile([rowNum, colNum], num, layer)
                layer += 1
                tileRow.append(tile)
                colNum += 1
            arr.append(tileRow)
            rowNum += 1
        file.close()
    puzzle = numpy.array(arr)
    originalPuzzle = copy.deepcopy(puzzle)
    if(ALGORITHM == 'bt'):
        solvedPuzzle, steps = backTracking(puzzle)
    elif(ALGORITHM == 'fc'):
        solvedPuzzle, steps = forwardChecking(puzzle)
    print(ALGORITHM)
    print(PUZZLE_PATH)
    print("=====================")
    print("Original Puzzle: ")
    printPuzzle(originalPuzzle)
    print("Solved Puzzle in", steps, "steps:")
    printPuzzle(solvedPuzzle)


    #Writing the finished puzzle to a file
    fileName = GROUP_ID + '_' + ALGORITHM + "_" + PUZZLE_TYPE + "_" + PUZZLE_PATH.lstrip("puzzles/")
    with open(fileName, 'w') as file:
        for row in range(9):
            for column in range(8):
                file.write(puzzle[row][column].value + ",")
            file.write(puzzle[row][8].value + '\n')
        file.close()


