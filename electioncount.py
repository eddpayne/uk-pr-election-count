def dHondt(results, seats, threshold=0):
  # Calculate the number of seats using the d'Hondt method
  # - Takes a dict with the votes and an int with the number of seats
  # - Optionally takes a minimum threshold percentage
  # - Returns a dict with the seats allocated per party

  # Labour and the Co-operative party would probably stand on the same list
  # This re-assigns votes for the Co-op party to the Labour party
  # Remove it to simulate two separate lists
  if "Lab Co-op" in results.keys():
    results['Lab'] += results['Lab Co-op']
    results['Lab Co-op'] = 0

  if "Labour and Co-operative" in results.keys():
    results['Labour'] += results['Labour and Co-operative']
    results['Labour and Co-operative'] = 0

  # We need two copies of this array:
  # - one to calculate the new distribution after assigning a seat
  # - one to keep track of the seats allocated (which we immediately zero)
  origvote = results.copy()

  elected = results.copy()
  for i in elected.keys():
    elected[i] = 0

  # If there's a threshold, make a list of parties eligible to receive seats
  if threshold != 0:
    totalvotes = sum(results.values())
    quota = totalvotes * threshold / 100
    eligible = []
    for party in results:
      if results[party] > quota:
        eligible.append(party)
  else:
  # if there's no threshold, all parties can receive seats
    eligible = list(results.keys())
    
  # Find the highest vote for each round and assign a seat to that party
  for round in range(seats):
    thisSeat = list(results.keys())[0]
    for party in results.keys():
      if results[party] > results[thisSeat] and party in eligible:
        thisSeat = party
    elected[thisSeat] += 1
    results[thisSeat] = origvote[thisSeat] / (elected[thisSeat] + 1)

  # Clean up the results dict by removing parties with no seats
  for party in list(elected.keys()):
    if elected[party] == 0:
      del elected[party]

  # Return a dict of the seats allocated for this region
  return elected

def SainteLague(results, seats, threshold=0):
  # Calculate the number of seats using the Sainte-Lague method
  # - Takes a dict with the votes and an int with the number of seats
  # - Optionally takes a minimum threshold percentage
  # - Returns a dict with the seats allocated per party

  # Labour and the Co-operative party would probably stand on the same list
  # This re-assigns votes for the Co-op party to the Labour party
  # Remove it to simulate two separate lists
  if "Lab Co-op" in results.keys():
    results['Lab'] += results['Lab Co-op']
    results['Lab Co-op'] = 0

  # We need two copies of this array:
  # - one to calculate the new distribution after assigning a seat
  # - one to keep track of the seats allocated (which we immediately zero)
  origvote = results.copy()

  elected = results.copy()
  for i in elected.keys():
    elected[i] = 0

  # If there's a threshold, make a list of parties eligible to receive seats
  if threshold != 0:
    totalvotes = sum(results.values())
    quota = totalvotes * threshold / 100
    eligible = []
    for party in results:
      if results[party] > quota:
        eligible.append(party)
  else:
  # if there's no threshold, all parties can receive seats
    eligible = list(results.keys())

  # Find the highest vote for each round and assign a seat to that party
  for round in range(seats):
    thisSeat = list(results.keys())[0]
    for party in results.keys():
      if results[party] > results[thisSeat] and party in eligible:
        thisSeat = party
    elected[thisSeat] += 1
    results[thisSeat] = origvote[thisSeat] / ((2 * elected[thisSeat]) + 1)

  # Clean up the results dict by removing parties with no seats
  for party in list(elected.keys()):
    if elected[party] == 0:
      del elected[party]

  # Return a dict of the seats allocated for this region
  return elected
