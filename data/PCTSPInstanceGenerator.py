import numpy as np
import pandas as pd
import random
from scipy.stats import poisson, norm

class PCTSPInstanceGenerator:
    def __init__(self, n_nodes, distribution='uniform', demand_params=None, seed=None):
        self.n_nodes = n_nodes
        self.distribution = distribution
        self.demand_params = demand_params if demand_params else {}
        self.seed = seed
        self.nodes = self.generate_nodes()

    def generate_nodes(self):
        if self.seed is not None:
            np.random.seed(self.seed)
            random.seed(self.seed)

        nodes = pd.DataFrame({
            'node_id': range(self.n_nodes),
            'x': np.random.randint(0, 201, self.n_nodes),
            'y': np.random.randint(0, 51, self.n_nodes)
        })
        return nodes

    def generate_demand(self):
        if self.distribution == 'uniform':
            a, b = self.demand_params.get('a', 0), self.demand_params.get('b', 100)
            return np.random.uniform(a, b, self.n_nodes)

        elif self.distribution == 'normal':
            mu, sigma = self.demand_params.get('mu', 50), self.demand_params.get('sigma', 10)
            demands = np.random.normal(mu, sigma, self.n_nodes)
            return np.clip(demands, 0, None)  # Aseguramos que no haya valores negativos

        elif self.distribution == 'poisson':
            lam = self.demand_params.get('lambda', 30)
            return poisson.rvs(lam, size=self.n_nodes)

        else:
            raise ValueError('Distribución no soportada')

    def generate_demand_history(self, n_samples):
        history = []
        for _ in range(n_samples):
            demands = self.generate_demand()
            demands = demands.astype(int)

            # Generar covariables ficticias
            hour_of_day = random.randint(0, 23)  # Hora del día
            day_of_week = random.randint(0, 6)  # Día de la semana (0 = Lunes, 6 = Domingo)
            weather_condition = random.choice(['Sunny', 'Rainy', 'Cloudy'])  # Clima ficticio
            temperature = np.random.uniform(0, 40)  # Temperatura en grados Celsius
            humidity = np.random.uniform(0, 100)  # Humedad en porcentaje
            wind_speed = np.random.uniform(0, 20)  # Velocidad del viento en m/s

            sample = {
                'hour_of_day': hour_of_day,
                'day_of_week': day_of_week,
                'weather_condition': weather_condition,
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed
            }

            # Añadir demandas generadas
            sample.update({f'demand_node_{i}': demands[i] for i in range(self.n_nodes)})
            history.append(sample)

        # Convertir a DataFrame
        history_df = pd.DataFrame(history)
        return history_df