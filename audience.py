import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# use the resource path for the driver
driver_path = resource_path("chromedriver")
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

driver.get("https://ads.tiktok.com/i18n/home")
print("Log in and navigate to the audience manager (create audience -> custom audience -> engagement).")
input("Press enter after reaching the correct spot to begin the script: ")
group_id_list = input("Paste in the full list here, with each number separated by a space: ").split()

try:
    print("start")

    print(group_id_list)

    # click the ad groups input field
    ad_groups_button = driver.find_element(By.XPATH, "//input[@placeholder='All']")
    actions = ActionChains(driver)
    actions.move_to_element(ad_groups_button).click().perform()

    # find and click the search input field
    search_input = driver.find_element(By.XPATH, "//input[@placeholder='Please enter']")
    search_input.click()

    for group_id in group_id_list:
        # enter the current group ID into the search field
        search_input.send_keys(group_id)

        time.sleep(0.5)

        # wait for the first audience result to appear and click it
        first_audience_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-testid='source-in-new-engagement-0-mst-t-0']"))
        )
        first_audience_result.click()

        time.sleep(0.5)

        # clear the search input field for the next ID
        search_input.send_keys(Keys.CONTROL + "a")  # Select all text
        search_input.send_keys(Keys.BACKSPACE)  # Delete selected text

        time.sleep(0.5)

    print("end")

except Exception as e:
    print(f"error: {e}")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
