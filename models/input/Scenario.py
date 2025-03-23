class Scenario:
    def __init__(self, problem, demands, hour_of_day = None, day_of_week = None, weather_condition = None, temperature = None, humidity = None, wind_speed = None):
        self.hour_of_day = hour_of_day
        self.day_of_week = day_of_week
        self.weather_condition = weather_condition
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed

        self.demands = demands
        self.distances_matrix = problem.distances_matrix
        self.cost_per_km = problem.cost_per_km
        self.cost_per_undelivered_demand = problem.cost_per_undelivered_demand

    def calculate_cost(self, route):
        cost = self.cost_per_undelivered_demand * sum(self.demands)
        for i, node in enumerate(route):
            distance = self.distances_matrix[route[i-1]][route[i]]
            cost += self.cost_per_km * distance
            
            demand = self.demands[node]
            cost -= self.cost_per_undelivered_demand * demand
        return cost
