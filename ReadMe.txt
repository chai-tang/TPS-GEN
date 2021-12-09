==================================
CISC455 Final Project - Genetic Algorithm for Target Prioritization Strategies
Joshua Chai-Tang 20119074
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
The initialization process is as straightforward as it gets. The core on an individual is their strat, which is simply a square 2D array. Therefore generating a random individual really just means generating a series of random TPVL's, which itself just means generating a list of random numbers. The function takes inputs for setting the upper and lower limits for random number generation, but what these values are isn't very important. So long as both limits are positive (ABSOLUTELY NOT ZERO OR LOWER) and have a decently large range of possible values between them, everything should run just fine. There's not much else to say about it, the code is pretty simple and self evident. 

----------------------------------
3. Evaluation
----------------------------------
As you would expect, the central function of the evaluation module is 'battle'. This function simulates a battle between two individuals and determines who the winner is, which is pretty much the single most important function of the entire algorithm because winning battles translates directly into high fitness. 

At the start of a battle each strategy gets its own copy of the party. Initially all units are set to their maximum health value. The fight itself it broken into rounds. At the start of each round, all units on either side select a target unit in the opposite party. Targets are selected probabilistically based on each strategy's TPVL for that particular unit. The random.choices() function makes selecting targets at random with different weighting for each very easy. Importantly, dead units cannot be selected as targets in this phase.

After targets are chosen, units on either side take turns 'attacking'. An 'attack' consists of subtracting the attacking unit's attack value from the target unit's health value. Every unit gets to make exactly one attack per round. Units whose health is reduced to or below 0 are considered 'dead', and are thus no longer able to make attacks in current or future rounds. Combat continues by simulating more rounds until one or both sides have no 'living' units left, at which point the victor is declared. I strongly recommend you run this function a couple times with debug mode on just to see how it all works.

Some important factors to note about how combat works: 

-Both parties must be of the same size. Hopefully I'l change that at some point in the future, but for now that's how it works. 

-If a unit's target dies before its turn, the unit effectively wastes its turn attacking a target that's already dead. This is because the target selection phase occurs before the attacking phase, so units don't get to change targets in the middle or a round. This definitely has some effect on the kinds of strategies this algorithm selects for. I'm not yet sure if that's a good thing or not. For the time being I'm leaving it as is, but I may consider changing this in the future. Besides, there are a decent number of games whose combat works similarly to this.

-Some parts of my functions are setup to account for ties, which never actually happen under the turn based system. This is because my original plan was to not use turn based combat, but rather have all attacks in a round occur simultaneously. I have since abandoned that plan, mainly to make development easier for myself, but the tie system remains. I'm still curious as to how that system would affect the emerging strategies, so I might end up implementing it in the future, but for now combat is turn based.

-Turn order is a big deal. Strat0 always goes first, and units attack in ascending order as well (meaning Unit0 always acts before Unit1, etc). The turn order is essentially strat0_unit0, strat1_unit0, strat0_unit1, strat1_unit1, strat0_unit2 ... and so on for each round. This means that strat0 has a huge advantage over strat1 because it is more likely to kill enemy units before they get a turn. It also means that units with lower numbers are disproportionately more important than those with higher numbers, but since that effect is symmetrical for both sides I don't consider it a problem. 

To account for the turn order advantage, as well as to account for the inherently random nature of battle outcomes, I determine strategy fitness by always running multiple battles. This is accomplished in the simulate_battles() function, which is affected by the battles_per_test variable in main(). After a battle, both individuals are awarded score values based on a couple parameters. Winning obviously grants a large score value. Losing grants little to none. There is also a bonus score awarded to the winner for each surviving unit at the end of the battle, as well as a bonus to the loser based on how many enemy units it managed to kill before losing. These score values are added directly to an individual's curr_fitness attribute. Their battle_count attribute is also incremented after each battle. After all the battles have been simulated, scores are normalized in main() calculating curr_fitness / battle_count. This value is then assigned to the individual's fitness attribute. Fitness is thus representative of how successful an individual performed in the battle, averaged across the number of battles it was in. In addition to prioritizing winning, this evaluation method also rewards individuals that can win without minimal losses, or who can inflict maximum losses on the enemy in case of defeat. This doesn't entirely eliminate the problem of non-deterministic fitness evaluation, but I believe that so long as the number of battles_per_test is adequately large then statistically it works out to be more or less an objective measure.

