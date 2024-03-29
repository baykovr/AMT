AMT
===

__Amazon Makes a Typeface__ for CSCE 438 with Dr. Caverlee

Members: Robert Baykov, William Guerra, and Jason Harris

===
## Part 1: Character drawing
HITs are created to have turkers draw and submit an image of a character (A, B, 7, etc.).
You can run this part by:
* Set the MTURK_CMD_HOME environment variable to the command_line_tools directory of your local clone. Example: `export MTURK_CMD_HOME=~/Documents/Development/amt/command_line_tools` in _~/.bash_profile_
* Navigate to command_line_tools/bin
* Add in your AWS credentials to _mturk.properties_, and ensure the link is set to sandbox, and not production
* Navigate to command_line_tools/samples/best_image
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
Turkers are asked to pick the best drawn character out of the results collected from Part 1. Detailed description of this process and how to use it is provided in the README of boto_voting

## Final Product: AMT
Navigate to the font/ directory to download the final font: AMT.ttf

(Other Formats also available)