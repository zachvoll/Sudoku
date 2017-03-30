from constraints import *

class Sudoku(object):

    def getBox(self, i, j):

        ri = (i // self.r) * self.r
        cj = (j // self.c) * self.c

        neighs = []

        for ni in range(ri,ri+self.r):
            for nj in range(cj,cj+self.c):
                neighs.append((ni,nj))

        return neighs

    def __init__(self, puzzle, r, c):
        self.size = r*c
        self.r = r
        self.c = c
        self.puzzle = puzzle

    def setupCSP(self):
        thevars = [ (x, y) for x in range(self.size) for y in range(self.size) ]
        variables = dict()

        for var in thevars:
            variables[var] = ConstraintVar([i for i in range(1, self.size+1)], var)

        constraints = list()

        different = lambda x,y: x != y

        for i in variables:
            for j in variables:
                # If two distinct cells are in the same row or column must be different
                if ( i != j and (i[0] == j[0] or i[1] == j[1] or self.getBox(i[0],i[1]) == self.getBox(j[0],j[1]) ) ) :
                    constraints.append(BinaryConstraint(variables[i], variables[j], different))

        #domain reduction
        for i in range(self.size):
            for j in range(self.size):
                value = self.puzzle[i][j]
                if value != 0:
                    nodeConsistent( UnaryConstraint(variables[(i,j)], lambda x: x == value) )

        for var in variables:
            variables[var].initNeighbours(constraints)

        return (variables, constraints)
