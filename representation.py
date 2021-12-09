"""
CISC455 Final Project
Representation Module

This file will define all key data structures (classes) used in my algorithm to represent solutions.

Joshua Chai-Tang 20119074
"""

"""
Defines the Unit object, which represents a single unit within a party.
A party will consist of a list of units.

Attributes:
-id     : int : The identifying number of this unit, usually corresponds to its position in the party
-attack : int : The amount of damage this unit deals to an enemy unit's health when attacking 
-health : int : The number of 'Hit Points' this unit has, which determines how much damage it can take before 'dying'

Methods
__repr__ & __str__ : Simple override methods to allow this unit's values to be printed to console in a readable manner. Only used for debugging, serves no actual purpose to the algorithm.
"""
class Unit:
    def __init__(self,id,attack,health):
        self.id = id
        self.attack = attack
        self.health = health
    def __repr__(self):
        return str(self)
    def __str__(self):
        return "<"+str(self.attack)+","+str(self.health)+">"


"""
Defines the strategy object, which represents a particular individual within the population.
Each strategy consists of a series of target priority value lists (TPVL's), with one such list for each unit in the party.
The TPVs are used to determine which units should attack which enemy units during battle.

Attributes:
-age          : int : Identifies which generation this individual belongs to
-size         : int : The party size this individual is designed for
-strat        : list(list(float)) : A list which contains the TPVL's for each unit
-curr_fitness : float : Records the current sum of fitness scores earned in battles so far. Resets to 0 when being re-evaluated.
-battle_count : int : Records the number of battles this strategy has participated in so far. Resets to 0 when being re-evaluated.
-fitness      : float : Once all battles are complete, fitness will be equal to curr_fitness / battle_count to determine average battle performance.

Methods:
__repr__ & __str__ : Simple override methods to allow a summary of this strategy to be printed to console in a readable manner. Only used for debugging, serves no actual purpose to the algorithm.
"""
class Strategy:
    def __init__(self,age,size,strat):
        self.age = age
        self.size = size
        self.strat = strat
        self.curr_fitness = 0
        self.battle_count = 0
        self.fitness = 0
    def __repr__(self):
        return str(self)
    def __str__(self):
        output = ">Strategy of size "+str(self.size)+" from Generation #"+str(self.age)+":\n"
        for unit in range(len(self.strat)):
            output += ">Unit"+str(unit)+": "+str(self.strat[unit])+"\n"
        output += ">Most Recent Fitness Value: "+str(self.fitness)
        return output
