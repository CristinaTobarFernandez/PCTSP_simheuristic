from models.input.Node import Node
from models.input.Scenario import Scenario
from utils.ml_models import MLModels
from utils.ml_enum import MachineLearningEnum
import numpy as np

class Problem:
    def __init__(self):
        self.nodes = []
        self.historical_data = []
        self.n_nodes = None
        self.truck_capacity = None
        self.cost_per_km = 100
        self.cost_per_undelivered_demand = 10

        self.distances_matrix = None

        self.scenarios_first_step = []
        self.scenarios_second_step = []

    def feed_historical_data(self, historical_data):
        for historical_data in historical_data:
            hour_of_day = historical_data[0]
            day_of_week = historical_data[1]
            weather_condition = historical_data[2]
            temperature = historical_data[3]
            humidity = historical_data[4]
            wind_speed = historical_data[5]
            demands = historical_data[6:6+self.n_nodes]
            
            self.historical_data.append(Scenario(self, demands,
                                                 hour_of_day, 
                                                 day_of_week, 
                                                 weather_condition, 
                                                 temperature, 
                                                 humidity, 
                                                 wind_speed))
            
        self.historical_demand = {node.index: {'X_train': [], 'y_train': []} 
                                          for node in self.nodes}
        for scenario in self.historical_data:
            for node in self.nodes:
                self.historical_demand[node.index]['X_train'].append((scenario.hour_of_day, scenario.day_of_week, 
                                                     scenario.weather_condition, scenario.temperature, 
                                                     scenario.humidity, scenario.wind_speed))
                self.historical_demand[node.index]['y_train'].append(scenario.demands[node.index])

    def feed_nodes(self, nodes):
        for node, x, y in nodes:
            self.nodes.append(Node(node, x, y))
        
        self.distances_matrix = [[None for _ in range(self.n_nodes)] for _ in range(self.n_nodes)]
        for node in self.nodes:
            for node2 in self.nodes:
                if self.distances_matrix[node.index][node2.index] is None:
                    distance = ((node.x - node2.x)**2 + (node.y - node2.y)**2)**0.5
                    self.distances_matrix[node.index][node2.index] = distance
            
    def generate_clasical_initial_solution(self):
        initial_solution = []

        historical_demand = {node.index: [] for node in self.nodes}
        for scenario in self.historical_data:
            for node in self.nodes:
                historical_demand[node.index].append(scenario.demands[node.index])

        for node in self.nodes:
            mean_demand = sum(historical_demand[node.index]) / len(historical_demand[node.index])
            initial_solution.append(mean_demand)

        return initial_solution
    
    def generate_log_normal_scenarios(self, n_scenarios_first_step, n_scenarios_second_step):
        demands = {node.index: [] for node in self.nodes}

        historical_demand = {node.index: [] for node in self.nodes}
        for scenario in self.historical_data:
            for node in self.nodes:
                historical_demand[node.index].append(scenario.demands[node.index])

        for node in self.nodes:
            mean_demand = sum(historical_demand[node.index]) / len(historical_demand[node.index])
            std_demand = np.std(historical_demand[node.index])
            demands[node.index] = np.random.lognormal(mean=mean_demand, sigma=std_demand, size=n_scenarios_second_step)
        
        for s in self.n_scenarios:
            scenario_demands = [demands[node.index][s] for node in self.nodes]
            scenario = Scenario(self, scenario_demands)
            if s < n_scenarios_first_step:
                self.scenarios_first_step.append(scenario)
            self.scenarios_second_step.append(scenario)

    
    def generate_ml_initial_solution(self, today, ml_model: MachineLearningEnum):
        self.historical_demand['X_test'].append((today.hour, today.day, today.weather, today.temperature, today.humidity, today.wind_speed))

        initial_solution = []

        for node in self.nodes:
            initial_solution.append(MLModels.predict(X_train=historical_demand[node.index]['X_train'], 
                                                     y_train=historical_demand[node.index]['y_train'], 
                                                     X_test=historical_demand[node.index]['X_test'], 
                                                     model=ml_model))
        return initial_solution

    def generate_knn_scenarios(self, today, n_scenarios_first_step, n_scenarios_second_step):
        self.historical_demand['X_test'].append((today.hour, today.day, today.weather, today.temperature, today.humidity, today.wind_speed))

        demands = {node.index: [] for node in self.nodes}

        for node in self.nodes:
            node_demands = MLModels.generate_knn_scenarios(X_train=self.historical_demand[node.index]['X_train'], 
                                                           y_train=self.historical_demand[node.index]['y_train'], 
                                                           X_test=self.historical_demand[node.index]['X_test'], 
                                                           n_scenarios=n_scenarios_second_step)
            demands[node.index] = node_demands

        for s in n_scenarios_second_step:
            scenario_demands = [demands[node.index][s] for node in self.nodes]
            scenario = Scenario(self, scenario_demands, today.hour, today.day, today.weather, today.temperature, today.humidity, today.wind_speed)
            if s < n_scenarios_first_step:
                self.scenarios_first_step.append(scenario)
            self.scenarios_second_step.append(scenario)