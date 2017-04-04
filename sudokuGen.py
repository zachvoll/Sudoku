# Author: Zachary Vollen

from copy import deepcopy
import random

def printBoard(board):
    for row in board:
        print(row)

def printDict(adict):
    for key, value in adict.items():
        print(key, value)

def reviseG(domain1, domain2):

	# copy domains for use with iteration (they might change inside the for loops)
	dom1 = deepcopy(domain1)
	dom2 = deepcopy(domain2)

	revised = False
	for x in dom1:
		satisfied = False
		for y in dom2:
			satisfied = (x != y)
			if satisfied:
				break
		if not satisfied:
			domain1.remove(x)
			revised = True

	return revised

def AC3G (domains, boxes, constraints):

    arcs = deepcopy(constraints)
    while arcs:
        var1,var2 = arcs.pop()
        d1 = domains[var1]
        d2 = domains[var2]

        if reviseG(d1, d2):
            if len(d1) == 0:
                return False

            neighbors = boxes[var1]

            for neigh in neighbors:
                if neigh != var2:
                    arcs.append((neigh,var1))

    return True


#generates a random board given r,c,n,p
def makeBoard(r, c, p):
    board = []
    boxes = dict()
    domains = dict()
    rqfill = []
    n = r*c

    #error checking
    if(r*c != n):
        print("invalid dimensions")
        return None

    if(n**2 < p):
        print("too many prefilled squares")
        return None

    #construct blank board and each cell's neighbors
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0)
            rqfill.append((i,j))
            boxes[(i,j)] = set()
            domains[(i,j)] = set([i for i in range(1,n+1)])
            ri = (i//r)*r
            cj = (j//c)*c

            #boxes
            for bi in range(ri,ri+r):
                for bj in range(cj,cj+c):
                    boxes[(i,j)].add((bi,bj))

            #rows
            for roj in range(n):
                boxes[(i,j)].add((i,roj))

            for roi in range(n):
                boxes[(i,j)].add((roi,j))

            boxes[(i,j)].remove((i,j))

        board.append(row)

    boxes = {key: sorted(list(value)) for key,value in boxes.items()}


    #generate constraints
    constraints = []
    for idx in rqfill:
        neighs = boxes[idx]
        for neigh in neighs:
            constraints.append((idx,neigh))

    #make index fill selection random
    random.shuffle(rqfill)

    #construct board
    aboard = fillBoard(board, boxes, domains, rqfill, p, constraints)

    return aboard

def fillBoard(board, boxes, domains, rqfill, prefilled, constraints):

    nboard = deepcopy(board)
    ndomains = deepcopy(domains)
    nrqfill = deepcopy(rqfill)

    if prefilled == 0:
        return nboard

    else:
        #randomly fill squares
        (au,bu) = nrqfill.pop()
        neighs = boxes[(au,bu)]
        numbers = list(ndomains[(au,bu)])
        random.shuffle(numbers)

        for number in numbers:
            good = True
            for (i,j) in boxes[(au,bu)]:
                ndom = ndomains[(i,j)]
                if (len(ndom) == 1) and number in ndom:
                    good = False
                    break

            if good:
                #assign value
                nboard[au][bu] = number
                prefilled -= 1

                #save the old domains just in case
                olddoms = deepcopy(ndomains)

                #update domains
                ndomains[(au,bu)] = {number}
                for (i,j) in boxes[(au,bu)]:
                    if number in ndomains[(i,j)]:
                        ndomains[(i,j)].remove(number)

                good2 = AC3G(ndomains, boxes, constraints)
                if good2:
                    #recursive call
                    result = fillBoard(nboard, boxes, ndomains, nrqfill, prefilled, constraints)
                    if result:
                        return result

                else:
                    #remove value
                    board[au][bu] = 0
                    prefilled += 1

                    #revert domains
                    domains = olddoms

        return None
