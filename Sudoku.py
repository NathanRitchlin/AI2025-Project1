import numpy

def checkPuzzle(p):
    correctNums = [1,2,3,4,5,6,7,8,9]

    #checks if puzzle passes row rule
    for row in range(9):
        nums = []
        for column in range(9):
            nums.append(int(p[row][column]))
        if nums != correctNums:
            return False

    #checks if puzzle passes column rule
    for column in range(9):
        nums = []
        for row in range(9):
            nums.append(int(p[row][column]))
        if nums != correctNums:
            return False

    #checks if puzzle passes 3x3 grid rules
    for i in range(3):
        for j in range(3):
            nums = []
            for row in range(0+(i*3), (i*3)+3):
                for column in range(0+(j*3), (j*3)+3):
                    nums.append(int(p[row][column]))
            if nums != correctNums:
                return False

    return True


puzzle = numpy.empty((9,9), dtype = int)
for i in range(9):
    for j in range(9):
        puzzle[i][j] = i

check = numpy.array()
print(puzzle)
checkPuzzle(puzzle)

