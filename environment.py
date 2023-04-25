import math
import tsplib95
import numpy as np

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
"""
class Environment:
    def __init__(self, rho):

        self.rho =rho
        
        # Initialize the environment topology
        self.problem = tsplib95.load('att48-specs/att48.tsp')

        self.distance_matrix = np.loadtxt('att48-specs/att48_distance_matrix.txt')
        self.coordinates = np.loadtxt('att48-specs/att48_coordinates.txt')
        

        # Intialize the pheromone map in the environment
        self.coord_list = list(self.problem.as_name_dict()['node_coords'].keys())

        self.ants = []
        # 1 as taken by the book
        change_to_1 = lambda x: 1 if x != 0 else x
        self.pheromone_map = np.vectorize(change_to_1)(self.distance_matrix)


    # Intialize the pheromone trails in the environment
    def initialize_pheromone_map(self, number_of_ants:int):
        expected_cost_of_tour = number_of_ants
        # 1 as taken by the book
        change_to_1 = lambda x: 1 if x != 0 else x
        self.pheromone_map = np.vectorize(change_to_1)(self.pheromone_map)


    # Update the pheromone trails in the environment
    def update_pheromone_map(self,ants):
        # remove pheromone from the arcs
        update_rho = lambda x: x * (1 - self.rho)
        self.pheromone_map = np.vectorize(update_rho)(self.pheromone_map)

        #calculate new pheromone 
        for ant in ants:
            c = ant.distance_per_iteration()
            if (c != 0):
                c_update = 1 / c
                ant_path = ant.get_log_book()
                for log_entry in range(len(ant_path)):
                    from_location = ant_path[log_entry][0]
                    to_location = ant_path[log_entry][1]
                    self.pheromone_map[from_location][to_location] = self.pheromone_map[from_location][to_location] + c_update
                    
    def get_pheromone_value(self,from_location, to_location):
        return self.pheromone_map[from_location][to_location]

    def get_distance(self, from_location, to_location):
        coord1 = self.coordinates[from_location]
        coord2 = self.coordinates[to_location]
        return self.euclidean_distance(coord1, coord2)
    
    # Get the environment topology
    def get_possible_locations(self):
        return self.coordinates
    
    def euclidean_distance(self,coord1, coord2):
        distance = math.sqrt((coord2[0] - coord1[0]) **2  + (coord2[1] - coord1[1]) ** 2)
        return distance 
    


    
