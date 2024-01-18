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


##### CHANGE THIS IN RASB PI #####
def main(browser):
    print(f"\nRunning mosaic_swp.py on {curr}...\n")
    # go to SWP -- already signed in from mosaic_ta

    browser.get("https://hrprd.mcmaster.ca/psc/prhrprd/EMPLOYEE/HRMS/c/HRS_HRAM_EMP.HRS_APP_SCHJOB.GBL?Page=HRS_APP_SCHJOB&Action=U&FOCUS=Employee&SiteId=1003&NavColl=true")

    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(SEARCH)).send_keys("summer")

    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(ENTER)).click()
    time.sleep(5)
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    job_titles = soup.select("a[class='PSHYPERLINK']")
    desc = soup.select("div[class='attributes PSTEXT align:left']")
    # ALT for above: desc = soup.select("b") --> this just gives "department" without the actual department name
    message = ''
    # below regex gets DETAILS for each job in GROUPS so email is easier to read
    details = re.compile(r'(.*)\|(.*)\|(.*)')
    f = open("mosaic_swp.txt", "r")
    last_swp_jobs = set()
    new_swp_jobs = set()
    for line in f.readlines():
        # add prev seen job after removing \n from end
        last_swp_jobs.add(line.strip())
    f.close()

    i = 0
    if job_titles:
        while job_titles[i].getText() not in last_swp_jobs:
            message += job_titles[i].getText() + '\n'
            new_swp_jobs.add(job_titles[i].getText() + '\n')
            for detail in details.search(desc[i].getText()).groups():
                message += detail.strip() + '\n'
            message += '\n'
            i += 1
            if i == len(job_titles):
                message = "Unfortunately all of the last seen jobs have been removed and the program cannot judge whether these jobs are new or not\n\n" + message
                break

    # if new jobs have been found, send message and update text file
    if message != '':
        ezgmail.send('swpjobs@googlegroups.com', 'New Summer 2024 SWP Jobs', message)
        print(f"MOSAIC SWP Email sent with message\n\n{message}\n\n")
        with open("mosaic_swp.txt", "w") as f:
            for job in new_swp_jobs:
                f.write(job + '\n')
    else:
        ezgmail.send('swpjobs@googlegroups.com', 'No New Summer 2024 SWP Jobs', 'Hopefully soon :)')
        print("MOSAIC SWP Email sent (no new jobs)\n")

    print("Done.\n")
    print("----------------------------------------------------------")