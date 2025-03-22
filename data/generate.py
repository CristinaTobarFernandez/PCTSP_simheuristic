from PCTSPInstanceGenerator import PCTSPInstanceGenerator
import os
import numpy as np
a = 50
b = 150
mu = 100
sigma = 15
lamb = 40
for distribution in ['uniform', 'normal', 'poisson']:
    for n_nodes in [100, 200, 300, 400, 500]:
        for history_length in [1000, 2000, 3000, 4000, 5000]:
            # Ejemplo de uso
            instance = PCTSPInstanceGenerator(n_nodes=n_nodes, distribution=distribution, demand_params={'a': a, 'b': b, 'mu': mu, 'sigma': sigma, 'lambda': lamb}, seed=42)

            # Generar histórico de demandas con 50 muestras
            historical_data = instance.generate_demand_history(history_length)
            if distribution == 'uniform':
                name = f'u_{a}_{b}_{n_nodes}_{history_length}'
            elif distribution == 'normal':
                name = f'n_{mu}_{sigma}_{n_nodes}_{history_length}'
            elif distribution == 'poisson':
                name = f'p_{lamb}_{n_nodes}_{history_length}'
            
            truck_capacity = int(np.mean(instance.nodes.values) * n_nodes)
            folder = f'instances/{name}'
            os.makedirs(folder, exist_ok=True)
            instance.nodes.to_csv(f'{folder}/nodes.csv', index=False)
            historical_data.to_csv(f'{folder}/historical_data.csv', index=False)
            with open(f'{folder}/truck_capacity.csv', 'w') as capacity_file:
                capacity_file.write('truck_capacity\n')
                capacity_file.write(f'{truck_capacity}\n')


            folder = f'instances_txt'
            os.makedirs(folder, exist_ok=True)
            # Crear archivo de texto con el formato especificado
            with open(f'{folder}/{name}.txt', 'w') as txt_file:
                txt_file.write(f'{truck_capacity}\n')
                txt_file.write(f'{n_nodes}\n')
                txt_file.write(f'{history_length}\n')

                txt_file.write('\n\n')
                # Escribir los nodos separados por espacios
                for node in instance.nodes.values:
                    txt_file.write(' '.join(map(str, node)) + '\n')
                txt_file.write('\n\n')
                # Escribir el histórico de demandas
                txt_file.write(historical_data.to_string(index=False, header=False))