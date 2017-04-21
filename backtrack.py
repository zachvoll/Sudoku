from constraints import *
from ac3 import *
from sudokuCSP import *
from sudokuGen import *
from copy import deepcopy
from math import ceil
from random import shuffle, randint
from time import time
from sys import setrecursionlimit

setrecursionlimit(10000)

'''
count node object for keeping a global value for testing 
and minimize global access delay by going with reference access
'''
class Count(object):
    def __init__(self, num = 0):
        self.num = num

#backtracking search
def backtracks(csp, inferType, pickType, count):
    result = backtrack({}, csp, inferType, pickType, count)
    if result:
        return result
    else:
        return None

#used to find all of the currently assigned variables
def findassignment(variables):

    assign = {}
    for value in variables.values():
        if(len(value.domain) == 1):
            assign[value.name] = value.domain[0]

    return assign

#find number of unassigned neighbors for a variable, used by degree heuristic
def consVal(assignment, cons):

    count = 0
    for neigh in cons:
        if neigh.var2 not in assignment:
            count += 1

    return count

#backtracking
def backtrack(assignment, csp, inferType, pickType, count):

    count.num += 1
    newvars,cons = deepcopy(csp)

    #check if we have a solution
    cspvars = set()
    for value in newvars.values():
        cspvars.add(value.name)

    assignvars = set(assignment.keys())

    #print("count", count.num, "assigned vars", len(assignvars))

    if(cspvars == assignvars):
        return assignment

    else:
        temp = sorted(list(cspvars - assignvars))
        convar = newvars[temp[0]]

        #find variable that has the most constraints with unassigned variables
        if(pickType == 'dh'):

            mostconst = consVal(assignment, convar.neighbors)

            for idx in temp:
                avar = newvars[idx]
                numcons = consVal(assignment, avar.neighbors)
                if mostconst < numcons:
                    mostconst = numcons
                    convar = avar

        #find variable with smallest domain
        elif(pickType == 'mrv'):

            mostconst = len(convar.domain)
            for idx in temp:

                avar = newvars[idx]
                asize = len(avar.domain)

                if mostconst > asize:
                    mostconst = asize
                    convar = avar

        #fetch reverse bc arcs.
        neighs = []
        for bc in convar.neighbors:
            if bc.var2.name not in assignment:
                neighcons = newvars[bc.var2.name].neighbors
                for nbc in neighcons:
                    if nbc.var2.name == convar.name:
                        neighs.append(nbc)

        olddom = deepcopy(newvars[convar.name].domain)
        for value in convar.domain:

            #add assignment
            assignment[convar.name] = value
            newvars[convar.name].domain = [value]
            newvars2,cons2 = deepcopy((newvars,cons))

            #check assignment consistency
            satisfied = True

            for bc in convar.neighbors:
                satisfied = False
                for y in bc.var2.domain:
                    satisfied = bc.func(value,y)
                    if satisfied:
                        break

                if not satisfied:
                    break

            if satisfied:
                #inference
                if(inferType == "fc"):
                    inf = FC(newvars, neighs)
                elif(inferType == "mac"):
                    inf = AC3(newvars, neighs)
                else:
                    inf = AC3(newvars, cons)

                if inf:
                    #get new assignment
                    newassign = {}
                    for value in newvars.values():
                        if(len(value.domain) == 1):
                            newassign[value.name] = value.domain[0]

                    result = backtrack(newassign, (newvars,cons), inferType, pickType, count)
                    if result:
                        return result

            #revert changes
            newvars,cons = newvars2,cons2
            newvars[convar.name].domain = olddom
            del assignment[convar.name]

    return None

#used for running experiments on sudoku
def testSudoku(puzzle, r, c, p, size, infType, pickType):

    init = Sudoku(puzzle, r, c)
    csp = init.setupCSP()

    newvars,cons = csp

    AC3(newvars, cons)
    count = Count()

    stime = time()
    finished = backtracks(csp, infType, pickType, count)
    etime = time()-stime

    if finished:

        print("time", etime)
        print("count", count.num)

        #create file name
        fname = str(infType) + " " + str(pickType) + " size " + str(size) +".txt"
        line = "time: " + str(etime) + ", calls: " + str(count.num) + " prefilled squares: " + str(p) + "\n"

        #write to file
        with open(fname, "a+") as myfile:
            myfile.write(line)

        line = "-"*(size*2+2)

        for row in range(size):
            if(row%r == 0):
                print(line)

            for col in range(size):
                if(col%c == 0):
                    print('|', end = '')

                print(finished[(row,col)], end = ' ')

            print('')

    else:
        print("NONE--------------------")
        printBoard(puzzle)
        print("------------------------")

    return finished

if __name__ == '__main__':

    p1 = [[0,0,0,0,0,0],[0,0,0,0,0,6],[4,0,0,0,0,3],[0,0,0,0,0,4],[6,3,0,0,2,0],[0,2,0,0,3,1]]

    p2 = [[0,0,0,4],[0,0,3,0],[0,2,0,0],[1,0,2,0]]

    p3 = [[0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0]]

    p4 = [[3,0,4,0,0,0,0,0,0],
          [0,5,0,0,0,3,0,6,0],
          [0,0,0,0,0,5,0,0,9],
          [0,0,0,3,0,6,1,7,0],
          [1,0,0,0,9,0,0,0,8],
          [0,6,2,4,0,8,0,0,0],
          [2,0,0,7,0,0,0,0,0],
          [0,1,0,8,0,0,0,4,0],
          [0,0,0,0,0,0,8,0,5]]

    r = 2
    c = 4
    n = r*c
    p = ceil((n**2)/4)

    for i in range(0, 3):
        board = None
        while not board:
            board = makeBoard(r, c, n, p)
        testSudoku(board, r, c, p, n, 'fc', 'dh')
