"""
CISC455 Final Project
Fitness Evaluation Module

Joshua Chai-Tang 20119074
"""

# My module imports
import representation
# Python module imports
import random
import copy

"""
Function for simulating a battle between two individuals and determining the winner.

Params:
-indv0        : Strategy : The first individual competing in this battle
-indv1        : Strategy : The second individual competing in this battle
-party_indv0  : list(Unit) : The party composition indv0 will use, consisting of a list of Units
-party_indv1  : list(Unit) : The party composition indv1 will use, consisting of a list of Units
-debug        : boolean : If set to true, will print out the entire battle sequence to console. Only used for testing purposes.

Returns: Two values
-0 if strat0 wins, 1 if strat1 wins, or 2 if there's a tie
-an integer stating how many of the winner's units survived, if any
"""
def battle(indv0,indv1,party_indv0,party_indv1,debug=False):

    # get each individual's strategy lists
    strat0 = indv0.strat
    strat1 = indv1.strat

    # initialize each side's starting party
    # these list will track the current remaining health of units for their respective sides
    # initially all units are set to maximum health
    party0 = copy.deepcopy(party_indv0)
    party1 = copy.deepcopy(party_indv1)
    party_length = len(party0)
    
    # tracking how many units are still alive on either side
    # (which is all of them at the start)
    alive0 = party_length
    alive1 = party_length

    # BEGIN THE BATTLE
    # (which keeps running until one or both sides has no more living units)
    round = 0
    while (alive0 > 0 and alive1 > 0):

        if debug:
            print("=================================================")
            print("ROUND",round,": FIGHT!")
            print("Strat0's Party:",party0)
            print("Strat1's Party:",party1)

        # create lists to track the chosen targets for each round
        # ex. if targets0[1] = 4, that means that strat0's unit1 has chosen to attack unit4
        targets0 = []
        targets1 = []

        # determine chosen targets for all units on either side, based on their TPVL
        all_targets = list(range(party_length)) # a list from 0 to the highest unit index
        for i in range(party_length):
            # for each unit, select a target using random.choices with that strategy's TPVL as weight values
            # make sure to only select a target which is still 'alive' 
            # IMPORTANT: NO TPV SHOULD NEVER EVER BE ZERO OR ELSE THIS COULD LOOP FOREVER

            # determine which targets are still alive and get their tpv's
            alive_targets = []
            alive_tpvs = []
            for k in range(party_length):
                if party1[k].health > 0:
                    alive_targets.append(k)
                    alive_tpvs.append(strat0[i][k])
            t0 = random.choices(alive_targets,weights=alive_tpvs,k=1)[0]

            alive_targets = []
            alive_tpvs = []
            for k in range(party_length):
                if party0[k].health > 0:
                    alive_targets.append(k)
                    alive_tpvs.append(strat1[i][k])
            t1 = random.choices(alive_targets,weights=alive_tpvs,k=1)[0]

            targets0.append(t0)
            targets1.append(t1)
        
        if debug:
            print("Strat0 Target Selection: ",targets0)
            print("Strat1 Target Selection: ",targets1)
        
        # make the attacks:
        # each unit on either side will attack their chosen target
        # this means retrieving the unit's damage value, then subtracting that number from the target unit's health
        for i in range(party_length):

            # Strat0 makes an attack
            # make sure only living units make attacks
            if party0[i].health > 0:
                # dont attack dead targets
                if party1[targets0[i]].health > 0 : 
                    # subtract this unit's attack from the target's health
                    party1[targets0[i]].health -= party0[i].attack
                    if debug: print("Strat0 Unit",i,"attacks enemy Unit",targets0[i],"for",party0[i].attack,"damage!")
                    # check if the target is now dead, update alive1 count accordingly
                    if party1[targets0[i]].health <= 0:
                        party1[targets0[i]].health = 0
                        alive1 -= 1
                        if debug: print("Strat1 Unit",targets0[i],"dies!")
                elif debug:
                    print("Strat0 Unit",i,"target died earlier this round")
            elif debug:
                print("Strat0 Unit",i,"does not attack because it's dead")

            # Strat1 makes an attack
            # make sure only living units make attacks
            if party1[i].health > 0:
                # dont attack dead targets
                if party0[targets1[i]].health > 0 : 
                    # subtract this unit's attack from the target's health
                    party0[targets1[i]].health -= party1[i].attack
                    if debug: print("Strat1 Unit",i,"attacks enemy Unit",targets1[i],"for",party1[i].attack,"damage!")
                    # check if the target is now dead, update alive0 count accordingly
                    if party0[targets1[i]].health <= 0:
                        party0[targets1[i]].health = 0
                        alive0 -= 1
                        if debug: print("Strat0 Unit",targets1[i],"dies!")
                elif debug:
                    print("Strat1 Unit",i,"target died earlier this round")
            elif debug:
                print("Strat1 Unit",i,"does not attack because it's dead")

            # important to note here that attacks are made in order, which could kill enemy units before they have a chance to act
            # Strat0 always goes first, and unit0 always goes before other units
            # Strat0 thus has a huge advantage in combat! Remember this.
        
        # rounds continue until one or both parties dies
        round += 1

    if debug:
        print("=================================================")
        print("FINAL STANDINGS:")
        print("Strat0's Party:",party0)
        print("Strat1's Party:",party1)

    # determine the winner
    if alive0 > 0:
        if debug: print("Strat0 Wins with",alive0,"survivors!")
        return 0, alive0
    elif alive1 > 0:
        if debug: print("Strat1 Wins with",alive1,"survivors!")
        return 1, alive1
    else:
        if debug: print("It's a tie!")
        return 2, 0


