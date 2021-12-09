"""
CISC455 Final Project
Mutation Module

Joshua Chai-Tang 20119074
"""

# My module imports
import representation
# Python module imports
import random
import copy

"""
Function for handling random mutation of an individual strategy
-randomly determines which mutation forms to use based on given probabilities
-an individual can undergo both micro and macro mutation, but also has a chance of neither
-applies the chosen micro and macro mutation methods

Params:
-individual            : Strategy : the individual solution to be mutated
-mutation_rate         : float : the chance of mutation occurring, out of 1
-party_size            : int : the party size these individuals are designed for
-lower_limit           : int : the minimum allowed TPV value (ABSOLUTELY MUST BE GREATER THAN 0)
-upper_limit           : int : the maximum allowed TPV value

-debug                 : boolean : if set to true, will print the entire mutation process (step by step) to the console

Returns:
-Nothing, as the mutated individual's strat attribute is altered directly.
"""
def mutate(individual,mutation_rate,party_size,lower_limit,upper_limit,debug=False):

    if debug:
        print("Mutating individual:")
        print(individual)

    # iterate through every TPVL and apply mutations to random TPV's
    for i in range(party_size):
        for j in range(party_size):  
            # determine if this TPV should be mutated
            if (random.uniform(0,1) < mutation_rate):
                # replace the TPV with a random new value
                individual.strat[i][j] = random.randint(lower_limit,upper_limit)

    if debug:
        print("Individual post mutation:")
        print(individual)

    return 