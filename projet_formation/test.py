# Importation des bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.tsa.stattools import adfuller
import pmdarima as pm

# Chargement des données
df = pd.read_csv("output2.csv")

# Prétraitement des données
df['Mois'] = df['Mois'].str.replace(r'\bJui\b', 'Juin', regex=True)

# Dictionnaire pour remplacer les noms de mois par leurs équivalents numériques
months_translation = {
    "Jan": "01", "Fev": "02", "Mar": "03", "Avr": "04", "Mai": "05", "Juin": "06",
    "Juil": "07", "Aou": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}
df['Mois'] = df['Mois'].str.replace(
    r'\b(' + '|'.join(months_translation.keys()) + r')\b',
    lambda x: months_translation[x.group(0)],
    regex=True
)

# Conversion en type datetime
df['Mois'] = pd.to_datetime(df['Mois'], errors="coerce", infer_datetime_format=True)
if df['Mois'].isnull().sum() > 0:
    raise ValueError("Certaines dates n'ont pas pu être converties correctement. Vérifiez les données.")
df.set_index('Mois', inplace=True)

# Agrégation mensuelle avec une fréquence explicite
df_grouped = df.groupby('Mois').agg({
    'Livrables conformes': 'sum',
    'Livrables dans la tolérance': 'sum',
    'Livrables non-conformes': 'sum'
}).sort_index().asfreq('MS')

# Vérification de la stationnarité avec le test de Dickey-Fuller
result = adfuller(df_grouped['Livrables conformes'].dropna())
print(f"P-valeur : {result[1]}")
if result[1] < 0.05:
    print("La série est stationnaire.")
    diff_data = df_grouped['Livrables conformes']
else:
    print("La série est non stationnaire. Différenciation requise.")
    diff_data = df_grouped['Livrables conformes'].diff().dropna()

# Vérification que les données différenciées ne sont pas vides
if diff_data.empty:
    raise ValueError("La série différenciée est vide. Vérifiez vos données d'entrée.")

# Séparation des données en ensemble d'entraînement et de test
train_data = diff_data[:-15]
test_data = diff_data[-15:]

# Vérification des ensembles d'entraînement et de test
if train_data.empty or test_data.empty:
    raise ValueError("Les ensembles d'entraînement ou de test sont vides. Vérifiez la séparation des données.")

# Recherche des meilleurs paramètres ARIMA avec auto_arima
model_auto = pm.auto_arima(
    train_data,
    seasonal=False,  # Activer la saisonnalité
    trace=True,
    suppress_warnings=True,
    error_action="ignore"
)
print(model_auto.summary())

# Création et ajustement du modèle ARIMA avec les paramètres optimaux
best_order = model_auto.order
best_seasonal_order = model_auto.seasonal_order
model = ARIMA(train_data, order=best_order, seasonal_order=best_seasonal_order)
model_fit = model.fit()

# Prédictions sur l'ensemble d'entraînement et de test
train_prediction = model_fit.predict(start=train_data.index[0], end=train_data.index[-1])
test_prediction = model_fit.predict(start=test_data.index[0], end=test_data.index[-1])

# Rétablir les valeurs originales (si différenciées)
train_prediction = train_prediction.cumsum() + df_grouped['Livrables conformes'].iloc[0]
test_prediction = test_prediction.cumsum() + df_grouped['Livrables conformes'].iloc[len(train_data)]

# Alignement des indices
train_prediction.index = train_data.index
test_prediction.index = test_data.index

# Calcul des métriques de performance
train_mae = mean_absolute_error(train_data, train_prediction)
train_mse = mean_squared_error(train_data, train_prediction)
train_rmse = np.sqrt(train_mse)
train_r2 = r2_score(train_data, train_prediction)

test_mae = mean_absolute_error(test_data, test_prediction)
test_mse = mean_squared_error(test_data, test_prediction)
test_rmse = np.sqrt(test_mse)
test_r2 = r2_score(test_data, test_prediction)

# Affichage des métriques
print(f"Ensemble d'entraînement: MAE={train_mae:.2f}, RMSE={train_rmse:.2f}, R2={train_r2:.2f}")
print(f"Ensemble de test: MAE={test_mae:.2f}, RMSE={test_rmse:.2f}, R2={test_r2:.2f}")

# Visualisation des résultats
plt.figure(figsize=(10, 6))
plt.plot(df_grouped['Livrables conformes'], label="Données réelles", color="blue")
plt.plot(train_prediction, label="Prédiction (entraînement)", color="red")
plt.plot(test_prediction, label="Prédiction (test)", color="orange", linestyle="--")

plt.xlabel("Date")
plt.ylabel("Livrables conformes")
plt.title("Comparaison des données réelles et prédites avec SARIMA")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
