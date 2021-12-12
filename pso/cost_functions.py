import representation
import evaluation
import copy

"""
Function for translating a particle into a strat matrix, then evaluating that strategy against the selected opponent strategy
"""
def translate_and_evaluate(particle,debug=False):

    # Determine the Party

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
    
    # setup battle parameters
    battles_per_test = 50 # number of battles simulated to determine an individual's fitness
    win_score = 5 # fitness score awarded for winning a battle
    lose_score = 1 # fitness score awarded for losing a battle
    survivor_bonus = win_score / party_size # bonus score awarded to winners for having multiple surviving units
    kill_bonus = lose_score / party_size # bonus score awarded to losers for killing the enemy's units

    # determine the opponent of choice
    #op_strat = [[1,98,12],[1,79,1],[1,77,8]] # best GA tanks strat
    #op_strat = [[98, 2, 1, 1, 2],[1, 93, 3, 3, 1],[2, 4, 98, 6, 6],[3, 1, 3, 98, 6],[1, 1, 2, 4, 87]] # best GA glass_cannons strat
    #op_strat = [[1, 71, 53, 14, 1],[3, 2, 5, 27, 97],[2, 1, 4, 11, 48],[2, 5, 2, 8, 86],[9, 3, 3, 95, 23]] # best GA boss_battle strat
    #op_strat = [[4, 88, 63, 29],[1, 81, 1, 2],[1, 2, 70, 5],[1, 58, 96, 46]] # best GA balanced strat
    op_strat = [[10]*party_size]*party_size # baseline strat
    opponent = representation.Strategy(0,party_size,op_strat)

    # turn the particle into a strat matrix
    counter = 0
    strat = []
    tpvl = []
    for i in particle:
        if counter < party_size:
            tpvl.append(i)
            counter += 1
        if counter >= party_size:
            strat.append(copy.deepcopy(tpvl))
            tpvl = []
            counter = 0
    
    # create a strategy from that matrix
    new_strategy = representation.Strategy(100,party_size,strat)

    # evaluate that strategy against the opponent
    evaluation.simulate_battles(new_strategy,opponent,party,party,battles_per_test,win_score,lose_score,survivor_bonus,kill_bonus,debug=False)
    new_strategy.fitness = new_strategy.curr_fitness / new_strategy.battle_count

    if debug:
        print(new_strategy)

    return (win_score*2) - new_strategy.fitness