"""
Function for simulating multiple battles between two individuals and awarding fitness scores

Params:
-indv0          : Strategy : The first individual competing in this battle
-indv1          : Strategy : The second individual competing in this battle
-party_indv0    : list(Unit) : The party composition indv0 will use, consisting of a list of Units
-party_indv1    : list(Unit) : The party composition indv1 will use, consisting of a list of Units
-num_battles    : int : The number of battles to simulate
-win_score      : float : The fitness score awarded to the winner of a battle
-lose_score     : float : The fitness score awarded to the loser of a battle
-survivor_bonus : float : The bonus score awarded to the winner for each surviving unit
-kill_bonus     : float : The bonus score awarded to the loser for each of the winner's units it managed to kill
-debug          : boolean : If set to true, will print out operational details to console. Only used for testing purposes.

Returns:
-Nothing, as fitness scores are awarded to individual objects directly through their fitness attributes
"""
def simulate_battles(indv0,indv1,party_indv0,party_indv1,num_battles,win_score,lose_score,survivor_bonus,kill_bonus,debug=False):
    
    # simulate the battles
    for i in range(num_battles):
        # have the individuals take turns going first
        # (note that indv0 goes first if i is even, but indv1 goes first if i is odd)
        if (i%2 == 0):
            winner, survivors = battle(indv0,indv1,party_indv0,party_indv1)
            # award score based on outcome
            if winner == 0:
                if debug: print("Indv0 wins battle",i,"with",survivors,"survivors.")
                indv0.curr_fitness += win_score + (survivors*survivor_bonus)
                indv1.curr_fitness += lose_score + ((len(party_indv0)-survivors)*kill_bonus)
                indv0.lifetime_win_count += 1
            elif winner == 1:
                if debug: print("Indv1 wins battle",i,"with",survivors,"survivors.")
                indv0.curr_fitness += lose_score + ((len(party_indv1)-survivors)*kill_bonus)
                indv1.curr_fitness += win_score + (survivors*survivor_bonus)
                indv1.lifetime_win_count += 1
            else:
                if debug: print("Battle",i,"is a tie")
                indv0.curr_fitness += (win_score+lose_score)/2
                indv1.curr_fitness += (win_score+lose_score)/2
        
        else:
            winner, survivors = battle(indv1,indv0,party_indv1,party_indv0)
            # award score based on outcome
            if winner == 0:
                if debug: print("Indv1 wins battle",i,"with",survivors,"survivors.")
                indv1.curr_fitness += win_score + (survivors*survivor_bonus)
                indv0.curr_fitness += lose_score + ((len(party_indv1)-survivors)*kill_bonus)
                indv1.lifetime_win_count += 1
            elif winner == 1:
                if debug: print("Indv0 wins battle",i,"with",survivors,"survivors.")
                indv1.curr_fitness += lose_score + ((len(party_indv0)-survivors)*kill_bonus)
                indv0.curr_fitness += win_score + (survivors*survivor_bonus)
                indv0.lifetime_win_count += 1
            else:
                if debug: print("Battle",i,"is a tie")
                indv1.curr_fitness += (win_score+lose_score)/2
                indv0.curr_fitness += (win_score+lose_score)/2

        # increment the battle counter for both individuals
        indv0.battle_count += 1
        indv1.battle_count += 1
        indv0.lifetime_battle_count += 1
        indv1.lifetime_battle_count += 1

    return

"""
strat0 = [[10000,10,1],[10000,10,1],[10000,10,1]]
strat1 = [[4,4,4],[4,4,4],[4,4,4]]
indv0 = representation.Strategy(0,3,strat0)
indv1 = representation.Strategy(0,3,strat1)

party = []
for i in range(len(strat0)):
    unit = representation.Unit(i,4,10)
    party.append(unit)

battle(indv0,indv1,party,party,debug=True)
"""