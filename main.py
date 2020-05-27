# Methodology adapted from "Code Heroku"
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import sys
import requests
import pandas as pd

def extractJobElement(soupObject, elementToExtract):
    try: 
        return soupObject.find(class_= elementToExtract).text.replace("\n","").strip()
    except:
        return "None"


if __name__ == "__main__":

    # Set up Attribute list and DataFrame
    attributeList = ["jobtitle" , "location", "company", "salary", "sponsoredGray"]
    df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Sponsored", "Description"])

    for page in range(0, 500, 10):

        # Set up Selenium driver
        driver = webdriver.Chrome("./chromedriver")
        driver.implicitly_wait(4)
        driver.get("https://www.indeed.com/jobs?q=Software+Engineering+Intern&l=San+Francisco%2C+CA&radius=50&start="+str(page))

        # Get all jobs in current page
        all_jobs = driver.find_elements_by_class_name("result")

        # Loop through postings on current page to extract information
        for posting in all_jobs:
            try:
                html = posting.get_attribute('innerHTML')
                soup = BeautifulSoup(html, 'html.parser')

                jobEntry = {
                    "Title": extractJobElement(soup, attributeList[0]), 
                    "Location": extractJobElement(soup, attributeList[1]), 
                    "Company": extractJobElement(soup, attributeList[2]), 
                    "Salary": extractJobElement(soup, attributeList[3]), 
                    "Sponsored":extractJobElement(soup, attributeList[4])
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
                
                # Tries different id keywords for job description
                descriptionTestKeywords = ["vjs-desc", "jobDescriptionText"]
                description = "None"
                for keyword in descriptionTestKeywords:
                    try:
                        description = driver.find_element_by_id(keyword).text.replace("\n","")
                        break
                    except:
                        pass

                jobEntry['Description'] = description

                # Appends current post to DataFrame
                print
                df = df.append(jobEntry, ignore_index=True)
            except:
                print("Error with this listing!")
                pass        

    # Exports to CSV
    df.to_csv("./data/test4.csv", index=False)
