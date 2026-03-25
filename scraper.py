from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd
import time
import random
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlsplit, urlunsplit
import sys

from tracker import mark_done, save_progress


def Business_scraper(search_query:str, output_format:str="csv"):
    """
    Extract and store business data 
    Args:
        search_query : query to perform the search on 
        output_format :format to which to save the extracted data (CSV or JSON)

    """

    print(f"Starting🔰🔰🔰: {search_query}")
    # lunch a chrome browser using selenium
    driver = webdriver.Chrome() # type:ignore

    try :
        # open google maps in browser
        driver.get("https://www.google.com/maps")
        time.sleep(3)

        # define the waiter
        wait = WebDriverWait(driver, 10)

        # wait for the page to load then locate the search input box  
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
        time.sleep(15)


        # find the scrollable result panel
        scrollable_div = driver.find_element(By.XPATH, '//div[@role="feed"]')

        # scroll to load more businesses
        for _ in range(4):
            # scroll down in the results panel
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scrollable_div
            )

            # wait for the results to load use random time to make it look more human
            time.sleep(random.uniform(2, 4))

        # After scrolling , collect all business cards
        businesses = driver.find_elements(By.CLASS_NAME, "Nv2PK")

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


        print(f"Found {len(links)} Total businesses links for {search_query}")

        # create an empty list to store the scraped data
        data = []

        # loop through each business page  by their links
        for link in links:
            # open the business listing card using their links
            driver.get(link)

            # wait for page to load use random sleep to make it look more human 
            time.sleep(random.uniform(4, 10))

            # scroll in business page to load the needed elements
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);", scroll_card)

            NAME_PATH = "DUwDvf"
            REVIEW_PATH = "//div[contains(@class,'F7nice')]/span[2]//span[@aria-label]"
            RATING_PATH = "//div[contains(@class,'F7nice')]/span/span[1]"
            ADDRESS_PATH = "//button[@data-item-id='address']"
            PHONE_PATH = "//button[contains(@data-item-id, 'phone')]"
            WEBSITE_PATH = "//a[@data-item-id='authority']"


    

            # use explicit delay 
            def save_loading_and_extraction(by, value, retries=3):
                for _ in range(retries):
                    try:
                        element = driver.find_element(by, value)
                    
                        if element and value ==  REVIEW_PATH:
                            return element.text.strip("()")
                            
                            
                        if element and value == "//a[@data-item-id='authority']":
                            web = element.get_attribute("href")
                            return get_proper_url(web)
                        else:
                            return element.text
                    except:
                        time.sleep(3)
                return None
                    


            # extract feilds 
            name = save_loading_and_extraction(By.CLASS_NAME,NAME_PATH )
            rating = save_loading_and_extraction(By.XPATH,RATING_PATH )
            review = save_loading_and_extraction(By.XPATH, REVIEW_PATH) 
            address = save_loading_and_extraction(By.XPATH, ADDRESS_PATH)
            phone = save_loading_and_extraction(By.XPATH,PHONE_PATH )
            website= save_loading_and_extraction(By.XPATH, WEBSITE_PATH)
            
            print("Rating  💡💡:", rating)
            print("Review 🤩🤩:", review)
            print("website 🖇️🖇️🖇️:", website)
            print("phone 📞📞📞:", phone)
            
            # clean the website url 
            def get_proper_url(url):

                split_url = urlsplit(url=url)
                
                url_withou_query = split_url._replace(query="")

                if not url :
                    return None
                else:
                    return urlunsplit(url_withou_query)
                
            # store the extracted information to a list of dicts
            data.append({
                "company_name": name,
                "phone": phone,
                "address": address,
                "rating": rating,
                "review": review,
                "website": website,
                "google_maps_link": link
            })

            print(f"Scraped: {search_query} -> {name}")

        # convert the list into a dataframe
        df = pd.DataFrame(data=data)


        # drop duplicates
        df = df.drop_duplicates(subset="company_name")

        # check if the output dir exsist else make one
        os.makedirs("output", exist_ok=True)
        
        # construct the a valid filename
        filename = f"output/{search_query.replace(' ', '_')}.{output_format}"

        # save to a CSV file
        if output_format == "csv":
            df.to_csv(filename, index=False)

        elif output_format == "json":
            df.to_json(filename, indent=4)

        print(f"Scraping done, {filename} saved ✅✅✅")

        # save progress to file 
        mark_done(search_query)
        # 

    except  Exception as e:

        # save error logs
        os.makedirs("logs", exist_ok=True)

        with open("logs/errors.txt", "a") as file:
            file.write(f"{search_query} -> DESCRIPTION👹👹👹: {str(e)}\n")

        print(f"Error with {search_query}")


    # close the browser when finished
    driver.quit()


#search query
# business_query = "solar installer Amsterdam"
# Business_scraper(search_query=business_query)

if __name__ == "__main__":
    if len(sys.argv) != 3 :
        print("Usage: python scraper.py  'query to search for'  'csv'")
        sys.exit(1)
    
    query  = sys.argv[1]
    output_format = sys.argv[2]

    Business_scraper(search_query=query, output_format=output_format )
    
