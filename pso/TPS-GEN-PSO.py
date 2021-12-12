"""
CISC455 Final Project
Target Prioritization Strategies - Particle Swarm Optimization

Joshua Chai-Tang 20119074
"""

from cost_functions import translate_and_evaluate
import pso_simple
import evaluation
import representation

def main():

    # set party size
    party_size = 4

    # determine initial particle (strat matrix) conditions
    initial = [5]*(party_size*party_size)
    # set the boundaries
    bounds = [(1,99)]*(party_size*party_size)

    # minimize
    result, particle = pso_simple.minimize(translate_and_evaluate,initial,bounds,num_particles=25,maxiter=100,verbose=True)

    translate_and_evaluate(particle,debug=True)

    return

def test():
    particle = [7.558151245676082, 2.2712238019891435, 15.7502493362461, 12.897263008073068, 1.0034778495853016, 7.5453372454625045, 21.761444682425054, 1.0, 8.031708656988956, 1.0, 17.084758051362623, 8.946878887779839, 1.0, 14.290377784437375, 1.0, 3.1202214400128065]
    translate_and_evaluate(particle,debug=True)

main()