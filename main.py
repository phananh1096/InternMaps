from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import sys
import requests
import pandas as pd

def extractJobElement(soupObject, elementToExtract):
    try: 
        element = soupObject.find()





if __name__ == "__main__":

    # link = "https://www.indeed.com/jobs?q=Software+Engineering+Intern&l=San+Francisco%2C+CA&radius=50"
    # response = requests.get(link)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # jobs = soup.find_all("div", class_= "clickcard")
    # # jobs = soup.find(string="Intel")
    # print(jobs)
    driver = webdriver.Chrome("./chromedriver")

    dataframe = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Sponsored", "Description"])
    driver.get("https://www.indeed.com/jobs?q=Software+Engineering+Intern&l=San+Francisco%2C+CA&radius=50")

    all_jobs = driver.find_elements_by_class_name("result")

    for posting in all_jobs:
        # print (posting)
        html = posting.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())
        
        # Extracts title for each job
        try:
            title = soup.find('a', class='jobtitle').text.replace('\n\, '')
        except: 
            title = 'None'