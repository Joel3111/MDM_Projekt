import os
from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Baue den Pfad zur Modell-Datei
base_dir = os.path.abspath(os.path.dirname(__file__))  # Verzeichnis von app.py
model_path = os.path.join(base_dir, '..', 'kalorien_model.joblib')  # Pfad zur Modell-Datei im übergeordneten Verzeichnis

model = joblib.load(model_path)  # Lade das Modell

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Eingabewerte extrahieren
        feature_values = [float(x) for x in request.form.values()]
        
        # Einen DataFrame mit den entsprechenden Spaltennamen erstellen
        features_df = pd.DataFrame([feature_values], columns=['Fett_total', 'Kohlenhydrate_verfügbar', 'Protein'])
        
        # Vorhersage mit dem Modell machen
        prediction = model.predict(features_df)[0]
        
        # Vorhersageergebnis zurückgeben
        return render_template('index.html', prediction_text=f'Geschätzte Kalorien: {prediction:.2f}')
    except Exception as e:
        return render_template('index.html', prediction_text=f'Fehler: {e}')


if __name__ == "__main__":
    app.run(debug=True)
