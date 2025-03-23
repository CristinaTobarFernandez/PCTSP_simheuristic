class Algorithm():
    def __init__(self, problem):
        self.problem = problem
        self.n_scenarios_first_step = 100
        self.n_scenarios_second_step = 1000
    
    def run(self, today):
        pass

    def generate_initial_solution(self):
        pass

    def evaluate_solution_in_selected_scenario(self, solution, scenarios):
        pass

    def evaluate_solution(self, solution):
        pass
