
class GRASP:
    def __init__(self, problem):
        self.problem = problem
        self.n_nodes = problem.n_nodes
        self.truck_capacity = problem.truck_capacity
        self.historical_data = problem.historical_data