Now, there's two main theories for how to pick which individuals should battle each other during fitness evaluation. The current theory is to have all enemies face the same opponent, called the 'baseline' strategy. This ensures that all individuals are evaluated against the same criteria, which maximizes fairness and eliminates an aspect of randomness that could otherwise skew simulation results. This method keeps things simple and ensures that the goalposts remain fixed, but it's far from ideal. For one, the exact details of this baseline could really make or break the algorithm. A baseline that's too weak won't present enough selection pressure, allowing for relatively weak strategies to earn high fitness scores. But a baseline that's too strong will crush new strategies before they have a chance to develop, leading to premature convergence of suboptimal strategies. Getting this balance right will prove to be incredibly important to the success of this algorithm.

The other theory, and this was my original idea, is to have the individuals battle against each other every generation. This forces old strategies to be constantly tested against new ones, and creates an incredibly interesting dynamic where the 'optimal' strategy is a constantly shifting goal that evolves over time. On one hand, that's really cool and could make for fascinating results. On the other hand, this not only makes the algorithm more complex but also introduces elements of randomness which could negatively impact the algorithm. Realistically I can't have every individual battle every other individual; even my PC would struggle to run that many simulations in a reasonable amount of time. My compromise is an option called 'do_tournament_battles'. More on that below.

----------------------------------
4. Tournament
----------------------------------
I decided to use the same parent/survivor selection methods from assignment 2, so I also got to reuse that entire module's code with minimal adjustments. The tournament method simply consists of selecting multiple random individuals and comparing their fitness values to each other. Those with the highest fitness are selected as parents, while those with the lowest are replaced by the children. There's not much else to say, it's a relatively simple module. One thing to note is that it is possible for an individual to be both the winner and the loser of a tournament if all contestants in that round have equal fitness, but in that case the offspring will just replace their own parents.

As I mentioned above, there's an additional option called 'do_tournament_battles' which makes things a bit more complex. When set to true, during each parent/survivor selection tournament every contestant will have battles simulated against all other contestants. Fitness is determined by the performance of an individual across all tournament battles. The advantage of this method is that potential parents are now competing directly with each other, rather than against an unchanging baseline. This should increase selection pressure by allowing superior strategies to prove themselves against weaker ones directly. However it also increases the program's runtime, which is already getting quite long. Whether or not I keep this option on may vary between tests.

----------------------------------
5. Recombination
----------------------------------
Single point crossover was my recombination method of choice because it's the simplest. Since every individual's strat has equal length, performing crossover with them proves a very simple task. All I have to do is pick a crossover point and exchange TPVL's to create two children. I considered performing crossover within each TPVL too, but I decided that my mutation method would be adequate for altering TPV's so there was no need to make the algorithm any more complex. One thing to note is that it's possible for no crossover to occur at all, thus creating children that are identical to the parents. I think that's perfectly acceptable, especially since the children still undergo mutation.

----------------------------------
6. Mutation
----------------------------------
For mutation, I opted to use a much more aggressive method than in assignment 2. I didn't want to limit my mutation methods to only changing a single TPV or TPVL in each individual because that could end up being too small a change to matter when simulating with large parties. Instead, I opted for a more universal mutation method. My method iterates through every single value in every single TPVL of the individual and randomly selects TPV's to mutate, based on the mutation rate. A mutated TPV is replaced with an entirely new value, generated randomly between the given limits. Essentially this means that every TPV is up for mutation. Statistically this does mean that it's incredibly unlikely for an individual to not get mutated at all, which I admit might have negative consequences. But it also means that mutations remain significant for any and all party sizes. I suspect that mutation rate is going to be a very important value to tinker around with. Getting that rate right could make or break this algorithm.

----------------------------------
7. Conclusions
----------------------------------
Conclusions are discussed in the main project report.


