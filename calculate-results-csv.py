#!/usr/bin/python3

import csv
from electioncount import dHondt, SainteLague

def prettyPrint(dictionary):
  longest = max([len(x) for x in list(dictionary.keys())])
  for line in sorted(dictionary,key=dictionary.get,reverse=True):
    print(line + " " * (longest - len(line)) + ": " + str(dictionary[line]))

# This is the file available at 
# http://researchbriefings.files.parliament.uk/documents/CBP-7979/hocl-ge2017-results-full.csv
# from http://researchbriefings.parliament.uk/ResearchBriefing/Summary/CBP-7979
csvfile = "hocl-ge2017-results-full.csv"

seatcount = {}
parties = {}
nationalresult = {}
constituencies = {}

csvhandle = open(csvfile)
csvreader = csv.reader(csvhandle)

# Discard the header line
csvreader.__next__()

# Get each row and parse the results
for row in csvreader:
  constituency = row[2]
  region = row[4]
  party = row[7]
  result = int(row[14])

  # Check that the region exists first
  if region not in parties:
    parties[region] = {}
    constituencies[region] = []
  
  # Keep a list of constituencies per region, to calculate the seats per region
  if constituency not in constituencies[region]:
    constituencies[region].append(constituency)

  # Keep a running total of votes per party, per region
  if party not in parties[region]:
    parties[region][party] = result
  else:
    parties[region][party] += result

# Close the file handle
csvhandle.close()

# Calculate the number of seats per region
for region in constituencies:
  seatcount[region] = len(constituencies[region])

# Do the calculation per region and print out the result
for region in sorted(parties.keys()):
  regionresult = dHondt(parties[region],seatcount[region],3)
  for party in regionresult.keys():
    if party in nationalresult.keys():
      nationalresult[party] += regionresult[party]
    else:
      nationalresult[party] = regionresult[party]

# Print out the final result
print("National Results")
print("================")
prettyPrint(nationalresult)
print()
print("Total Seats: " + str((sum(nationalresult.values()))))
