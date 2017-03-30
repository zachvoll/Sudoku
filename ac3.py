from copy import deepcopy

# The revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
# A single BinaryConstraint instance is passed in to this function.
def revise( bc ):

	dom1 = list(bc.var1.domain)
	dom2 = list(bc.var2.domain)

	revised = False
	for x in dom1:
		satisfied = False
		for y in dom2:
			satisfied = bc.func(x,y)
			if satisfied:
				break
		# the loop exited naturally; no value y in dom2 allows (x,y) to satisfy bc
		if not satisfied:
			bc.var1.domain.remove(x)
			revised = True
	return revised

def AC3 (variables, constraints):

	arcs = list(constraints)
	while arcs:
		bc = arcs.pop()
		if revise( bc ):
			if len(bc.var1.domain) == 0:
				return False

			neighbors = bc.var1.neighbors
			xjn = bc.var2.name

			for neighbourCon in neighbors:
				for constraint in neighbourCon.var2.neighbors:
					if (constraint.var2.name == neighbourCon.var1.name) and (constraint.var1.name != xjn):
						arcs.append(constraint)

	return True

def FC ( variables, constraints ):
	arcs = set( constraints )

	while arcs:
		bc = arcs.pop()
		if revise( bc ):
			if len(bc.var1.domain) == 0:
				return False

			neighbors = bc.var1.neighbors
			neighbors.remove(bc)

	return True
