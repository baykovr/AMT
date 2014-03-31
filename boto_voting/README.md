# CSCE 438 Group Project
# AMT Voting Componenet

Summary
-------

This section of the project provides the tools to process and tally
the voting amt hits we utilize to select the 'best' character drawing.

The tools are composed of 3 parts: 

amt_voting.py

Script used to interface with amt and issue the hits/pull results.

tally.sh

Bash script to sort/uniq the resulting raw dataset.

tall.py

Final script to select the best imgur link based on the vote results.


amt_voting.py
-------------

Exec: "python2 amt_voting.py"

The purpose of this program is to issue the hits and gather statistics 
and results from amt. 

Before you begin you should configure the variables at the top of the script,
the most important ones being ACCESS_ID, SECRET_KEY, and INFILE.

Additionally you may also configure the hit reward and timeout values, as well
as changing the image format and thumbnail size. 

To issue the hits run amt_voting.py and choose task [1]
The INFILE will be processed in its entirety, split into hits and issued to 
amt. 

You may then review the status, balance and other attributes using options 3+
Some tools are also avaiable for basic administrator, although custom tailored to
our setup you may wish to modify them to suit your needs. 

When the hits are complete you should download the 'raw' results from amt 
using [2]. 

The resulting raw unsorted file is saved to 'Vote_Results.raw' for later processing.

# INFILE FORMAT
The infile is a collection of characters preceeded by the # symbol
followed by a set of image links. 

Input file regular expression:
(#{A-Z,.?!}\n{link}*\n)*

Example:
#A
http://imgur.com/y3kU3ff
http://i.imgur.com/RCHzSn3
http://imgur.com/xyqXnxq
#B
http://imgur....


The url's themselves do not need to be imgur in particular, they do however 
need to exclude the file format. This is because imgur provides several api
functions for automatically converting the image to different formats by 
modifying the url.


tally.sh
--------


This shell script leverages sort and uniq to process the voting results,
the end file is 'Vote_Results.tally.sorted which is the input to tally.py

The purpose of this script is to eliminate any possible duplicates or anomalies 
in the file, it also allows for a count to be generated for each link.

tally.py
--------

The final script processes 'Vote_Results.tally.sorted' in order to choose the 
imgur links per character with the highest number of votes. The implimentation 
uses a simple algorithm to resolve ties in the votes, so for best outcomes it 
is recomended to run many hits for a better dataset to parse. 


The resulting file generated will be 'Vote_Result.final', a list of characters
and url's with a vote count.