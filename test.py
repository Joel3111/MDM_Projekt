from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

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

try:
    # Warten, bis Elemente mit der Klasse 'ui-treetable-toggler ng-star-inserted' verfügbar sind
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-treetable-toggler"))
    )
    time.sleep(5)
    # Durch die gefundenen Elemente iterieren und das erste mit dem gewünschten style-Attribut anklicken
    for element in elements:
        style = element.get_attribute("style")
        if "visibility: visible" in style and "margin-left: 16px" in style:
            element.click()
            time.sleep(3)
            print("Gesuchtes erste Element wurde angeklickt.")
            break
    # Warten, bis Elemente mit der Klasse 'ui-treetable-toggler ng-star-inserted' verfügbar sind
    elements = driver.find_elements(By.CLASS_NAME, "ui-treetable-toggler")
    
    # Einen Zähler für passende Elemente einführen
    match_count = 0
    
    # Durch die gefundenen Elemente iterieren
    for element in elements:
        style = element.get_attribute("style")
        if "visibility: visible" in style and "margin-left: 16px" in style:
            match_count += 1
            if match_count == 2:  # Wenn das zweite passende Element gefunden wird
                element.click()
                print("Das zweite passende Element wurde angeklickt.")
                break

except Exception as e:
    print("Fehler beim Suchen oder Anklicken des Elements:", e)

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

print(nahrwertinformationen)

# Schließe den WebDriver
driver.quit()
