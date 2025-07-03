# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate

import warnings
warnings.filterwarnings('ignore')

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# %%
df = pd.read_csv("output2.csv")

# %%
# Remplacer "Jui" par "Juin" dans toute la colonne 'Mois'
df['Mois'] = df['Mois'].str.replace(r'\bJui\b', 'Juin', regex=True)

# Dictionnaire de traduction des mois
months_translation = {
    "Jan": "01", "Fev": "02", "Mar": "03", "Avr": "04", "Mai": "05", "Juin": "06",
    "Juil": "07", "Aou": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}

# Remplacer chaque mois par son équivalent numérique
df['Mois'] = df['Mois'].str.replace(r'\b(' + '|'.join(months_translation.keys()) + r')\b',
                                    lambda x: months_translation[x.group(0)], regex=True)

# Convertir la colonne 'Mois' au format 'YYYY-MM' (mois et année seulement)
df['Mois'] = pd.to_datetime(df['Mois'], infer_datetime_format=True)
df.set_index('Mois', inplace=True)

# %%
df_grouped = df.groupby('Mois').agg({
    'Livrables conformes': 'sum',
    'Livrables dans la tolérance': 'sum',
    'Livrables non-conformes': 'sum'
}).reset_index()

df_grouped.set_index('Mois', inplace=True)
df_grouped = df_grouped.sort_index()

# %%
# Convertir la colonne 'Mois' au format 'YYYY-MM' (mois et année seulement)
df_grouped.index = pd.to_datetime(df_grouped.index)

# %%
plt.figure(figsize=(10, 6))
plt.plot(df_grouped.index, df_grouped['Livrables conformes'], color='blue')
plt.title('Evolution des Livrables conformes')
plt.xlabel('Date')
plt.ylabel('Nombre de Livrables conformes')
plt.grid()

# Rotation des labels de l'axe X
plt.xticks(rotation=90)

plt.tight_layout()  # Ajuste automatiquement les éléments pour éviter les chevauchements
plt.show()

# %%
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Tracer l'ACF
plot_acf(df_grouped['Livrables conformes'], lags=15, zero=True, ax=ax1)
ax1.set_title('ACF - Série de Livraisons conformes')
ax1.set_xlabel('Lag')
ax1.set_ylabel('Corrélation')
ax1.grid(True)

# Tracer le PACF
plot_pacf(df_grouped['Livrables conformes'], lags=15, zero=True, ax=ax2)
ax2.set_title('PACF - Série de Livraisons conformes')
ax2.set_xlabel('Lag')
ax2.set_ylabel('Corrélation Partielle')
ax2.grid(True)

# Ajuster les subplots
plt.tight_layout()
plt.show()

# %%
# Analyse de la stationnarité de la variable
result = adfuller(df_grouped['Livrables conformes'])

# Formater les résultats dans un tableau
table = [
    ['valeur de test', result[0]],
    ['P-valeur', result[1]],
    ['Conclusion', 'La série est stationnaire' if result[1] < 0.05 else 'La série est non stationnaire']
]

# Afficher les résultats sous forme de tableau
print(tabulate(table, headers=['Métrique', 'Valeur'], tablefmt='github'))

# %%
# Différenciation des données pour les rendre stationnaires
difference = df_grouped['Livrables conformes'].diff().dropna()

plt.figure(figsize=(10, 6))
plt.plot(difference, color='blue')
plt.title('Evolution des Livrables conformes (différenciés)')
plt.xlabel('Date')
plt.ylabel('Différence')
plt.grid()

# Rotation des labels de l'axe X
plt.xticks(rotation=90)

plt.tight_layout()  # Ajuste automatiquement les éléments pour éviter les chevauchements
plt.show()

# %%
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Tracer l'ACF
plot_acf(difference, lags=15, zero=True, ax=ax1)
ax1.set_title('ACF - Série de Livraisons conformes (différenciés)')
ax1.set_xlabel('Lag')
ax1.set_ylabel('Corrélation')
ax1.grid(True)

# Tracer le PACF
plot_pacf(difference, lags=15, zero=True, ax=ax2)
ax2.set_title('PACF - Série de Livraisons conformes (différenciés)')
ax2.set_xlabel('Lag')
ax2.set_ylabel('Corrélation Partielle')
ax2.grid(True)

# Ajuster les subplots
plt.tight_layout()
plt.show()

# %%
# Analyse de la stationnarité de la variable différenciée
result = adfuller(difference)

# Formater les résultats dans un tableau
table = [
    ['valeur de test', result[0]],
    ['P-valeur', result[1]],
    ['Conclusion', 'La série est stationnaire' if result[1] < 0.05 else 'La série est non stationnaire']
]

# Afficher les résultats sous forme de tableau
print(tabulate(table, headers=['Métrique', 'Valeur'], tablefmt='github'))

# %%
# Séparer les données en ensemble d'entraînement et ensemble de test
train_data = df_grouped['Livrables conformes'][:-15]
test_data = df_grouped['Livrables conformes'][-15:]

# %%
# Utiliser pmdarima pour trouver le meilleur modèle ARIMA
model = pm.auto_arima(train_data, seasonal=False, stepwise=True, suppress_warnings=True)
print(model.summary())

# %%
# Ajuster le modèle aux données d'entraînement
model.fit(train_data)

# Obtenir les résidus du modèle
residuals = model.resid()

plt.figure(figsize=(10, 5))
plot_acf(residuals, lags=15)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title("ACF des résidus")
plt.show()

plt.figure(figsize=(10, 5))
plot_pacf(residuals, lags=8)
plt.xlabel('Lag')
plt.ylabel('Partial Autocorrelation')
plt.title("PACF des résidus")
plt.show()

# %%
# Faire des prédictions sur l'ensemble d'entraînement
train_pred = model.predict_in_sample()

# Faire des prédictions sur l'ensemble de test
n_periods = len(test_data)
predicted = model.predict(n_periods=n_periods)

# Concaténer les prédictions pour l'ensemble d'entraînement et de test
all_prediction = pd.concat([pd.Series(train_pred, index=train_data.index),
                            pd.Series(predicted, index=test_data.index)],
                           axis=0)

plt.figure(figsize=(10, 6))
plt.plot(train_data.index, train_data.values, label="Ensemble d'entraînement", color="blue")
plt.plot(test_data.index, test_data.values, label="Ensemble de test (réel)", color="green", linestyle="--")
plt.plot(train_pred.index, train_pred, label="Prédiction (Entraînement)", color="red")
plt.plot(predicted.index, predicted, label="Prédiction (Test)", color="orange")

plt.xlabel("Date")
plt.ylabel("Livrables conformes")
plt.title("Comparaison des données réelles et prédites")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# Mesure de performance sur l'ensemble d'entraînement
train_mae = mean_absolute_error(train_data, train_pred)
train_mse = mean_squared_error(train_data, train_pred)
train_rmse = np.sqrt(train_mse)
train_r2 = r2_score(train_data, train_pred)

# Mesure de performance sur l'ensemble de test
test_mae = mean_absolute_error(test_data, predicted)
test_mse = mean_squared_error(test_data, predicted)
test_rmse = np.sqrt(test_mse)
test_r2 = r2_score(test_data, predicted)

# Créer un DataFrame pour afficher les mesures de performance
performance_df = pd.DataFrame({
    'Métrique': ['MAE', 'MSE', 'RMSE', 'R2'],
    'Ensemble d\'entraînement': [train_mae, train_mse, train_rmse, train_r2],
    'Ensemble de test': [test_mae, test_mse, test_rmse, test_r2]
})

print(performance_df)
