import numpy as np
import math
import random
# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.initial_location = initial_location
        self.travelled_distance = 0
        self.log_book = []
        

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        all_locations = self.environment.get_possible_locations()
        visited_locations = []
        visited_locations.append(self.current_location)
        while(len(visited_locations) < 48):
            #get all possible distances
            coordinates_to_choose_from = {}
            coordinates_current_location = all_locations[self.current_location]
            for possible_location in range(all_locations.shape[0]):
                if not possible_location in visited_locations:
                    coordinates_to_choose_from[possible_location] = self.environment.euclidean_distance(coordinates_current_location, all_locations[possible_location])
            #calculate where to go next
            sum_all_value = 0
            p_values_dict = {}
            # calculate some of the p-value
            for location in coordinates_to_choose_from.keys():
                pheromone_value = self.environment.get_pheromone_value(self.current_location, location)
                distance_to_target = self.environment.get_distance(self.current_location, location)
                d_value = 1 / distance_to_target
                sum_all_value = sum_all_value + ((pheromone_value) ** self.alpha * (d_value) ** self.beta)
            # calculate indidviual p-value
            for location in coordinates_to_choose_from.keys():
                pheromone_value = self.environment.get_pheromone_value(self.current_location, location)
                distance_to_target = self.environment.get_distance(self.current_location, location)
                d_value = 1 / distance_to_target
                p_value = (((pheromone_value) ** self.alpha * (d_value) ** self.beta)) / sum_all_value
                p_values_dict[location] = p_value
            # one should take a random number out of this probability
            go_to_location = self.select_probable_number(p_values_dict)
            
                
            #update the travelled distance
            distance_to_travel = self.environment.get_distance(self.current_location, go_to_location)
            self.travelled_distance = self.travelled_distance + distance_to_travel
            #update visited_locations
            visited_locations.append(go_to_location)
            #update log_book
            self.log_book.append([self.current_location, go_to_location])
            self.current_location = go_to_location
        # add final step
        self.travelled_distance = self.travelled_distance + self.environment.get_distance(self.current_location, self.initial_location)
        self.log_book.append([self.current_location, self.initial_location])

    def distance_per_iteration(self):
        return self.travelled_distance
    
    def select_probable_number(self,data):
        # Sort the dictionary by values in descending order
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        
        # Extract the keys and probabilities from the sorted data
        keys = [item[0] for item in sorted_data]
        probabilities = [item[1] for item in sorted_data]
        
        # Select a random key based on probabilities
        selected_key = random.choices(keys, probabilities)[0]
    
        # Return the selected key
        return selected_key
        
    def init_ant(self):
        self.travelled_distance = 0
        self.log_book = []
        self.current_location = self.initial_location

    
    def get_log_book(self):
        return self.log_book


    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
        
