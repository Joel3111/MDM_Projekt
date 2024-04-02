import joblib
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# MongoDB Verbindung aufbauen
client = MongoClient("mongodb+srv://joelegli:test@nutritionbase.rx1ko0e.mongodb.net/")
db = client["NutritionBase"]
data_collection = db["Nahrungsmittel"]

# Daten extrahieren
data = list(data_collection.find())

# Daten in ein Pandas DataFrame umwandeln
df = pd.DataFrame(data)

# Hilfsfunktion, um Werte aus MongoDB-Dokumenten zu extrahieren und in numerische Werte umzuwandeln
def extract_value(doc, key):
    if key in doc and isinstance(doc[key], dict):
        if '$numberInt' in doc[key]:
            return int(doc[key]['$numberInt'])
        elif '$numberDouble' in doc[key]:
            return float(doc[key]['$numberDouble'])
    return 0

# Extrahiere und konvertiere die benötigten Spalten
df['Fett_total'] = df.apply(lambda row: extract_value(row, 'Fett_total'), axis=1)
df['Kohlenhydrate_verfügbar'] = df.apply(lambda row: extract_value(row, 'Kohlenhydrate_verfügbar'), axis=1)
df['Protein'] = df.apply(lambda row: extract_value(row, 'Protein'), axis=1)
df['Kalorien'] = df.apply(lambda row: extract_value(row, 'Kalorien'), axis=1)

# Zielvariable 'Kalorien' auswählen
y = df['Kalorien']

# Features auswählen: Fett_total, Kohlenhydrate_verfügbar, Protein
X = df[['Fett_total', 'Kohlenhydrate_verfügbar', 'Protein']]

# Daten aufteilen (z.B. 80% Training, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modell initialisieren
model = LinearRegression()

# Modell mit Trainingsdaten trainieren
model.fit(X_train, y_train)

# Vorhersagen auf dem Testset machen
predictions = model.predict(X_test)

# Modellleistung bewerten
mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Mean Squared Error (MSE): {mse}")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"R^2 Score: {r2}")

# Modell speichern
joblib.dump(model, 'kalorien_model.joblib')
print("Modell wurde gespeichert.")
