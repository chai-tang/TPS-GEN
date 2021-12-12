# TPS-GEN

CISC455 Final Project by Joshua Chai-Tang 

Genetic Algorithm for Target Prioritization Strategies
==================================

This document contains the explanation for my implementation of a genetic programming algorithm designed to generate target priority strategies. The project report will contain more details about what that means, so this readme is only focused on the technical aspects. I chose to implement the algorithm in Python3 because that's what I'm familiar with and because it allowed me to reuse a lot of my assignment 2 code. Similar to my A2 readme, this document is primarily focused on rationalizing my implementation decisions since all of my functions contain comments to explain finer details.

----------------------------------
1. Representation
----------------------------------
An individual in this algorithm is called a 'Strategy', implemented as an object class with the same name. Most of the attributes are for record keeping purposes, such as the individual's age and the party size it's designed for. The most important value is 'strat', which is a square 2D array that maps an array of numbers to each unit in the party. Those subarrays are called TPVL's, and their values are used to determine which how the unit it's mapped to chooses its targets in battle. More explanation of on how that works can be found in the project report. Essentially an individual's strat is really what defines an its behaviour, and these TPVL's are what the algorithm is designed to optimize. A highly successful individual is one whose TPVL's allow them to win the majority of battles they partake in. 

Other values to note are the three fitness attributes, which are discussed in more detail in the evaluation section.

The only other class defined in this module is the 'Unit'. Units are really just pairs of integers, one to represent attack damage and another to represent health. Each party consists of a list of Unit objects, and these Units are what 'fight' each other during battle simulations. Again, more detail on that is in the project report.
Technically the Unit object is simple enough that it could have just been a tuple or list. But I liked the idea of being able to call unit.health and unit.attack rather than unit[0] or unit[1] to refer to these values. It also made me generally less worried about Python3's aliasing issues. This decision proved useful for readability purposes, although it probably has a negative impact on algorithm efficiency (especially in terms of memory usage). Thankfully I'm not too worried about memory usage or runtime now that I can run the algorithm on my significantly more powerful PC instead of a laptop.

----------------------------------
2. Initialization
----------------------------------
The initialization process is as straightforward as it gets. The core on an individual is their strat, which is simply a square 2D array. Therefore generating a random individual really just means generating a series of random TPVL's, which itself just means generating a list of random numbers. The function takes inputs for setting the upper and lower limits for random number generation, but what these values are isn't very important. So long as both limits are positive (ABSOLUTELY NOT ZERO OR LOWER) and have a decently large range of possible values between them, everything should run just fine. I chose 1 and 99 as my limits. There's not much else to say about it, the code is pretty simple and self evident. 

----------------------------------
3. Evaluation
----------------------------------
As you would expect, the central function of the evaluation module is 'battle'. This function simulates a battle between two individuals and determines who the winner is, which is pretty much the single most important function of the entire algorithm because winning battles translates directly into high fitness. 

At the start of a battle each strategy gets its own copy of the party. Initially all units are set to their maximum health value. The fight itself it broken into rounds. At the start of each round, all units on either side select a target unit in the opposite party. Targets are selected probabilistically based on each strategy's TPVL for that particular unit. The random.choices() function makes selecting targets at random with different weighting for each very easy. Importantly, dead units cannot be selected as targets in this phase.

After targets are chosen, units on either side take turns 'attacking'. An 'attack' consists of subtracting the attacking unit's attack value from the target unit's health value. Every unit gets to make exactly one attack per round. Units whose health is reduced to or below 0 are considered 'dead', and are thus no longer able to make attacks in current or future rounds. Combat continues by simulating more rounds until one or both sides have no 'living' units left, at which point the victor is declared. I strongly recommend you run this function a couple times with debug mode on just to see how it all works.

Some important factors to note about how combat works: 

-Both parties must be of the same size. Hopefully I'l change that at some point in the future, but for now that's how it works. In the meantime, you can add filler <0,0> units to a party that effectively die at the very beginning of combat.

-If a unit's target dies before its turn, the unit effectively wastes its turn attacking a target that's already dead. This is because the target selection phase occurs before the attacking phase, so units don't get to change targets in the middle or a round. This definitely has some effect on the kinds of strategies this algorithm selects for. I'm not yet sure if that's a good thing or not. For the time being I'm leaving it as is, but I may consider changing this in the future. Besides, there are a lot of games whose combat works on a turn based system.

-Some parts of my functions are setup to account for ties, which never actually happen under the turn based system. This is because my original plan was to not use turn based combat, but rather have all attacks in a round occur simultaneously. I have since abandoned that plan, mainly to make development easier for myself, but the tie system remains. I'm still curious as to how that system would affect the emerging strategies, so I might end up implementing it in the future, but for now combat is turn based.

