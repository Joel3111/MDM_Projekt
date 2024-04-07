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
    # Definiere einen leeren Zustand für input_values
    input_values = {'protein': '', 'fett': '', 'kohlenhydrate': '', 'nahrungsfasern': ''}
    return render_template('index.html', input_values=input_values)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Eingabewerte extrahieren und in der richtigen Reihenfolge anordnen
        protein = request.form['protein']
        fett = request.form['fett']
        kohlenhydrate = request.form['kohlenhydrate']
        nahrungsfasern = request.form['nahrungsfasern']
        feature_values = [float(fett), float(kohlenhydrate), float(protein), float(nahrungsfasern)]
        
        # Einen DataFrame mit den entsprechenden Spaltennamen erstellen
        features_df = pd.DataFrame([feature_values], columns=['Fett_total', 'Kohlenhydrate_verfügbar', 'Protein', 'Nahrungsfasern'])
        
        # Vorhersage mit dem Modell machen
        prediction = model.predict(features_df)[0]
        
        # Vorhersageergebnis und eingegebene Werte zurückgeben
        input_values = {'protein': protein, 'fett': fett, 'kohlenhydrate': kohlenhydrate, 'nahrungsfasern': nahrungsfasern}
        return render_template('index.html', prediction_text=f'Geschätzte Kalorien: {prediction:.2f}', input_values=input_values)
    except Exception as e:
        input_values = {'protein': '', 'fett': '', 'kohlenhydrate': '', 'nahrungsfasern': ''}
        return render_template('index.html', prediction_text=f'Fehler: {e}', input_values=input_values)

if __name__ == "__main__":
    app.run(debug=True)
