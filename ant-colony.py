import numpy as np

from environment import Environment
from ant import Ant 

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""
class AntColony:
    def __init__(self, ant_population: int, iterations: int, alpha: float, beta: float, rho: float):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho 

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho)


        # Initilize the list of ants of the ant colony
        self.ants = []


        # Initialize the ants of the ant colony
        for i in range(ant_population):

            # Initialize an ant on a random initial location 

            ant = Ant(self.alpha, self.beta, (i % 48) )

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)
        
            # Add the ant to the ant colony
            self.ants.append(ant)

        self.environment.initialize_pheromone_map(ant_population)

        

    # Solve the ant colony optimization problem  
    def solve(self):

        shortest_distance_sol = np.Inf
        solution_book = []

        #update path
        for iteration in range(self.iterations):
            for ant in self.ants:
                ant.run()
            #get ant_with_shortest_distance
            paths = {}
            log_books = {}
            
            
            for ant in range(len(self.ants)):
                paths[ant] = self.ants[ant].distance_per_iteration()
                log_books[ant] = self.ants[ant].get_log_book()
            shortest_distance_key = min(paths, key=paths.get)
            maybe_best = paths[shortest_distance_key]
            if maybe_best < shortest_distance_sol:
                print('shortest distance key', shortest_distance_key, maybe_best)
                shortest_distance_sol = maybe_best
                solution_book = log_books[shortest_distance_key]
            
            self.environment.update_pheromone_map(self.ants)

            for ant in self.ants:
                ant.init_ant()

        #if statement for a solution


        # The solution will be a list of the visited cities
        solution = solution_book

        # Initially, the shortest distance is set to infinite
        shortest_distance = shortest_distance_sol

        return solution, shortest_distance


def main():
    # Intialize the ant colony
    ant_colony = AntColony(48, 500,1, 5,0.5)

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()

    #need to add 1 to every node because indexes start with 0 :-)
    new_solution = []
    for [x,y] in solution:
        new_solution.append([x+1, y+1])
        

    print("Solution: ", new_solution)
    print("Distance: ", distance)


if __name__ == '__main__':
    main()    