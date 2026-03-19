from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlsplit, urlunsplit
import sys


def Business_scraper(search_query:str, output_file:str):

    # lunch a chrome browser using selenium
    driver = webdriver.Chrome() # type:ignore

    # open google maps in browser
    driver.get("https://www.google.com/maps")

    # define the waiter
    wait = WebDriverWait(driver, 10)

    # wait time for the page to load then locate the search input box  with a
    # search_box = driver.find_element(By.ID, "searchboxinput")
    search_box = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "UGojuc"))
    )

    # type the query into the search box
    search_box.send_keys(search_query)

    # locate the search button
    search_button = driver.find_element(By.CLASS_NAME, "mL3xi")

    # click the search button to start the search 
    search_button.click()

    # wait for the result to load
    time.sleep(8)


    # find the scrollable result panel
    scrollable_div = driver.find_element(By.XPATH, '//div[@role="feed"]')

    # scroll to load more businesses
    for _ in range(4):
        # scroll down in the results panel
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight",
            scrollable_div
        )

        # wait for the results to load
        time.sleep(4)

    # After scrolling , collect all business cards
    businesses = driver.find_elements(By.CLASS_NAME, "Nv2PK")
    print(f"Found {len(businesses)} businesses")

    # ############## Extract the business links

    # store the links 
    links = []

    for business in businesses:
        try:
            # find the links in each card
            link = business.find_element(By.TAG_NAME, "a").get_attribute("href")

            # save the link
            links.append(link)
        except:
            pass


    print("Total businesses links found:", len(links))

    # create an empty list to store the scraped data
    data = []

    # loop through each business page  by their links
    for link in links:
        # open the business listing
        driver.get(link)

        # wait for page to load 
        time.sleep(10)

        # scroll in business page to load the needed elements
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);", scroll_card)

        # use explicit delay 
        def save_loading_and_extraction(by, value):

            try:
                element = wait.until(
                    EC.presence_of_element_located((by, value))
                )
                if value == "HHrUdb":
                    return element.text.split(" ")[0]
                if value == "//a[@data-item-id='authority']":
                    return element.get_attribute("href")
                else:
                    return element.text
            except:
                return None
            


        # extract feilds 
        name = save_loading_and_extraction(By.CLASS_NAME, "DUwDvf")
        rating = save_loading_and_extraction(By.CLASS_NAME, "fontDisplayLarge")
        review = save_loading_and_extraction(By.CLASS_NAME, "HHrUdb")
        address = save_loading_and_extraction(By.XPATH, "//button[@data-item-id='address']")
        phone = save_loading_and_extraction(By.XPATH, "//button[contains(@data-item-id, 'phone:tel')]")
        website_ = save_loading_and_extraction(By.XPATH, "//a[@data-item-id='authority']")
    
        # clean the website url 
        def get_proper_url(url):

            split_url = urlsplit(url=url)
            
            url_withou_query = split_url._replace(query="")

            if not url :
                return None
            else:
                return urlunsplit(url_withou_query)
            # if url_withou_query:
            #     return urlunsplit(url_withou_query)
            # else:
            #     return None
        
        website = get_proper_url(website_)
        
        
        # store the extracted information to a list of dicts
        data.append({
            "company_name": name,
            "phone":phone,
            "address": address,
            "rating": rating,
            "review": review,
            "website":website,
            "google_maps_link": link
        })

        print("Scraped:", name)

    # convert the list into a dataframe
    df = pd.DataFrame(data=data)


    # drop duplicates
    df = df.drop_duplicates(subset="company_name")

    # save to a CSV file
    if output_file.endswith(".csv"):
        df.to_csv(f"output/{output_file}", index=False)

    elif output_file.endswith(".json"):
        df.to_json(f"output/{output_file}", indent=4)

    else:
        df.to_csv(f"output/{output_file}.csv", index=False)

    print("Scraping completed and dataset is saved ✅✅✅")


    # close the browser when finished
    driver.quit()


#search query
# business_query = "solar installer Amsterdam"
# Business_scraper(search_query=business_query)

if __name__ == "__main__":
    if len(sys.argv) != 3 :
        print("Usage: python scraper.py  'query to search for'  'output_file_name'")
        sys.exit(1)
    
    query  = sys.argv[1]
    output_file = sys.argv[2]

    Business_scraper(search_query=query, output_file=output_file )
    
