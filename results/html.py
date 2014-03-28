import re
f = open('Vote_Results.final')
lines = f.readlines()
lines.sort()
for line in lines:
	char = line[0]
	url = re.search("(?P<url>https?://[^\s]{19})",line).group('url') + '.png'
	print '<li><a href="' + url + '"><p>' + char + '</p><img src="' + url + '"/></a></li>'
