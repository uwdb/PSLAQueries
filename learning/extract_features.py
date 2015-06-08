from plans import MyriaPlan
from plans import MyriaOperator
from plans import MyriaFragment	
import random
import json
import os


path = "/Users/jortiz16/Documents/queryFeaturesPostgres/MyriaFeatures/synqueries1"
queriesInPath = os.listdir(path)

f = open('outputFeatures', 'w')

for currentFile in queriesInPath:
	filePath = os.path.join(path, currentFile)
	raw = open(filePath).read()
	queryID = currentFile.replace("json", "").replace(".", "")
	print currentFile
	if raw:
		json_data = json.loads(raw)
		plan = MyriaPlan(json_data)
		#count operatators and fills the mapper
		operatorMap = {}
		jsonOp = ['Scan', 'Insert', 'Shuffle', 'Sink', 'Join', 'Producer', 'Consumer']
		for op in jsonOp:
			if op not in operatorMap:
				operatorMap[op] = 0
			for fragments in plan.fragments:
				for operator in fragments.operators:
					if op in operator.type:
						operatorMap[op] = operatorMap.get(op) + 1
		#iterate mapper object to get final counts
		finalLine = str(queryID) + ','
		for key in operatorMap:
			finalLine = finalLine  + str(operatorMap.get(key)) + ','
		f.write(finalLine + '\n')
	else:
		f.write(str(queryID) + ',0,0,0,0,0,0,0' + '\n')
f.close()

#figure out the shuffle situation divide by the number of workers
cardFile = open('synCardinalities', 'r')
workers = 4
outCard = open('shuffleCardinalities', 'w')

for line in cardFile:
	outCard.write(str(int(line) / int(workers)) + '\n')

cardFile.close()
outCard.close()


#traverse tree given the values of the scans in post-order
def traversal(self):
	#recurse first
	if len(self._child_ids) == 1:
		traversal(self.nextSingleChild)
	elif len(self._child_ids) > 1:
		traversal(self.nextLeftChild)
		traversal(self.nextRightChild)

	print 'currently at operator ', self.id


	if isLeaf(self): 
		tempCost = random.randint(1,10)
		print "for operator ", self.id, " setting cost of scan to ", tempCost
		self.setCost(cost=tempCost)
		return None
	else: 
		#both children have been set
		if checkChildrenSet(self) is not True:
			print "ERROR, both children not set in cost"
		else:
			#set the cost based on the children based on special operators
			print 'setting cost for', self.type
			if 'Join' in self.type:
				print 'setting cost for join'
				childOneCost = self.nextRightChild.getCost
				childTwoCost = self.nextLeftChild.getCost
				self.setCost(childOneCost*childTwoCost)
				print 'new cost of this operator', self.getCost
			elif ('Insert' in self.type or 'Sink' in self.type) and len(self._child_ids) > 1:
				print 'setting cost for sink or insert'
				childOneCost = self.nextRightChild.getCost
				childTwoCost = self.nextLeftChild.getCost
				self.setCost(childOneCost+childTwoCost)
				print 'new cost of this operator', self.getCost
			else:
				childCost = self.nextSingleChild.getCost
				self.setCost(childCost)
				print 'new cost of this operator', self.getCost

def isLeaf(self):
	if len(self._child_ids) == 0:
		return True
	else: 
		return False

def checkChildrenSet(self):
	childrenIds = self._child_ids
	for c in childrenIds:
		currentChildOperatorID = childrenIds.get(c)
		currentChildOperator= self.plan.findOp(currentChildOperatorID) 
		childCost = currentChildOperator.getCost
		if childCost == 0:
			return False
	return True

#find the root operator first?
#rootOperator = None
#for fragments in plan.fragments:
#	for operator in fragments.operators:
#			if operator.parent is None:
#				print "no parent", operator
#				rootOperator = operator
#print "Root Operator Found: ", rootOperator
#something is wrong with shuffle consumer finding its parent?

#traversal(rootOperator)

		