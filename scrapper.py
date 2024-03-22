from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import By
import undetected_chromedriver as uc
from time import sleep
import json


def main():

    # Name of the vessels to find
    vesselNames = [
        "KRITI VIGOR",
        "QUEEN MARY 2",
        "EVER GIVEN",
        "QUEEN ELIZABETH",
        "ECLIPSE",
        "WIZARD",
        "NORTHWESTERN",
        "BRITANNIA",
        "VENTURA",
        "AURORA",
    ]
    # Url of the website
    url = "https://www.marinetraffic.com/"

    # Init undetected_chromedriver cause MarineTraffic detects bots
    driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Open the URL in the browser
    driver.get(url)

    # Wait for the page to load
    sleep(5)
    # Check for page ready
    WebDriverWait(driver, 10).until(
        EC.title_contains(
            "MarineTraffic: Global Ship Tracking Intelligence | AIS Marine Traffic"
        )
    )

    # Check for the element with class name "css-1yp8yiu" to be clickable (cookies popup)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "css-1yp8yiu"))
    ).click()

    sleep(0.5)
    # Check for the element with ID "login" to be clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login"))
    ).click()

    sleep(0.5)
    # Check for the email input field to be visible
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    email_input.send_keys("edriseitlli@gmail.com")

    sleep(0.5)
    # Check for the password input field to be visible
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    password_input.send_keys("yu*8ATD9Qg*pi8Z")

    sleep(0.5)
    # Check for the login button to be clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login_form_submit"))
    ).click()

    # Wait for the presence of a specific element on the refresh after login
    sleep(5)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myAccount"))
    )

    searchVessels(driver, vesselNames)

    sleep(5)

    driver.quit()


def searchVessels(driver, vesselNames):
    attributes = ["Name", "IMO", "MMSI", "Speed", "Course"]
    data = []
    for vesselName in vesselNames:
        sleep(1)
        # Check for the search input field to be visible and clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "searchMarineTraffic"))
        ).click()
        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "searchMT"))
        )
        search_input.send_keys(vesselName)

        # Wait for the search results
        sleep(2)
        # find all li elements of the search results
        liElements = driver.find_elements(
            By.CSS_SELECTOR,
            ".MuiButtonBase-root.MuiListItemButton-root.MuiListItemButton-gutters.MuiListItemButton-root.MuiListItemButton-gutters.css-1ymo28p",
        )
        for li in liElements:
            if li.find_element(By.TAG_NAME, "b").text == vesselName:
                li.click()
                break

        # Wait for the page to load
        sleep(5)
        # find all tr elements of the search results
        trElements = driver.find_elements(
            By.CSS_SELECTOR, ".MuiTableRow-root.css-1gmif6u"
        )
        # find attributes Name, IMO, MMSI, Speed, Course
        vesselData = {}
        for tr in trElements:
            attr = tr.find_element(By.TAG_NAME, "th").text
            value = tr.find_element(By.TAG_NAME, "td").text
            if attr in attributes:
                vesselData[attr] = value
        data.append(vesselData)
        
    # Convert the extracted data to a JSON array
    json_data = json.dumps(data, indent=2)

    # Write JSON data to a file
    with open('results.json', 'w') as file:
        file.write(json_data)



if __name__ == "__main__":
    main()