-Turn order is a big deal. Strat0 always goes first, and units attack in ascending order as well (meaning Unit0 always acts before Unit1, etc). The turn order is essentially strat0_unit0, strat1_unit0, strat0_unit1, strat1_unit1, strat0_unit2 ... and so on for each round. This means that strat0 has a huge advantage over strat1 because it is more likely to kill enemy units before they get a turn. It also means that units with lower numbers are disproportionately more important than those with higher numbers, but since that effect is symmetrical for both sides I don't consider it a problem. 

To account for the turn order advantage, as well as to account for the inherently random nature of battle outcomes, I determine strategy fitness by always running multiple battles. This is accomplished in the simulate_battles() function, which runs a number of battles equal to the battles_per_test parameter in main(). After a battle, both individuals are awarded score values based on the fitness score parameters. Winning obviously grants a large score value. Losing grants little to none. There is also a bonus score awarded to the winner for each surviving unit at the end of the battle, as well as a bonus to the loser based on how many enemy units it managed to kill before losing. These score values are added directly to an individual's curr_fitness attribute. Their battle_count attribute is also incremented after each battle. After all the battles have been simulated, scores are normalized in main() by calculating curr_fitness / battle_count. This value is then assigned to the individual's fitness attribute.  This function doesn't entirely eliminate the problem of non-deterministic fitness evaluation, but I believe that so long as the number of battles_per_test is adequately large then statistically it works out to be more or less an objective measure.

Now, there's two main theories for how to pick which individuals should battle each other during fitness evaluation. Those are covered in the main project report under sections 2.3.1 and 2.3.2. For the baseline method I'd use 50 battles_per_test, though it ultimately proved too difficult to find a good enough baseline strategy to make this method work. For the tournament battles method I'd use only 5 battles_per_test because individuals could participate in multiple tournaments throughout the simulation. On average most top individuals ended up fighting in over 200 battles total. 

----------------------------------
4. Tournament
----------------------------------
I decided to use the same parent/survivor selection methods from assignment 2, so I also got to reuse that entire module's code with minimal adjustments. The tournament function simply consists of selecting multiple random individuals and comparing their fitness values to each other. Under the baseline method that just means comparing their fitness scores earned from battling the baseline. Under the tournament battles method, that meant simulating battles between all the potential parents directly and then comparing those fitness scores. Individuals with the highest fitness are selected as parents, while those with the lowest are replaced by the children. 

----------------------------------
5. Recombination
----------------------------------
Single point crossover was my recombination method of choice because it's the simplest. Since every individual's strat has equal length, performing crossover with them proves a very simple task. All I have to do is pick a crossover point and exchange TPVL's to create two children. I considered performing crossover within each TPVL too, but I decided that my mutation method would be adequate for altering TPV's so there was no need to make the algorithm any more complex. One thing to note is that it's possible for no crossover to occur at all if the crossover point is either 0 or party_size, thus creating children that are identical to the parents. I think that's perfectly acceptable, especially since the children still undergo mutation.

----------------------------------
6. Mutation
----------------------------------
For mutation, I opted to use a much more aggressive method than in assignment 2. I didn't want to limit my mutation methods to only changing a single TPV or TPVL in each individual because that could end up being too small a change to matter when simulating with large parties. Instead, I opted for a more universal mutation method. My method iterates through every single value in every single TPVL of the individual and randomly selects TPV's to mutate, based on the mutation rate. A mutated TPV is replaced with an entirely new value, generated randomly between the given limits. Essentially this means that every TPV is up for mutation. Statistically this does mean that it's incredibly unlikely for an individual to not get mutated at all, which I admit might have negative consequences. But it also means that mutations remain significant for any and all party sizes. I suspect that mutation rate is going to be a very important value to tinker around with. Getting that rate right could make or break this algorithm.

----------------------------------
7. Particle Swarm Optimization
----------------------------------
The pso folder contains the modified particle swarm optimization algorithm I used to compare to my genetic algorithm. The majority of the complicated stuff is in the pso_simple.py file, which was made by Nathan Rooy. I suggest you refer his documentation to fully understand the details of his implementation. In terms of my edits, the only major modification needed was a way to translate the particle object into a strategy object. Particles only support being represented as one dimensional arrays, while Strategies require 2D Strat matrices. Thankfully the conversion is incredibly simple because all Strat matrices for a given party have the same n*n square dimensions. Thus the particle just needs to be an n*n length list, which my translate_and_evaluate function easily breaks into n lists of length n to comprise a Strat matrix. It then simulates battles against the baseline and determines fitness score in exactly the same way my GA does. Since Rooy's module is designed to minimize fitness, I simply invert the fitness score by subtracting the result from the maximum potential fitness (which could only be achieved by winning every simulated battle). This translate_and_evaluate function serves as the particle fitness evaluation function passed to Rooy's pso module. The best strategies produced by my GA were inputted manually for comparison.
