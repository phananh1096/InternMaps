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

    # for page in range(0, 200, 10):
    # Required driver for selenium
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(4)

    # List of Attributes to be extracted   
    attributeList = ["jobtitle" , "location", "company", "salary", "sponsoredGray"]
    
    df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Sponsored", "Description"])
    # driver.get("https://www.indeed.com/jobs?q=Software+Engineering+Intern&l=San+Francisco%2C+CA&radius=50&start="+str(page))
    driver.get("https://www.indeed.com/jobs?q=Software+Engineering+Intern&l=San+Francisco%2C+CA&radius=50")

    all_jobs = driver.find_elements_by_class_name("result")

    count = 0
    for posting in all_jobs:
        try:
            html = posting.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')

            
            # print(soup.prettify())       
            jobEntry = {
                "Title": extractJobElement(soup, attributeList[0]), 
                "Location": extractJobElement(soup, attributeList[1]), 
                "Company": extractJobElement(soup, attributeList[2]), 
                "Salary": extractJobElement(soup, attributeList[3]), 
                "Sponsored":extractJobElement(soup, attributeList[4])
                }
            
            summary = posting.find_elements_by_class_name("summary")[0]
            try:
                summary.click()
            except:
                try:
                    closeButton = driver.find_elements_by_class_name("popover-x-button-close")
                    closeButton.close()
                    summary.click()
                except:
                    pass
            
            descriptionTestKeywords = ["vjs-desc", "jobDescriptionText"]
            description = "None"
            for keyword in descriptionTestKeywords:
                try:
                    description = driver.find_element_by_id(keyword).text.replace("\n","")
                    break
                except:
                    pass

            jobEntry['Description'] = description
            df = pd.concat(df, pd.DataFrame(jobEntry, ignore_index=True))
            print(jobEntry)
        except:
            print("Error with this listing!")
            pass

        df.to_csv("./data/test2.csv", index=False)