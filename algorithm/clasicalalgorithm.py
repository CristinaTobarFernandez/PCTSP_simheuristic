from algorithm.algorithm import Algorithm
from models.input.Problem import Problem

class ClasicalAlgorithm(Algorithm):
    def __init__(self, problem, n_scenarios_first_step: int, n_scenarios_second_step: int):
        super().__init__(problem, n_scenarios_first_step, n_scenarios_second_step)

    def run(self):
        pass

    def generate_initial_solution(self):
        self.problem.generate_clasical_initial_solution()
    
    def generate_scenarios(self):
        self.problem.generate_log_normal_scenarios(self.n_scenarios_first_step, self.n_scenarios_second_step)

    def evaluate_solution_in_selected_scenarios_first_step(self, solution, scenarios):
        pass

    def evaluate_solution_in_selected_scenarios_second_step(self, solution, scenarios):
        pass

    def evaluate_solution(self, solution):
        pass
    
    
