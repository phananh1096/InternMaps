# Methodology adapted from "Code Heroku"
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import sys
import requests
import pandas as pd

import googlemaps
from datetime import datetime

print(pd.__version__)

def testMaps(CompanyName, CompanyLocation):
    APIkey = "AIzaSyAn2aGy_mPi-cr-bOopwYzEr2r1athMKJ8"

    gmaps = googlemaps.Client(key=APIkey)

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
            driver.implicitly_wait(4)
            driver.get(link)

            # Get all jobs in current page
            all_jobs = driver.find_elements_by_class_name("result")

            # Loop through postings on current page to extract information
            for posting in all_jobs:
                try:
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
                    try:
                        summary.click()
                    except:
                        try:
                            closeButton = driver.find_elements_by_class_name("popover-x-button-close")
                            closeButton.close()
                            summary.click()
                        except:
                            pass

                    # Fetches application link
                    applyLink = "None"
                    try:
                        link = driver.find_element_by_link_text('Apply On Company Site')
                        applyLink = link.get_attribute('href')
                        # print(applyLink)
                    except:
                        # In case direct link to company website not available, links to indeed posting
                        time.sleep(1)
                        applyLink = driver.current_url
                        # print(applyLink)
                    
                    # Tries different id keywords for job description
                    descriptionTestKeywords = ["vjs-desc", "jobDescriptionText", "jobsearch-JobComponent-embeddedBody"]
                    description = "None"
                    for keyword in descriptionTestKeywords:
                        try:
                            description = driver.find_element_by_id(keyword).text.replace("\n","")
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
                        print("Failed to get long, lat!")
                        pass

                    # Appends current post to DataFrame
                    df = df.append(jobEntry, ignore_index=True)
                except:
                    print("Error with this listing!")
                    pass        
        # Exports to CSV
        df.to_csv("./data/testFlask.csv", index=False)
        print(df.to_json())
        return df.to_json()

    def extractJobElement(self,soupObject, elementToExtract):
        try: 
            return soupObject.find(class_= elementToExtract).text.replace("\n","").strip()
        except:
            return "None"


if __name__ == "__main__":

    newSearch = JobSearch()
    newSearch.search("software engineering intern", "CA 94105", "5")
    # testMaps()

