import pandas as pd
from models import Problem

class ReadInstance:
    def __init__(self, instance_name):
        self.instance_name = instance_name

    def read_instance(self)->Problem:
        problem = Problem()

        folder_directory = 'instances_txt/' + self.instance_name

        with open(folder_directory, 'r') as file:
            truck_capacity = int(file.readline().strip())  # Primera línea: Capacidad del camión
            n_nodes = int(file.readline().strip())  # Segunda línea: Número de nodos
            history_length = int(file.readline().strip())  # Tercera línea: Longitud del historial
            
            # Skip two lines
            file.readline()
            file.readline()
            # Leer los nodos (suponiendo que están en el formato esperado)
            nodes = []
            for _ in range(n_nodes):
                node_data = list(map(float, file.readline().strip().split()))
                nodes.append(node_data)

            # Skip two lines
            file.readline()
            file.readline()

            # Leer el histórico de demandas
            demand_history = []
            for _ in range(history_length):
                line_data = file.readline().strip().split()
                demand_history.append([float(x) if x.replace('.', '', 1).isdigit() else x for x in line_data])

        problem.truck_capacity = truck_capacity
        problem.n_nodes = n_nodes
        problem.feed_historical_data(demand_history)
        problem.feed_nodes(nodes)

        return problem


        
