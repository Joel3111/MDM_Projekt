from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

# Stellt eine Verbindung zu MongoDB her
client = MongoClient("mongodb+srv://joelegli:test@nutritionbase.rx1ko0e.mongodb.net/")
db = client["NutritionBase"]
collection = db["Nahrungsmittel"]

# Initialisiere den WebDriver
driver = webdriver.Chrome()

# Maximiere das Browserfenster
driver.maximize_window()

# URL der Seite
url = "https://naehrwertdaten.ch/de/search/#/food/340936"

# Gehe zur URL
driver.get(url)

# Warte, damit die Seite Zeit hat, Inhalte zu laden
time.sleep(5)

# Extrahiere den Namen des Nahrungsmittels
name_element = driver.find_element(By.CSS_SELECTOR, "label.food-content--header-title--label")
name_des_nahrungsmittels = name_element.text.strip()

# Kategorien in der Reihenfolge, wie sie erscheinen
kategorien = [
    "Kalorien",
    "Joule",
    "Fett_total",
    "Fettsäuren_gesättigt",
    "Fettsäuren_einfach_ungesättigt",
    "Fettsäuren_mehrfach_ungesättigt",
    "Cholesterin",
    "Kohlenhydrate_verfügbar",
    "Zucker",
    "Stärke",
    "Nahrungsfasern",
    "Protein",
    "Salz_NaCl",
    "Alkohol",
    "Wasser"
]

# Initialisiere ein Dictionary für die Nährwertinformationen
nahrwertinformationen = {"Name": name_des_nahrungsmittels}

# Extrahiere die Werte und ordne sie den Kategorien zu
for i, kategorie in enumerate(kategorien, start=1):
    try:
        xpath = f"(//tr[contains(@class, 'kb-row-1')])[{i}]/td[2]"
        wert_element = driver.find_element(By.XPATH, xpath)
        wert_text = wert_element.text.strip()
        wert = 0 if wert_text == "k.A." else float(wert_text.replace(',', '.'))
        nahrwertinformationen[kategorie] = wert
    except Exception as e:
        print(f"Es gab ein Problem beim Extrahieren des Werts für {kategorie}: {e}")
        nahrwertinformationen[kategorie] = 0

# Hier aktualisieren wir das Dokument, wenn es bereits existiert, basierend auf dem Namen
nahrwertinformationen_update = {"$set": nahrwertinformationen}
result = collection.update_one({"Name": nahrwertinformationen["Name"]}, nahrwertinformationen_update, upsert=True)

if result.matched_count:
    print("Dokument wurde aktualisiert.")
elif result.upserted_id:
    print(f"Neues Dokument wurde eingefügt mit der _id: {result.upserted_id}")

# Schließe den WebDriver
driver.quit()
