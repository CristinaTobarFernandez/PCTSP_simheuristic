from utils.ml_enum import MachineLearningEnum
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

class MLModels:
    def __init__(self):
        pass
    
    @staticmethod
    def predict(X_train, y_train, X_test, model: MachineLearningEnum):
        transformations = ColumnTransformer(
            [('encoder', OneHotEncoder(handle_unknown='ignore'), [0, 1, 2])]
        )

        X_train = transformations.fit_transform(X_train)
        X_test = transformations.transform(X_test)
        
        if model == MachineLearningEnum.LINEAR_REGRESSION:
            model = LinearRegression()
        elif model == MachineLearningEnum.RIDGE:
            model = Ridge()
        elif model == MachineLearningEnum.LASSO:
            model = Lasso()
        elif model == MachineLearningEnum.SVR:
            model = SVR()
        elif model == MachineLearningEnum.NEURAL_NETWORK:
            model = MLPRegressor()
        elif model == MachineLearningEnum.XGBOOST:
            model = XGBRegressor()

        model.fit(X_train, y_train)
        return model.predict(X_test)

    @staticmethod
    def generate_knn_scenarios(X_train, y_train, X_test, n_scenarios: int):
        transformations = ColumnTransformer(
            [('encoder', OneHotEncoder(handle_unknown='ignore'), [0, 1, 2])]
        )

        X_train = transformations.fit_transform(X_train)
        X_test = transformations.transform(X_test)
        
        knn = KNeighborsRegressor(n_neighbors=n_scenarios)
        knn.fit(X_train, y_train)
        return knn.predict(X_test)

