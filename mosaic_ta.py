from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import ezgmail
import re

## NEED TO GET SUMMER 2024 SWP APPROVAL ON AWARDSPRING (prob around March)
## SUMMER 2024 SWP JOBS WILL BE POSTED ON/AFTER MARCH 1

curr = datetime.now()

EMAILFIELD = (By.ID, "userid")
PASSWORDFIELD = (By.ID, "pwd")
LOGIN = (By.CSS_SELECTOR, "input[name = 'Submit']")
CAREERS = (By.CSS_SELECTOR, "img[src='/cs/prepprd/cache/MCM_IMG_CAREERS2_1.SVG']")
SEARCH = (By.CSS_SELECTOR, "input[type = 'text']")
ENTER = (By.CSS_SELECTOR, "input[name = 'SEARCHACTIONS#SEARCH']")
FIRST_YEAR = 'PHYSICS 1* | MATH 1Z* | IBEHS 1* | CHEM 1* | PSYCH 1XX3'
SECOND_YEAR = 'HTHSCI 2F* | MATH 2Z03 | SFWRENG 2D* | SFWRENG 2OP3 | SFWRENG 2XC3'
courses = [FIRST_YEAR, SECOND_YEAR]
##### CHANGE THIS IN RASB PI #####
def main(browser):
    print(f"\nRunning mosaic_ta.py on {curr}...\n")
    browser.get("https://mosaic.mcmaster.ca/")

    # wait for email field and enter email
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys("lunawadm")

    # wait for password field and enter password
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys("Talabat4651")

    # Login
    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(LOGIN)).click()

    # WebDriverWait(browser, 60).until(EC.element_to_be_clickable(CAREERS)).click()
    # go to TA
    browser.get("https://hrprd.mcmaster.ca/psc/prhrprd/EMPLOYEE/HRMS/c/HRS_HRAM_EMP.HRS_APP_SCHJOB.GBL?Page=HRS_APP_SCHJOB&Action=U&FOCUS=Employee&SiteId=1004&NavColl=true")

    job_titles = []
    desc = []
    for year in courses:
        # go in search bar
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(SEARCH)).send_keys(year)
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(ENTER)).click()
        time.sleep(5)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        job_titles.extend(soup.select("a[class='PSHYPERLINK']"))
        desc.extend(soup.select("div[class='attributes PSTEXT align:left']"))
        browser.refresh()


    # ALT for above: desc = soup.select("b") --> this just gives "department" without the actual department name
    message = ''
    # below regex gets DETAILS for each job in GROUPS so email is easier to read
    details = re.compile(r'(.*)\|(.*)\|(.*)')
    f = open("mosaic_ta.txt", "r")
    last_ta_jobs = set()
    new_ta_jobs = set()
    for line in f.readlines():
        # add prev seen job after removing \n from end
        last_ta_jobs.add(line.strip())
    f.close()

    i = 0
    if job_titles:
        while job_titles[i].getText() not in last_ta_jobs:
            message += job_titles[i].getText() + '\n'
            new_ta_jobs.add(job_titles[i].getText() + '\n')
            for detail in details.search(desc[i].getText()).groups():
                message += detail.strip() + '\n'
            message += '\n'
            i += 1
            if i == len(job_titles):
                message = "Unfortunately all of the last seen jobs have been removed and the program cannot judge whether these jobs are new or not\n\n" + message
                break

    # if new jobs have been found, send message and update text file
    if message != '':
        ezgmail.send('mansoorlunawadi@yahoo.ca', 'New TA Jobs', message)
        print(f"MOSAIC TA Email sent with message\n\n{message}\n\n")
        with open("mosaic_ta.txt", "w") as f:
            for job in new_ta_jobs:
                f.write(job + '\n')
    else:
        ezgmail.send('mansoorlunawadi@yahoo.ca', 'No New TA Jobs', 'Hopefully soon :)')
        print("MOSAIC TA Email sent (no new jobs)\n")

    print("Done.\n")
    print("----------------------------------------------------------")
