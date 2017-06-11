#!/usr/bin/python3

import requests
import json

def dHondt(results, seats):
  # Calculate the number of seats using the d'Hondt method
  # Takes a dict with the votes and an int with the number of seats
  # Returns a dict with the seats allocated per party

  # Labour and the Co-operative party would probably stand on the same list
  # This re-assigns votes for the Co-op party to the Labour party
  # Remove it to simulate two separate lists
  if "Lab Co-op" in results.keys():
    results['Lab'] += results['Lab Co-op']
    results['Lab Co-op'] = 0

  # We need two copies of this array:
  #   one to calculate the new distribution after assigning a seat
  #   one to keep track of the seats allocated (which we immediately zero)
  origvote = results.copy()

  elected = results.copy()
  for i in elected.keys():
    elected[i] = 0

  # Find the highest vote for each round and assign a seat to that party
  # This is assuming pure PR, there is no hurdle (usually 3 or 5%)
  for round in range(seats):
    thisSeat = list(results.keys())[0]
    for party in results.keys():
      if results[party] > results[thisSeat]:
        thisSeat = party
    elected[thisSeat] += 1
    results[thisSeat] = origvote[thisSeat] / elected[thisSeat] + 1

  # Clean up the results dict by removing parties with no seats
  for party in list(elected.keys()):
    if elected[party] == 0:
      del elected[party]

  # Return a dict of the seats allocated for this region
  return elected

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
