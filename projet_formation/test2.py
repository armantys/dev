import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Étape 1 : Charger les données
file_path = "output2.csv"  # Remplacez par le chemin correct vers votre fichier
df = pd.read_csv(file_path)

# Nettoyage des mois
months_translation = {
    "Jan": "01", "Fev": "02", "Mar": "03", "Avr": "04", "Mai": "05", "Juin": "06",
    "Juil": "07", "Aou": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
}
df['Mois'] = df['Mois'].replace(months_translation, regex=True)
df['Mois'] = pd.to_datetime(df['Mois'], format='%m %Y', errors='coerce')

# Agréger les données par mois
df_grouped = df.groupby('Mois').sum()

# Convertir la colonne 'Mois' en format datetime et définir comme index
df['Mois'] = pd.to_datetime(df['Mois'])
df.set_index('Mois', inplace=True)

# Vérification des données
print(df.head())

# Sélection de la série à prédire (par exemple, 'Livrables conformes')
serie = df['Livrables conformes']

# Étape 2 : Visualisation des données
plt.figure(figsize=(12, 6))
plt.plot(serie, label="Livrables conformes")
plt.title("Série temporelle : Livrables conformes")
plt.xlabel("Date")
plt.ylabel("Livrables conformes")
plt.legend()
plt.show()

# Étape 3 : Découper les données en train et test
train = serie[:int(0.8 * len(serie))]
test = serie[int(0.8 * len(serie)):]

# Étape 4 : Construction et ajustement du modèle ARIMA
model = ARIMA(train, order=(5, 1, 0))  # Modifiez (p, d, q) si nécessaire
model_fit = model.fit()

# Résumé du modèle
print(model_fit.summary())

# Étape 5 : Prévision
forecast = model_fit.forecast(steps=len(test))  # Prévisions pour la période de test

# Étape 6 : Évaluation des performances
mae = mean_absolute_error(test, forecast)
rmse = np.sqrt(mean_squared_error(test, forecast))
print(f"MAE : {mae}")
print(f"RMSE : {rmse}")

# Étape 7 : Visualisation des résultats
plt.figure(figsize=(12, 6))
plt.plot(train, label="Train")
plt.plot(test, label="Test", color="orange")
plt.plot(test.index, forecast, label="Prévisions", color="green")
plt.title("Modèle ARIMA - Prévisions")
plt.xlabel("Date")
plt.ylabel("Livrables conformes")
plt.legend()
plt.show()

# Étape 8 : Prévision future
future_steps = 12  # Par exemple, 12 mois à prévoir
future_forecast = model_fit.forecast(steps=future_steps)

# Création d'un DataFrame pour les prévisions futures
future_dates = pd.date_range(start=serie.index[-1], periods=future_steps + 1, freq='M')[1:]
future_df = pd.DataFrame({'Mois': future_dates, 'Prévisions': future_forecast})

print("Prévisions futures :")
print(future_df)

# Visualisation des prévisions futures
plt.figure(figsize=(12, 6))
plt.plot(serie, label="Données réelles")
plt.plot(future_df['Mois'], future_df['Prévisions'], label="Prévisions futures", color="red")
plt.title("Prévisions futures avec ARIMA")
plt.xlabel("Date")
plt.ylabel("Livrables conformes")
plt.legend()
plt.show()
