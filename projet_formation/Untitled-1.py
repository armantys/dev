# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima.model import ARIMA

# %%
df = pd.read_csv("output2.csv")

# %%
df

# %%
df.info()

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

# Vérifier les valeurs après le remplacement des mois par des chiffres
print(df['Mois'].unique())

df['Mois']=pd.to_datetime(df['Mois'], infer_datetime_format=True)
df
df.info()


# %%
df_grouped = df.groupby('Mois').agg({
    'Livrables conformes': 'sum',
    'Livrables dans la tolérance': 'sum',
    'Livrables non-conformes': 'sum'
}).reset_index()

df_grouped.set_index('Mois', inplace=True)
df_grouped = df_grouped.sort_index()
df_grouped

# %%
# Convertir la colonne 'Mois' au format 'YYYY-MM' (mois et année seulement)
df_grouped.index = pd.to_datetime(df_grouped.index)
df_grouped

# %%
df_grouped.isnull().sum()

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

fig, (ax1,ax2) = plt.subplots(2,1, figsize=(10,8))

#tracer l'ACF 
plot_acf(df_grouped['Livrables conformes'], lags=15, zero=True, ax=ax1)
ax1.set_title('ACF - Série de Livraisons conformes')

ax1.set_xlabel('Lag')
ax1.set_ylabel('Corrélation')
ax1.grid(True)

#ajuster les graduations sur l'axe x pour l'ACF
ax1.set_xticks(np.arange(0, 31, 1))

#tracer le PACF 
plot_pacf(df_grouped['Livrables conformes'], lags=15, zero=True, ax=ax2)
ax2.set_title('ACF - Série de Livraisons conformes')
ax2.set_xlabel('Lag')
ax2.set_ylabel('Corrélation Partielle')
ax2.grid(True)

#ajuster les graduations sur l'axe x pour le PACF
ax2.set_xticks(np.arange(0, 31, 1))

# Ajuster les subplots
plt.tight_layout()

plt.show()

# %%
#analyse de la stationnarité de la variable

from statsmodels.tsa.stattools import adfuller
from tabulate import tabulate

#Effectuer le test de Dickey-fuller augmenter
result = adfuller(df_grouped['Livrables conformes'])

#formater les résultats dans un tableau
table = [
    ['valeur de test', result[0]],
    ['P-valeur', result[1]],
    ['Conclusion', 'La sére est stationnaire' if result[1] < 0.05 else 'La série est non stationnaire']
]

#Afficher les résultats sous forme de tableau
print(tabulate(table, headers=['Métrique', 'Valeur'], tablefmt='github'))

# %%
difference = df_grouped['Livrables conformes'].diff().diff().dropna()

plt.figure(figsize=(10, 6))
plt.plot(difference, color='blue')
plt.title('Evolution des Livrables conformes')
plt.xlabel('Date')
plt.ylabel('difference')
plt.grid()

# Rotation des labels de l'axe X
plt.xticks(rotation=90)

plt.tight_layout()  # Ajuste automatiquement les éléments pour éviter les chevauchements
plt.show()

# %%
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, (ax1,ax2) = plt.subplots(2,1, figsize=(10,8))

#tracer l'ACF 
plot_acf(difference, lags=15, zero=True, ax=ax1)
ax1.set_title('ACF - Série de Livraisons conformes')

ax1.set_xlabel('Lag')
ax1.set_ylabel('Corrélation')
ax1.grid(True)

#ajuster les graduations sur l'axe x pour l'ACF
ax1.set_xticks(np.arange(0, 16, 1))

#tracer le PACF 
plot_pacf(difference, lags=15, zero=True, ax=ax2)
ax2.set_title('ACF - Série de Livraisons conformes')
ax2.set_xlabel('Lag')
ax2.set_ylabel('Corrélation Partielle')
ax2.grid(True)

#ajuster les graduations sur l'axe x pour le PACF
ax2.set_xticks(np.arange(0, 16, 1))

