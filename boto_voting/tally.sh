sort Vote_Results.raw > Vote_Results.sorted
uniq -c Vote_Results.sorted > Vote_Results.tally
sort Vote_Results.tally -r > Vote_Results.tally.sorted