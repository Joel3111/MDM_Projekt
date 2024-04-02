from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialisiere den WebDriver
driver = webdriver.Chrome()

# Maximiere das Browserfenster
driver.maximize_window()

# URL der Seite
url = "https://naehrwertdaten.ch/de/search/#/food/340936"

# Gehe zur URL
driver.get(url)

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
finally:

    # Wichtig: Browser schließen, wenn nicht mehr benötigt
    driver.close()
