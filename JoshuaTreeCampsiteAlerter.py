# This code uses selenium to navigate to the Joshua Tree camping reservation page to search for an available campsite on August 12th
# The HTML content that contains the reserved/available table is retrieved and converted to a dataframe using pandas and then searches for open spots
# The code will stop running when an available campsite is found, and alert the user to which campsite has an availability 

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

options = webdriver.ChromeOptions()

#Keep web browser open after web driver object is closed
#options.add_experimental_option("detach", True)

# Run in the background
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

# Open the main reservation webpage
driver.get("https://www.recreation.gov/search?q=Joshua%20Tree%20National%20Park&entity_id=2782&entity_type=recarea&inventory_type=camping&parent_asset_id=2782")

# Debug checkpoint
#print(driver.title)

# Select the desired dates to search for availability via the calendar
driver.find_element(By.XPATH, value="//*[@id='flex-dates-container']/button/p").click()
driver.find_element(By.XPATH, value="//*[@id='calendar-wrapper']/div/div/div/div[2]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[7]").click()
driver.find_element(By.XPATH, value="//*[@id='calendar-wrapper']/div/div/div/div[2]/div[2]/div/div[3]/div/table/tbody/tr[3]/td[1]").click()
driver.find_element(By.XPATH, value="//*[@id='calendar-button-handler']").click()

availability = False

while(True):

# Indian Cove Campground XPATH
    driver.find_element(By.XPATH, value="//*[@id='rec-card-232472_campground']/a").click()

# Wait 5 seconds for JavaScript to load
    time.sleep(5)

# Switch focus to newly opened tab
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(5)

# Capture website HTML content
    html_content = driver.page_source

# Close the new tab
    driver.close()

# Switch focus back to main tab with campground list
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(1)

# Create a list of data frame objects...only 1 data frame should be in this list
    df_list = pd.read_html(html_content)
    sat12 = df_list[0].loc[:, ('August', 'Sat12')]
    #print(sat12)

# Loop through all rows of data frame corresponding to August 12th, stop search if "A" is found
    for row in sat12:
        if row == "A":
            print("There is availability at Indian Cove!")
            availability = True
            break

# Break out of the while(True) loop, ending the program
    if availability:
        break

## Follow same steps as above, but using XPATH for different camgrounds ##

# Black Rock Campground XPATH
    driver.find_element(By.XPATH, value="//*[@id='rec-card-232473_campground']/a").click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)
    html_content = driver.page_source
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    df_list = pd.read_html(html_content)
    sat12 = df_list[0].loc[:, ('August', 'Sat12')]
    #print(sat12)

    for row in sat12:
        if row == "A":
            print("There is availability at Black Rock!")
            availability = True
            break

    if availability:
        break

# Cottonwood Campground XPATH
    driver.find_element(By.XPATH, value="//*[@id='rec-card-272299_campground']/div/a").click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)
    html_content = driver.page_source
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    df_list = pd.read_html(html_content)
    sat12 = df_list[0].loc[:, ('August', 'Sat12')]
    #print(sat12)

    for row in sat12:
        if row == "A":
            print("There is availability at Cottonwood!")
            availability = True
            break

    if availability:
        break

# Ryan Campground XPATH
    driver.find_element(By.XPATH, value="//*[@id='rec-card-10056207_campground']/a").click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)
    html_content = driver.page_source
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    df_list = pd.read_html(html_content)
    sat12 = df_list[0].loc[:, ('August', 'Sat12')]
    #print(sat12)

    for row in sat12:
        if row == "A":
            print("There is availability at Ryan!")
            availability = True
            break

    if availability:
        break

# Jumbo Rocks Campground XPATH
    driver.find_element(By.XPATH, value="//*[@id='rec-card-272300_campground']/div/a").click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)
    html_content = driver.page_source
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    df_list = pd.read_html(html_content)
    sat12 = df_list[0].loc[:, ('August', 'Sat12')]
    #print(sat12)

    for row in sat12:
        if row == "A":
            print("There is availability at Jumbo Rocks!")
            availability = True
            break

    if availability:
        break

#insert next campground

driver.quit()
