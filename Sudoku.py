import numpy
GROUP_ID = 'Group04'
ALGORITHM = 'bt'
PUZZLE_TYPE = 'easy'
PUZZLE_PATH = 'puzzles/Easy-P1.txt'


def checkPuzzle(p):

    #checks if puzzle passes row rule
    for row in range(9):
        nums = []
        for column in range(9):
            nums.append(p[row][column])
        newNums = [item for item in nums if item != "?"]
        setNums = set(newNums)
        if len(newNums) > len(setNums):
            print("Fails to pass row rule")
            return False


    #checks if puzzle passes column rule
    for column in range(9):
        nums = []
        for row in range(9):
            nums.append(p[row][column])
        newNums = [item for item in nums if item != "?"]
        setNums = set(newNums)
        if len(newNums) > len(setNums):
            print("Fails to pass column rule")
            return False

    #checks if puzzle passes 3x3 grid rules
    for i in range(3):
        for j in range(3):
            nums = []
            for row in range(0+(i*3), (i*3)+3):
                for column in range(0+(j*3), (j*3)+3):
                    nums.append(p[row][column])
            newNums = [item for item in nums if item != "?"]
            setNums = set(newNums)
            if len(newNums) > len(setNums):
                print("Fails to pass 3x3 rule")
                return False

    return True

#Processes the sudoku file into a numpy array
arr = []
with open(PUZZLE_PATH, 'r') as file:
    firstLine = True
    for line in file:
        processedLine = line.rstrip('\n')
        if(firstLine):
            row = processedLine[3:].split(",")
            firstLine = False
        else:
            row = processedLine.split(",")
        arr.append(row)
    file.close()
puzzle = numpy.array(arr)


puzzle[6][2] = '6'
print(puzzle)
print("\n")
checkPuzzle(puzzle)

#Writing the finished puzzle to a file
fileName = GROUP_ID + '_' + ALGORITHM + "_" + PUZZLE_TYPE + "_" + PUZZLE_PATH.lstrip("puzzles/")
with open(fileName, 'w') as file:
    for row in range(9):
        for column in range(8):
            file.write(puzzle[row][column] + ",")
        file.write(puzzle[row][8] + '\n')


    file.close()

