from data.ReadInstance import ReadInstance
from models.input.Today import Today
from algorithm.algorithm import Algorithm
from utils.ml_enum import MachineLearningEnum

if __name__ == '__main__':
    instance_name = 'n_50_10_100_1000.txt'
    read_instance = ReadInstance(instance_name)
    problem = read_instance.read_instance()
    today = Today(hour=10, day=1, weather='sunny', temperature=20, humidity=50, wind_speed=10)
    algorithm = Algorithm(problem)
    algorithm.run(today)

    problem.generate_ml_initial_solution(today, MachineLearningEnum.LINEAR_REGRESSION)
    
