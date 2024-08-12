#This is my solution to the 2024 Advent of Code Day 5 Part 2 Challenge.
#I am using this challenge to try different technologies, and for todays challenge I will develop this solution entirely with the ubuntu CLI and VIM.
#By: C Wyatt Bruchhauser
#Date Last Modified: August 11, 2024

import sys
import copy

class Mfunc:
	def __init__(self, start, end, delta=0):
		self.start=start
		self.end=end
		self.delta=delta

	#This method will apply the given delta to all the values in the irange for which it applies. This method will return an array of 1 to 3 ranges.
	def apply(self, irange):
		if (irange.end<self.start or self.end<irange.start):
			return [Mfunc(irange.start, irange.end)]
		elif (irange.start<self.start<=irange.end<=self.end):
			return [Mfunc(irange.start,self.start-1), Mfunc(self.start,irange.end,self.delta)]
		elif (self.start<=irange.start<=self.end<irange.end):
			return [Mfunc(irange.start, self.end, self.delta), Mfunc(self.end+1,irange.end)]
		elif (irange.start<self.start<=self.end<irange.end):
			return [Mfunc(irange.start, self.start-1), Mfunc(self.start, self.end, self.delta), Mfunc(self.end+1, irange.end)]
		elif (self.start<=irange.start<=irange.end<=self.end):
			return [Mfunc(irange.start, irange.end, self.delta)]
		else:
			return None #This should never happen

#subtract irange from self delta of result  will always be zero
	def subtract(self, b):
		if b.start <= self.start and self.end <= b.end:
			return None
		elif self.end < b.start or b.end < self.start:
			return [Mfunc(self.start, self.end)]
		elif self.start < b.start and b.start <= self.end:
			return [Mfunc(self.start, b.start-1)]
		elif b.end < self.end and self.start <= b.end:
			return [Mfunc(b.end+1, self.end)]
		elif self.start < b.start and b.end < self.end:
			return [Mfunc(self.start, b.start-1), Mfunc(b.end+1, self.end)]
		else:
			return -1 #this should never happen.		

	def normalize(self):
		self.start=self.start+self.delta
		self.end=self.end+self.delta
		self.delta=0

#open file
lines = []
with open(sys.argv[1]) as f:
	lines=f.readlines()

#parse our text into a useful format
line0 = lines[0].split(": ")[1]
strseeds = line0.split(" ")

iranges = [] #stores our initail ranges as tuples with the first entry being the start and the second being the end.

seedi = 0
while seedi < len(strseeds):
	iranges.append(Mfunc(int(strseeds[seedi]), int(strseeds[seedi])+int(strseeds[seedi+1])-1))
	seedi+=2

iranges.sort(key=lambda f: f.start)

steps=[] #This variable will contain an array of ordered mapping steps,
	 #each of which will have its own list of amaps

for line in lines:
	if len(line) == 1:
		steps.append([])
	elif line[0] >= '0' and line[0] <= '9':
		stramap = line.split()
		steps[-1].append(Mfunc(int(stramap[1]),int(stramap[1])+int(stramap[2])-1, int(stramap[0])-int(stramap[1])))

for step in steps:
	cranges=[]
	for f in step:
		for ir in iranges:
			results = f.apply(ir)
			for result in results:
				if result.delta != 0:
					cranges.append(result)
	for cr in cranges:
		uranges=[]
		for ir in iranges:
			if ir.subtract(cr) != None:
				uranges+=ir.subtract(cr)
		iranges=copy.deepcopy(uranges)
	if len(cranges)!=0:
		iranges=cranges+uranges
		for ir in iranges:
			ir.normalize()

print(min(iranges, key=lambda ir:ir.start).start)	

