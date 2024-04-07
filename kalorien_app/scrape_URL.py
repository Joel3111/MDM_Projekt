from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from pymongo import MongoClient
import time

def scrape_data():

    # Verbindung zu MongoDB herstellen
    client = MongoClient("mongodb+srv://joelegli:test@nutritionbase.rx1ko0e.mongodb.net/")
    db = client["NutritionBase"]
    collection = db["URL_Liste"]  # Ändert den Sammlungsnamen, wenn nötig

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
        gesammelte_urls = []
        
        foods = driver.find_elements(By.CSS_SELECTOR, "a.results--food.ng-star-inserted")
        if not foods:
            print("Keine weiteren Lebensmittel gefunden.")

        for index, food in enumerate(foods):
            # Um 'stale element reference' zu vermeiden, finde das Element jedes Mal neu
            food = driver.find_elements(By.CSS_SELECTOR, "a.results--food.ng-star-inserted")[index]
            food.click()

            # Speichere die aktuelle URL in der Liste
            gesammelte_urls.append(driver.current_url)
            print(driver.current_url)

        # Füge jede URL in die Datenbank ein, wenn sie noch nicht vorhanden ist
        for url in gesammelte_urls:
            result = collection.update_one(
                {"url": url},  # Suchkriterium
                {"$setOnInsert": {"url": url}},  # Nur setzen, wenn ein neues Dokument eingefügt wird
                upsert=True  # Fügt ein neues Dokument ein, wenn keines gefunden wird, das den Kriterien entspricht
            )

            if result.upserted_id:
                print("Neue URL hinzugefügt:", url)
            else:
                print("URL existiert bereits in der Datenbank.")

        print("Alle URLs wurden erfolgreich verarbeitet.")

    finally:
        # Schließe den Browser
        driver.quit()
