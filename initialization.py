"""
CISC455 Final Project
Population Initialization Module

Joshua Chai-Tang 20119074
"""

# My module imports
import representation
# Python module imports
import random

"""
Function for initializing the population 
-generates random individual strategies based on input params and compiles them all into a single list

Params:
-population_size : int : total number of individuals to create
-party_size      : int : the party size these individuals are designed for
-lower_limit     : int : the minimum allowed TPV value (ABSOLUTELY MUST BE GREATER THAN 0)
-upper_limit     : int : the maximum allowed TPV value

Returns:
-population : list(Strategy): the full list of individual strategies 
"""
def initialize(population_size,party_size,lower_limit,upper_limit):
    
    # create up to population_size random individuals based on the constraints given, then place them in the population list.
    population = []

    # individuals are represented as Strategy objects
    # the Strategy object is defined in the representation module.
    for i in range(population_size):

        # generate the individual's strat list by generating party_size random TPVL's
        new_strat = []
        for x in range(party_size):
            # create a random TPVL with length of party_size
            tpvl = []
            for y in range(party_size):
                # generate random TPV's between the lower and upper limits and add them to the TPVL
                tpv = random.randint(lower_limit,upper_limit)
                tpvl.append(tpv)
            # append the new TPVL to the strat
            new_strat.append(tpvl)
        
        # generate the individual
        # all intialized individuals have age 0
        individual = representation.Strategy(0,party_size,new_strat)

        # add the individual to the population
        population.append(individual)

    return population

"""
pop = initialize(10,5,1,100)
for i in pop:
    print(i)
"""