from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time

# Starte den Chrome Browser
driver = webdriver.Chrome()

# Maximiere das Browserfenster, um sicherzustellen, dass alle Elemente sichtbar sind
driver.maximize_window()


# Gehe zur gewünschten Webseite
driver.get("https://naehrwertdaten.ch/de/search/#/food/340302")

# Warte einen Moment, damit die Seite vollständig geladen wird (anpassen nach Bedarf)
time.sleep(5)  # 5 Sekunden warten; für dynamische Inhalte kann WebDriverWait bevorzugt werden

# Annahme: 'driver' ist bereits definiert und zur richtigen Seite navigiert
while True:
    try:
        # Versuche, den "Weitere 20 LADEN" Button zu finden
        load_more_button = driver.find_element(By.CSS_SELECTOR, "button.dataScroller-button")
        
        # Überprüfe, ob das 'disabled'-Attribut vorhanden ist
        if load_more_button.get_attribute('disabled'):
            break
        else:
            load_more_button.click()
            # Kurze Pause, um das Laden zu erlauben
            time.sleep(1)
    except NoSuchElementException:
        print("Button wurde nicht gefunden. Beende den Loop.")
        break

try:
    while True:
        foods = driver.find_elements(By.CSS_SELECTOR, "a.results--food.ng-star-inserted")
        if not foods:
            print("Keine weiteren Lebensmittel gefunden.")
            break

        for index, food in enumerate(foods):
            try:
                # Um 'stale element reference' zu vermeiden, finde das Element jedes Mal neu
                food = driver.find_elements(By.CSS_SELECTOR, "a.results--food.ng-star-inserted")[index]
                food.click()
                print(driver.current_url)
            except StaleElementReferenceException:
                print("Element nicht mehr im DOM, erneuter Versuch...")
                continue

        # Versuche, "WEITERE 20 LADEN" zu klicken, um mehr Elemente zu laden
        #try:
            #load_more_button = driver.find_element(By.CSS_SELECTOR, "button.dataScroller-button")

            #load_more_button.click()
            #time.sleep(2)
        #except (NoSuchElementException, TimeoutException):
            #print("Keine 'WEITERE 20 LADEN' Schaltfläche gefunden oder Ende der Liste erreicht.")
            #break

    
    #print("Fertig mit dem Anklicken aller Nahrungsmittel.")

finally:
    # Schließe den Browser
    driver.quit()
