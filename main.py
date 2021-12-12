"""
CISC455 Final Project
Target Prioritization Strategies - Main Module

Joshua Chai-Tang 20119074
"""

# My module imports
import initialization
import evaluation
import tournament
import recombination
import mutation
import representation
# Python module imports
import random

def main():

    # create the parties 

    # party comp A : tanks
    party_size = 3
    tanks = [party_size]
    for i in range(party_size):
        unit = representation.Unit(5,30)
        tanks.append(unit)
    
    # party comp B : glass cannons
    party_size = 5
    glass_cannons = [party_size]
    for i in range(party_size):
        unit = representation.Unit(10,1)
        glass_cannons.append(unit)
    
    # party comp C : boss battle
    party_size = 5
    boss_battle = [party_size]
    for i in range(party_size):
        if i == 0:
            unit = representation.Unit(20,100)
        else:
            unit = representation.Unit(5,10)
        boss_battle.append(unit)
    
    # party comp D : balanced
    party_size = 4
    balanced = [party_size]
    unit = representation.Unit(5,45)
    balanced.append(unit)
    unit = representation.Unit(25,25)
    balanced.append(unit)
    unit = representation.Unit(30,20)
    balanced.append(unit)
    unit = representation.Unit(15,35)
    balanced.append(unit)

    # select a party composition to use
    party = balanced[1:]
    party_size = balanced[0]
    
    # select a baseline strategy
    # this is the default strategy that all other individuals are compared to for determining fitness under the baseline evaluation method
    # - this baseline consists of a strategy that has no preference for any target, essentially picking all targets at absolute random
    baseline = representation.Strategy(0,party_size,[[10]*party_size]*party_size)
    # - this baseline consists of a strategy that focuses all its attacks on one target at a time (requires party size of 5)
    #baseline = representation.Strategy(0,party_size,[[10000,1000,100,10,1]]*party_size)

    # DEFINE KEY VALUES:

    # population parameters
    population_size = 100 # number of individuals per generation
    lower_limit = 1 # the minimum allowed TPV
    upper_limit = 99 # the maximum allowed TPV
    mutation_rate = 0.1 # the percentage of TPV's to change during mutation
    tourney_size = 4 # number of individuals being compared in each selection tournament
    num_parents = 20 # number of parents to select at each generation. must be even and tourney_size*num_parents must be smaller than popsize
   
    # combat parameters
    battles_per_test = 50 # number of battles simulated to determine an individual's fitness
    win_score = 5 # fitness score awarded for winning a battle
    lose_score = 1 # fitness score awarded for losing a battle
    survivor_bonus = win_score / party_size # bonus score awarded to winners for having multiple surviving units
    kill_bonus = lose_score / party_size # bonus score awarded to losers for killing the enemy's units
    
    # other parameters
    termination_condition = 2000 # max number of generations to simulate
    update_distance = 500 # number of generations between each progress update to be printed to the console
    do_tournament_battles = False # select parents by simulating battles between them

##############################################################################################################################
##################################### This is where the algorithm actually happens ###########################################
##############################################################################################################################

    # initialize the population
    population = initialization.initialize(population_size,party_size,lower_limit,upper_limit)

    # evaluate fitness of all individuals by simulating battles against the baseline
    for i in range(len(population)):
        evaluation.simulate_battles(population[i],baseline,party,party,battles_per_test,win_score,lose_score,survivor_bonus,kill_bonus)
        population[i].fitness = population[i].curr_fitness / population[i].battle_count
    
    # evaluate the fitness of baseline
    baseline.fitness = baseline.curr_fitness / baseline.battle_count

    # BEGIN THE SIMULATION:
    generation = 0
    while (generation < termination_condition):
        # increment generation
        generation += 1

        # Run tournaments to select winners to be parents, and losers to be replaced
        winners, losers = tournament.select_parents(population,tourney_size,num_parents,do_tournament_battles,party,battles_per_test,win_score,lose_score,survivor_bonus,kill_bonus,debug=False)
        # Sort the loser list, because they have to be removed in reverse order to prevent indexing errors
        losers = sorted(losers)

        # Create offspring from the parents
        offspring = []
        for i in range(0,len(winners),2):
            parent_a = population[winners[i]]
            parent_b = population[winners[i+1]]
            child_a, child_b = recombination.crossover(parent_a,parent_b,party_size,generation,debug=False)
            offspring.append(child_a)
            offspring.append(child_b)

        # Mutate the offspring 
        for i in range(len(offspring)):
            mutation.mutate(offspring[i],mutation_rate,party_size,lower_limit,upper_limit,debug=False)

        # Evaluate the fitness of the children by simulating battles against the baseline
        if not(do_tournament_battles):
            for i in range(len(offspring)):
                evaluation.simulate_battles(offspring[i],baseline,party,party,battles_per_test,win_score,lose_score,survivor_bonus,kill_bonus)
                offspring[i].fitness = population[i].curr_fitness / population[i].battle_count

        # Replace the losers with the offspring
        # Start with the losers near the end of the list, and work backwards
        for i in range(len(losers)-1,-1,-1):
            population.pop(losers[i])
        # Add in the new children
        for i in offspring:
            population.append(i)

        # Every update_distance evaluations, produce a status update on the state of the population
        if (generation % update_distance == 0):

            best_fit = -1
            best_strat = None
            best_new_fit = -1
            best_new_strat = None
            for strategy in population:
                # find the best individual in the population
                if strategy.fitness > best_fit:
                    best_fit = strategy.fitness
                    best_strat = strategy
                # find the best individual from this generation
                if not(do_tournament_battles):
                    if strategy.age == generation and strategy.fitness > best_new_fit:
                        best_new_fit = strategy.fitness
                        best_new_strat = strategy
            print("=== Generation",generation,"===")
            print("Best Individual Overall:")
            print(best_strat)

            if not(do_tournament_battles):
                print("\nBest From This Generation:")
                print(best_new_strat)
                # compare best individuals with the baseline
                baseline.fitness = baseline.curr_fitness / baseline.battle_count
                print("\nBaseline:")
                print(baseline)

            print("*************************************************")

    return 

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

main()

