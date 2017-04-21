import itertools
from itertools import product

'''
'a list->string->ConstraintVar
A constraint variable with a domain (possible legal values), name (index identifier), 
and neighbors (those cells that share a row, column, or box)
'''
class ConstraintVar:
    def __init__(self, d, n ):
        self.domain = [ v for v in d ]
        self.name = n
        self.neighbors = []

    # call AFTER all constraints have been made
    def initNeighbours(self, constraints):
        for bc in constraints:
            if bc.var1.name == self.name:
                self.neighbors.append(bc)
'''
ConstraintVar->('a -> bool)->UnaryConstraint
Unary Constraint is used to constrain initialized sudoku cells to reduce potential values.
'''
class UnaryConstraint:
    def __init__(self, v, fn):
        self.var = v
        self.func = fn

'''
ConstraintVar->ConstraintVar->('a->'a->bool)->BinaryConstraint
Binary Constraints are relationships between neighbors based on a function.
In this case it's that neighbors can't be equal to each other.
'''
class BinaryConstraint:
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn

'''
Used to reduce the initial domains of cells due to preassigned cells.
'''
def nodeConsistent(uc):
    domain = list(uc.var.domain)
    for x in domain:
        if (not uc.func(x)):
            uc.var.domain.remove(x)

