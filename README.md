AMT
===

Amazon Makes a Typeface

CSCE 438 - Homework 3

Robert Baykov
William Guerra
Jason Harris

===
## Part 1: Character drawing
HITs are created to have turkers draw and submit an image of a character (A, B, 7, etc.).
You can run this part by:
* Navigate to /command_line_tools/bin
* Add in your AWS credentials to _mturk.properties_, and ensure the link is set to sandbox, and not production
* Navigate to /command_line_tools/samples/best_image
* modify best_image.input to include whatever characters you'd like to create HITs for. The example file creates a HIT for A, B, and C with the following format:
	```
	LETTER
	A
	B
	C
	```
* modify best_image.properties and best_image.question as desired
* run the run.sh shell script

Also,
* getresults.sh will download a .csv file with current results of the HITs
* approveAndDeleteResults.sh will approve all HITs and delete them from your account

## Part 2: Voting for the best character
Turkers are asked to pick the best drawn character out of the results collected from Part 1. Detailed description of this process and how to use it is provided in the README of /boto_voting