# Ajuster les subplots
plt.tight_layout()

plt.show()

# %%
#analyse de la stationnarité de la variable

from statsmodels.tsa.stattools import adfuller
from tabulate import tabulate

#Effectuer le test de Dickey-fuller augmenter
result = adfuller(difference)

#formater les résultats dans un tableau
table = [
    ['valeur de test', result[0]],
    ['P-valeur', result[1]],
    ['Conclusion', 'La sére est stationnaire' if result[1] < 0.05 else 'La série est non stationnaire']
]

#Afficher les résultats sous forme de tableau
print(tabulate(table, headers=['Métrique', 'Valeur'], tablefmt='github'))

# %%
p = 1
q = 1
d = 1,3

# %%
train_data = difference[:-15]
test_data = difference[-15:]

# %%
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(train_data, order=(1,1,1))

model_fit = model.fit()

print(model_fit.summary())

# %%
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
import seaborn as sns

#Calculer les résidus
residuals = model_fit.resid

plt.figure(figsize=(10,5))
plot_acf(residuals, lags=15, zero=False)
plt.title("Autocorrelation des residus")
plt.show()

plt.figure(figsize=(10,5))
plot_pacf(residuals, lags=8, zero=False)
plt.title("Partiel Autocorrelation des residus")
plt.show()


# %%
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

#prediction sur l'ensemble d'entrainement
train_prediction = model_fit.predict(start=train_data.index[0], end=train_data.index[-1])

#prediction sur l'ensemble de test
test_prediction = model_fit.predict(start=test_data.index[0], end=test_data.index[-1])

#prediction sur l'ensemble d'entrainement
train_prediction = model_fit.predict(start=train_data.index[0], end=train_data.index[-1])

#prediction sur l'ensemble de test
test_prediction = model_fit.predict(start=test_data.index[0], end=test_data.index[-1])

print(train_prediction.index.dtype)
print(test_prediction.index.dtype)

# Conversion explicite en séries Pandas
train_prediction = pd.Series(train_prediction, index=train_data.index)
test_prediction = pd.Series(test_prediction, index=test_data.index)

# Tracer les courbes
plt.figure(figsize=(10, 6))
plt.plot(train_data.index, train_data.values, label="Ensemble d'entraînement", color="blue")
plt.plot(test_data.index, test_data.values, label="Ensemble de test (réel)", color="blue", linestyle="--")
plt.plot(train_prediction.index, train_prediction, label="Prédiction (Entraînement)", color="red")
plt.plot(test_prediction.index, test_prediction, label="Prédiction (Test)", color="green")

# Définir les limites des axes pour une continuité visuelle
plt.xlim(train_data.index[0], test_data.index[-1])
plt.ylim(min(train_data.min(), test_data.min()), max(train_data.max(), test_data.max()))

# Ajouter des labels et une légende
plt.xlabel("Date")
plt.ylabel("Livrables conformes")
plt.title("Comparaison des données réelles et prédites")
plt.legend()
plt.show()

# %%
#Mesure de performence sur l'ensemble d'entrainement
train_mae = mean_absolute_error(train_data, train_prediction)
train_mse = mean_squared_error(train_data, train_prediction)
train_rmse = np.sqrt(train_mse)
train_r2 = r2_score(train_data, train_prediction)

#Mesure de performance sur l'ensemble de test
test_mae = mean_absolute_error(test_data, test_prediction)
test_mse = mean_squared_error(test_data, test_prediction)
test_rmse = np.sqrt(test_mse)
test_r2 = r2_score(test_data, test_prediction)

#Créer un DataFrame pour afficher les mesures de performance
performance_df = pd.DataFrame({
    'Métrique' : ['MAE', 'MSE', 'RMSE', 'R2'],
    'Ensemble d\'entrainement' : [train_mae, train_mse, train_rmse, train_r2],
    'Ensemble de test' : [test_mae, test_mse, test_rmse, test_r2]
})

