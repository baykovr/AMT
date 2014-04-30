all_votes = {}

f = open('Vote_Results.tally.sorted', 'r')
for line in f:
	#input Vote_Reuslts.tally.sorted
	if len(line) > 0:

		# numvotes letter imgurlink
		line = line.split()

		tally  = line[0]
		letter = line[1]
		link   = line[2]

		entry = [tally,link]

		if letter in all_votes:
			#check if new entry has more votes
			if all_votes[letter][0] > tally:
				all_votes[letter] = entry
		else:
			all_votes[letter] = entry
f.close()


for key in all_votes:
	print key,all_votes[key]