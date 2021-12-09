"""
CISC455 Final Project
Recombination Module

Joshua Chai-Tang 20119074
"""

# My module imports
import representation
# Python module imports
import random
import copy

"""
Function for performing single point crossover recombination
-takes two parent individuals and produces two offspring

Params:
-parent_a   : Strategy : an individual strategy to serve as one parent
-parent_b   : Strategy : an individual strategy to serve as the other parent
-party_size : int : the party size these individuals are designed for
-generation : int : which generation this individual belongs to
-debug      : boolean : if set to true, will print the entire crossover process (step by step) to the console

Returns:
-child_a : Strategy : the first offspring individual
-child_b : Strategy : the second offspring individual
"""
def crossover(parent_a,parent_b,party_size,generation,debug=False):

    if (debug):
        print("Parent A:")
        print(parent_a)
        print("Parent B:")
        print(parent_b)

    # select a random crossover point
    # it's possible for no crossover to occur at all if the point selected is 0 or party_size
    crossover_point = random.randint(0,party_size)
    
    if debug: print("Crossover Point: ",crossover_point)

    # perform crossover (exchanging entire TPVL's)
    strat_a = []
    strat_b = []
    for i in range(party_size):
        # up to the crossover point, child_a gets TPVL's from parent_a (inverse for child_b)
        if i < crossover_point:
            strat_a.append(copy.deepcopy(parent_a.strat[i]))
            strat_b.append(copy.deepcopy(parent_b.strat[i]))
        # after the crossover point, child_a gets TPVL's from parent_b (inverse for child_b)
        else:
            strat_a.append(copy.deepcopy(parent_b.strat[i]))
            strat_b.append(copy.deepcopy(parent_a.strat[i]))
    
    # create the new children
    child_a = representation.Strategy(generation,party_size,strat_a)
    child_b = representation.Strategy(generation,party_size,strat_b)

    if (debug):
        print("Child A:")
        print(child_a)
        print("Child B:")
        print(child_b)

    return child_a, child_b