print(performance_df)


# %%
import pmdarima as pm

#Séparer les données en ensemble d'entrainement et ensemble de test
train_data = df['Livrables conformes'][:-15]
test_data = df['Livrables conformes'][-15:]

#model auto_arima pour trouver le meilleur modèle ARIMA
model = pm.auto_arima(train_data)

print(model.summary())

# %%
#Ajuster le modèle aux données
model.fit(train_data)

#obtenir les résidus du modeèle
residuals = model.resid()

plt.figure(figsize=(10,5))
plot_acf(residuals, lags=15)
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title("ACF des residus")
plt.show()

plt.figure(figsize=(10,5))
plot_pacf(residuals, lags=8)
plt.xlabel('Lag')
plt.ylabel('Patial Autocorrelation')
plt.title("PACF des residus")
plt.show()

# %%
# Faire des prédictions sur l'ensemble d'entrainement
train_pred, train_confint = model.predict_in_sample(return_conf_int=True)

#Faire des prédiction sur l'ensemble de test
n_periods = len(test_data)
predicted, confint = model.predict(n_periods=n_periods, return_conf_int=True)

#Concaténer les prédictions pour l'ensemble d'entrainement et de test
all_prediction = pd.concat([pd.Series(train_pred,index=train_data.index),
                           pd.Series(predicted, index=test_data.index)],
                           axis=0)


plt.figure(figsize=(10, 6))
plt.plot(train_data.index, train_data.values, label="Ensemble d'entraînement", color="blue")
plt.plot(test_data.index, test_data.values, label="Ensemble de test (réel)", color="green", linestyle="--")
plt.plot(train_prediction.index, train_prediction, label="Prédiction (Entraînement)", color="red")
plt.plot(test_prediction.index, test_prediction, label="Prédiction (Test)", color="orange")

plt.xlabel("Date")
plt.ylabel("Livrables conformes")
plt.title("Comparaison des données réelles et prédites")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%


df.set_index('Mois', inplace=True)
print(df.index)

df_grouped = df.groupby('Mois').sum()  # Assurez-vous que l'agrégation se fait bien

print(df_grouped.head())
print(df_grouped.index)

print("Train Data:", train_data.index.min(), "-", train_data.index.max())
print("Test Data:", test_data.index.min(), "-", test_data.index.max())
print("Train Predictions:", train_prediction.index.min(), "-", train_prediction.index.max())
print("Test Predictions:", test_prediction.index.min(), "-", test_prediction.index.max())

# %% [markdown]
# 

# %%
print("Train Data:")
print(train_data.head())
print("Test Data:")
print(test_data.head())

# %%
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Ensure the correct indices are used for predictions
train_start = train_data.index[0]
train_end = train_data.index[-1]
test_start = test_data.index[0]
test_end = test_data.index[-1]

# Prédictions sur l'ensemble d'entraînement
train_prediction = model_fit.predict(start=train_start, end=train_end)

# Prédictions sur l'ensemble de test
test_prediction = model_fit.predict(start=test_start, end=test_end)

# Assign predictions to the appropriate indices
train_prediction = pd.Series(train_prediction, index=train_data.index)
test_prediction = pd.Series(test_prediction, index=test_data.index)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(train_data, label="Données d'entraînement", color="blue")
plt.plot(test_data, label="Données de test (réelles)", color="green", linestyle="--")
plt.plot(train_prediction, label="Prédiction (entraînement)", color="red")
plt.plot(test_prediction, label="Prédiction (test)", color="orange")

plt.xlabel("Date")
plt.ylabel("Valeur")
plt.title("Comparaison des données réelles et prédites")
plt.legend()
plt.show()

# %%
print("Start date for training:", train_data.index[0])
print("End date for training:", train_data.index[-1])
print("Start date for testing:", test_data.index[0])
print("End date for testing:", test_data.index[-1])


