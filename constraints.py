import itertools
from itertools import product

'''
'a list->string->ConstraintVar

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

'''
class UnaryConstraint:
    def __init__(self, v, fn):
        self.var = v
        self.func = fn

'''
ConstraintVar->ConstraintVar->('a->'a->bool)->BinaryConstraint

'''
class BinaryConstraint:
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn

'''

'''
def nodeConsistent(uc):
    domain = list(uc.var.domain)
    for x in domain:
        if (not uc.func(x)):
            uc.var.domain.remove(x)

