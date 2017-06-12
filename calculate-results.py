#!/usr/bin/python3

import requests
import json
from electioncount import dHondt

# Using the JSON feed from the Guardian for the results
resultsJSONurl = "https://interactive.guim.co.uk/2017/06/ukelection2017-data/snap/full.json"
regionsJSON = "constituencies-regions.json"

r = requests.get(resultsJSONurl)
results = r.json()

regionsFH = open(regionsJSON)
regions = json.load(regionsFH)

# Define some empty dicts to be filled with the results
seatcount = {}
parties = {}
nationalresult = {} 

for region in list(set(regions.values())):
  parties[region] = {} 

# Get the number of seats (constituencies) per region
for region in set(regions.values()):
  seatcount[region] = len([x for x in regions.values() if x == region])

# Build a dict of regions, each a dict with the results per party
for constituency in results:
  independentcounter = 1
  thisRegion = regions[constituency['name']]
  for result in constituency['candidates']:
    # Sum up independents as separate parties
    if result['party'] == "Ind":
      parties[thisRegion]["Independent-" + str(independentcounter)] = result['votes']
      independentcounter += 1
      continue
    if not result['party'] in parties[thisRegion]:
      parties[thisRegion][result['party']] = 0
    parties[thisRegion][result['party']] += result['votes']

# Do the calculation per region and print out the result
for region in sorted(parties.keys()):
  regionresult = dHondt(parties[region],seatcount[region])
  for party in regionresult.keys():
    if party in nationalresult.keys():
      nationalresult[party] += regionresult[party]
    else:
      nationalresult[party] = regionresult[party]

  print(region, regionresult)

# Print out the final result
print()
print("National Results")
print("================")
print(json.dumps(nationalresult, indent=2, sort_keys=True))
