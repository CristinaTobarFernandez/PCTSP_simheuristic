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
        self.client_factors = np.random.uniform(0.8, 1.2, self.n_nodes)  # Factores aleatorios por cliente

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

            # Ajuste de demanda basado en el día de la semana
            day_type_factor = 1.0
            if day_of_week in [5, 6]:  # Fin de semana
                day_type_factor = 1.2  # Aumentar demanda en fines de semana
            
            weather_factor = 1.0
            if weather_condition == 'Rainy':
                weather_factor = 0.8  # Disminuye demanda en condiciones de lluvia

            # Ajuste de demanda basado en la temperatura humedad y velocidad del viento
            factor_temperature = 1.0
            if temperature > 30:
                factor_temperature = 1.2 # Aumenta demanda en condiciones de alta temperatura

            factor_humidity = 1.0
            if humidity > 70:
                factor_humidity = 0.8 # Disminuye demanda en condiciones de alta humedad

            factor_wind_speed = 1.0
            if wind_speed > 15:
                factor_wind_speed = 0.8 # Disminuye demanda en condiciones de alta velocidad del viento
            
            noise = np.random.normal(0, 0.1 * demands)
            adjusted_demands = (demands * self.client_factors * day_type_factor * weather_factor * factor_temperature * 
                               factor_humidity * factor_wind_speed) + noise
            adjusted_demands = np.clip(adjusted_demands, 0, None)  # Aseguramos que no haya valores negativos

            sample = {
                'hour_of_day': hour_of_day,
                'day_of_week': day_of_week,
                'weather_condition': weather_condition,
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed
            }

            # Añadir demandas generadas
            sample.update({f'demand_node_{i}': adjusted_demands[i] for i in range(self.n_nodes)})
            history.append(sample)

        # Convertir a DataFrame
        history_df = pd.DataFrame(history)
        return history_df