import string
import math
numberLines = 59986052
listChunks = [2,4,5]
numberWorkers = 6
alpha = list(string.ascii_lowercase)[:10]

#split original file first
linesForNumWorkers = math.ceil(numberLines/(numberWorkers*1.0))
print linesForNumWorkers

print 'split -l ' + str(int(linesForNumWorkers)) + ' lineorderOUT.csv '+ str(numberWorkers) + 'Workers/lineitem;' 
print 'cd '  + str(numberWorkers) + 'Workers/;'

for currentWorker in range(1,numberWorkers+1):
	print 'mkdir ' + 'Worker' + str(currentWorker) +';'

for currentChunk in listChunks:
	for currentWorker in range(1,numberWorkers+1):
		print 'mkdir Worker' + str(currentWorker) + '/Chunks-' + str(currentChunk) + ';'
	for currentWorker in range(1,numberWorkers+1):
		print 'split -l ' + str(int(math.ceil(linesForNumWorkers/(currentChunk*1.0)))) + ' lineitema' + alpha[currentWorker-1] + ' Worker' + str(numberWorkers) + '/Chunks-' + str(currentChunk) + '/lineitem' + ';'
