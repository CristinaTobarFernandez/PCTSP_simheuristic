from algorithm.algorithm import Algorithm
from utils.ml_enum import MachineLearningEnum

class MLAlgorithm(Algorithm):
    def __init__(self, problem, n_scenarios_first_step: int, n_scenarios_second_step: int, today, ml_model: MachineLearningEnum):
        super().__init__(problem, n_scenarios_first_step, n_scenarios_second_step)
        self.today = today
        self.ml_model = ml_model

    def run(self):
        pass

    def generate_initial_solution(self):
        self.problem.generate_ml_initial_solution(self.today, self.ml_model)
    
    def generate_scenarios(self):
        self.problem.generate_knn_scenarios(self.today, self.n_scenarios_first_step, self.n_scenarios_second_step)

    def evaluate_solution_in_selected_scenarios_first_step(self, solution, scenarios):
        pass

    def evaluate_solution_in_selected_scenarios_second_step(self, solution, scenarios):
        pass

    def evaluate_solution(self, solution):
        pass
