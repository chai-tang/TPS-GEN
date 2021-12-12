"""
CISC455 Final Project
Parent & Survivor Selection Tournament Module

Joshua Chai-Tang 20119074
"""

# My module imports
import representation
import evaluation
# Python module imports
import random

"""
Function to select parents from the population by running tournaments
-runs a set number of tournaments, without replacement, and selects the winners of each as parents

Params:
-population            : list(list(instruction)) : full list of individual strategies in the population
-tourney_size          : int : number of individuals per tournament
-num_parents           : int : number of tournaments to run, thus the number of parents selected
-do_tournament_battles : boolean : if set to true, potential parents will battle each other to determine fitness

>the following parameters are for if tournament battles are being used<
-party                 : list(Unit) : The party composition all individuals will use, consisting of a list of Units
-num_battles           : int : The number of battles to simulate
-win_score             : float : The fitness score awarded to the winner of a battle
-lose_score            : float : The fitness score awarded to the loser of a battle
-survivor_bonus        : float : The bonus score awarded to the winner for each surviving unit
-kill_bonus            : float : The bonus score awarded to the loser for each of the winner's units it managed to kill
-debug                 : boolean : if set to true, will print the entire tournament process (step by step) to the console

Returns:
-winners : list(int) : list of tournament winners (by index) to be used as parents
-losers  : list(int) : list of tournament losers (by index) to be replaced by offspring
"""
def select_parents(population,tourney_size,num_parents,do_tournament_battles,party,battles_per_test,win_score,lose_score,survivor_bonus,kill_bonus,debug=False):
    
    # create the list to hold the indexes of winners & losers 
    winners = []
    losers = []
    # create a list to hold the previous tournament contestants
    previous_contestants = []

    # run the tournaments
    for k in range(num_parents):
        # select tourney_size random individuals
        contestants = []
        while len(contestants) < tourney_size:
            i = random.randint(0,len(population)-1)
            # only select individuals that have not competed before
            if (i not in contestants) and (i not in previous_contestants):
                contestants.append(i)
                previous_contestants.append(i)
        
        if debug:
            print("Contestants this round: ",contestants)
            for i in contestants:
                print(population[i])

        # if do_tournament_battles is true, simulate battles between the parents
        if do_tournament_battles:
            # reset curr_fitness and battle_count attributes
            for i in contestants:
                population[i].curr_fitness = 0
                population[i].battle_count = 0
            # simulate the battles
            for i in contestants:
                for j in contestants:
                    # strategies shouldn't battle themselves
                    if i != j:
                        evaluation.simulate_battles(population[i],population[j],party,party,battles_per_test,win_score,lose_score,survivor_bonus,kill_bonus)
            # determine the fitness scores
            for i in contestants:
                population[i].fitness = population[i].curr_fitness / population[i].battle_count

        # select the contestant with the highest fitness value as winner
        best_fit = -99999999999999
        best_index = None
        worst_fit = 999999999999
        worst_index = None
        for i in contestants:
            if population[i].fitness > best_fit:
                best_fit = population[i].fitness
                best_index = i
            if population[i].fitness < worst_fit:
                worst_fit = population[i].fitness
                worst_index = i
        
        # add the winners and losers to their respective lists
        winners.append(best_index)
        losers.append(worst_index)
    
    if debug:
        print("Winning Individuals:")
        for i in winners:
            print("Individual ",i)
            print(population[i])

        print("Losing Individuals:")
        for i in losers:
            print("Individual ",i)
            print(population[i])

    return winners, losers


