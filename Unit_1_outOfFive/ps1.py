###########################
# 6.00.2x Problem Set 1: Space Cows 
#     ps1_partition.py, ps1_cow_data.txt - provided by the course

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
        provided by the course
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips. Like this for two trips overall: [["Jesse", "Maybel"], ["Maggie", "Callie"]].
    """
    import copy
    # the idea to use list of lists (list of pairs) credited to pelos,
    # http://stackoverflow.com/questions/1867861/python-dictionary-how-to-keep-keys-values-in-same-order-as-declared
    #  will create [['Maggie,3], [Herman,7], ..]
    # 
    # then sorted() by the tonnage
    # the technique of sorting by the second index of the inner list credited to mouad
    # http://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list
    #  key = lambda x: x[1]
    
    keys = cows.keys()
    cowsLst = []
    # POPULATE THE LIST OF [cowName, cowWeight] PAIRS:
    for k in keys:
        if cows[k] <= limit:
            cowsLst.append([k, cows[k]])
    
    transportableCowsOnEarthLst = sorted(cowsLst, key = lambda x: x[1], reverse = True)
    
    transportedInTotal = []
    
    toShrinkLst = copy.deepcopy(transportableCowsOnEarthLst)
    
    # SERIES OF TRIPS
    while toShrinkLst:
        # EACH SINGLE TRIP
        tripTonnage = 0
        cowsToTripL = []
        for i in range(0, len(transportableCowsOnEarthLst)):
            if tripTonnage + transportableCowsOnEarthLst[i][1] <= limit and [transportableCowsOnEarthLst[i][0],transportableCowsOnEarthLst[i][1]] in toShrinkLst:
                tripTonnage += transportableCowsOnEarthLst[i][1]
                cowsToTripL.append(transportableCowsOnEarthLst[i][0])
                toShrinkLst.remove([transportableCowsOnEarthLst[i][0],transportableCowsOnEarthLst[i][1]])
        transportedInTotal.append(cowsToTripL)
        
    return transportedInTotal
    



# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    import copy
    
    cowsNames = cows.keys()
    cowsNamesList = []
    
    for cowName in cowsNames:
        if cows[cowName] <= limit:
            cowsNamesList.append(cowName)
    
    leastNumOfTripsInSuccessflTransport = len(cowsNamesList)
    
    bestTransport = []
    
    for oneTransport in (get_partitions(cowsNamesList)):
        breakInThisTransport = False
        numOfTripsInThisTransport = 0
        for oneTrip in oneTransport:
            if breakInThisTransport:
                break            
            tripTonnage = 0
            for oneCow in oneTrip:
                tripTonnage += cows[oneCow]
                if tripTonnage <= limit:
                    continue
                else:
                    breakInThisTransport = True
                    break
            if not breakInThisTransport:
                numOfTripsInThisTransport += 1
        if (numOfTripsInThisTransport <= leastNumOfTripsInSuccessflTransport) and not breakInThisTransport:
            leastNumOfTripsInSuccessflTransport = numOfTripsInThisTransport
            bestTransport = copy.deepcopy(oneTransport)
    
    return bestTransport




# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    begGreedy = time.time()
    print('GREEDY ALGORITHM returned', len(greedy_cow_transport(cows, limit)), 'trips')
    endGreedy = time.time()
    print('GREEDY ALGORITHM took', endGreedy - begGreedy, 'seconds to run')
    print('----------------------------------------')
    begBruteForce = time.time()
    print('BRUTE FORCE ALGORITHM returned', len(brute_force_cow_transport(cows, limit)), 'trips')
    endBruteForce = time.time()
    print('BRUTE FORCE ALGORITHM took', endBruteForce - begBruteForce, 'seconds to run')


"""
        provided by the course
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")

limit= 10
print(cows)

print('Function greedy_cow_transport:', greedy_cow_transport(cows, limit))
print('Function brute_force_cow_transport:', brute_force_cow_transport(cows, limit))

#compare_cow_transport_algorithms()