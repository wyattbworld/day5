#This is my solution to the 2024 Advent of Code Day 5 Part 1 Challenge.
#I am using this challenge to try different technologies, and for todays challenge I will develop this solution entirely with the ubuntu CLI and VIM.
#By: C Wyatt Bruchhauser
#Date Last Modified: August 2, 2024

import sys

class Amap:
	def __init__(self, destination, source, length):
		self.destination = destination
		self.source = source
		self.length = length
	#This method will check if a certain number is in the range to be modified.
	def check_range(self, num):
		if num >= self.source and num < self.source+self.length:
			return True
		return False
	#This method will modify a number into its mapped value. If it is not in the applicable range, this method will do nothing.
	def map_number(self, num):
		if not self.check_range(num):
			return num
		return num-self.source+self.destination

#open file
lines = []
with open(sys.argv[1]) as f:
	lines=f.readlines()

#parse our text into a useful format
line0 = lines[0].split(": ")[1]
strseeds = line0.split(" ")

seeds = [] #stores our initial seeds

for strseed in strseeds:
	seeds.append(int(strseed))

steps=[] #This variable will contain an array of ordered mapping steps,
	 #each of which will have its own list of amaps

for line in lines:
	if len(line) == 1:
		steps.append([])
	elif line[0] >= '0' and line[0] <= '9':
		stramap = line.split()
		steps[-1].append(Amap(int(stramap[0]),int(stramap[1]),int(stramap[2])))	

#time to run the algorithm!
locations = []
seedid = 0
for seed in seeds:
	num = seed
	for step in steps:
		for amap in step:
			if amap.check_range(num):
				num = amap.map_number(num)
				break
	locations.append(num)
	seedid+=1

#finally find the min location
min_location = -1
for location in locations:
	if (location < min_location or min_location == -1):
		min_location = location
print(min_location)
