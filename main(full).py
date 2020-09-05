# Methodology adapted from "Code Heroku"
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import csv
import sys
import requests
import pandas as pd

import googlemaps
from datetime import datetime

# # **** For Heroku ****n
# GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
# CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.binary_location = GOOGLE_CHROME_PATH

# browser = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

# **** End of Heroku Setup ****

def testMaps(CompanyName=None, CompanyLocation=None):
    APIkey = "*** API KEY ***"

    gmaps = googlemaps.Client(key=APIkey)

    if CompanyName is None:
        addressToGet = CompanyLocation
    elif CompanyLocation is None:
        addressToGet = CompanyName
    else:
        addressToGet = CompanyName + ", " + CompanyLocation

    # Geocoding an address
    geocode_result = gmaps.geocode(addressToGet)
    # print("LongLat for your search is: ", geocode_result)
    # print("What you want is: ")
    # print(geocode_result[0]['geometry']['location']["lng"], geocode_result[0]['geometry']['location']["lat"], geocode_result[0]['formatted_address'])
    return geocode_result[0]['geometry']['location']["lng"], geocode_result[0]['geometry']['location']["lat"], geocode_result[0]['formatted_address']

    # # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode(geocode_result)
    # print("Reversed geocode address is: ", reverse_geocode_result)

    # Request directions via public transit
    # now = datetime.now()
    # directions_result = gmaps.directions("Sydney Town Hall",
    #                                     "Parramatta, NSW",
    #                                     mode="transit",
    #                                     departure_time=now)

class JobSearch():

    def __init__(self):
        pass

    def search(self, searchPosition, searchLocation, searchRadius):
        # Set up Attribute list and DataFrame
        attributeList = ["jobtitle" , "location", "company", "salary", "sponsoredGray"]
        df = pd.DataFrame(columns=["Title", 
                                "Location", 
                                "Company", 
                                "Salary", 
                                "Sponsored", 
                                "Description", 
                                "Link",
                                "Address",
                                "Lng",
                                "Lat"])

        # Convert search terms to url compatible format
        searchPosition = searchPosition.replace(" ", "+")
        searchLocation = searchLocation.replace(" ", "+")
        print (searchPosition, " ", searchLocation, " ", searchRadius)
        

        for page in range(0, 10, 10):
            
            # Generate link for driver
            link = "https://www.indeed.com/jobs?q=" + searchPosition + "&l=" + searchLocation + "&radius="  + searchRadius + "&start=" + str(page)

            # Set up Selenium driver
            driver = webdriver.Chrome("./chromedriver")
            # driver = browser
            driver.implicitly_wait(1)
            driver.get(link)

            # Get all jobs in current page
            all_jobs = driver.find_elements_by_class_name("result")

            # Loop through postings on current page to extract information
            for posting in all_jobs[:-5]:
                # try:
                html = posting.get_attribute('innerHTML')
                soup = BeautifulSoup(html, 'html.parser')

                jobEntry = {
                    "Title": self.extractJobElement(soup, attributeList[0]), 
                    "Location": self.extractJobElement(soup, attributeList[1]), 
                    "Company": self.extractJobElement(soup, attributeList[2]), 
                    "Salary": self.extractJobElement(soup, attributeList[3]), 
                    "Sponsored":self.extractJobElement(soup, attributeList[4])
                    }
                
                summary = posting.find_elements_by_class_name("summary")[0]
                
                # Error handling for pop-up
                # ****** Disabled in demo to increase search speed*****
                # try:
                #     summary.click()
                # except:
                #     try:
                #         closeButton = driver.find_elements_by_class_name("popover-x-button-close")
                #         closeButton.close()
                #         summary.click()
                #     except:
                #         pass

                summary.click()

                # Fetches application link
                applyLink = "None"
                # time.sleep(15)

                # **** Test speed of finding link ****
                # try:
                #     link = driver.find_element_by_link_text('Apply On Company Site')
                #     applyLink = link.get_attribute('href')
                # except:

                # **** End test speed of finding link ****
                    # In case direct link to company website not available, links to indeed posting
                time.sleep(.2)
                applyLink = driver.current_url
                
                # Tries different id keywords for job description
                # Test
                # descriptionTestKeywords = ["jobDescriptionText","vjs-desc","jobsearch-JobComponent-embeddedBody"]
                descriptionTestKeywords = ["jobDescriptionText"]
                description = "None"
                # for keyword in descriptionTestKeywords:
                #     try:
                #         description = driver.find_element_by_id(keyword).text.replace("\n"," ")
                #         print(keyword)
                #         break
                #     except:
                #         pass
                        
                try:
                        description = driver.find_element_by_id("jobDescriptionText").text.replace("\n"," ")
                        print(keyword)
                        break
                    except:
                        pass
                
                # Appends job link and description to jobEntry
                jobEntry["Link"] = applyLink
                jobEntry["Description"] = description
    
                # Tests Map Call functionality
                longitude = latitude = address = "None" 
                
                try:
                    longitude,latitude, address = testMaps(jobEntry["Company"], jobEntry["Location"])
                    jobEntry["Lng"] = longitude
                    jobEntry["Lat"] = latitude
                    jobEntry["Address"] = address
                except:
                    # print("Failed to get long, lat!")
                    pass

                # Appends current post to DataFrame
                df = df.append(jobEntry, ignore_index=True)
                # except:
                #     pass        
        # Exports to CSV
        df.to_csv("./data/testFlask.csv", index=False)
        # print(df.to_json(orient='index'))
        return df.to_json(orient='index')

    def extractJobElement(self,soupObject, elementToExtract):
        try: 
            return soupObject.find(class_= elementToExtract).text.replace("\n","").strip()
        except:
            return "None"


if __name__ == "__main__":

    newSearch = JobSearch()
    newSearch.search("software engineering intern", "CA 94105", "5")
    # testMaps()

