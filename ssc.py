from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import ezgmail
import re

curr = datetime.now()

EMAILFIELD = (By.ID, "i0116")
PASSWORDFIELD = (By.ID, "i0118")
NEXTBUTTON = (By.ID, "idSIButton9")
MENU = (By.CSS_SELECTOR, "button[aria-label='Toggle Main Menu']")
SSC = (By.CSS_SELECTOR, "a[href = '/myAccount/studentSuccessCentre.htm']")
WORK = (By.CSS_SELECTOR, "a[href = '/myAccount/studentSuccessCentre/employment.htm']")
POSTINGS = (By.CSS_SELECTOR, "a[href = '/myAccount/studentSuccessCentre/employment/postings.htm']")
SPRING = (By.CSS_SELECTOR, "a[href = '#runMultipleSearchesDialog']")
TEST = (By.CSS_SELECTOR, "select[id = 'savedSearchId']")
TEST2 = (By.CSS_SELECTOR, "option[value = '884']")

BOX = (By.CSS_SELECTOR, "input[type = 'checkbox']")
SEARCH = (By.CSS_SELECTOR, "button[type = 'submit']")

def main(browser, recipient):
    print(f"\nRunning ssc.py on {curr}...\n")
    # already signed in -- from oscarplus.main
    # Redirect to SSC jobs URL

    browser.get("https://www.oscarplusmcmaster.ca/myAccount/studentSuccessCentre/employment/postings.htm")

    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(TEST)).click()

    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(TEST2)).click()

    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    all = soup.select('td')
    # first group in deadlineRegex matches DATE and second matches TIME (w/o unnecessary spaces)

    IDRegex = re.compile(r'(\d\d\d\d\d\d)', re.I) 
    dateRegex = re.compile(r'(\w+\s\d+,\s\d+)', re.I)
    timeRegex = re.compile(r'(\d+:\d+\s\w+)', re.I)
    new = all[5].getText().strip()
    f = open("ssc.txt", "r")
    last_jobs = set()
    for line in f.readlines():
        # add prev seen job after removing \n from end
        last_jobs.add(line.strip())
    f.close()


    updated_last_jobs = set()
    i = 0
    j = 0
    message = ''
    # just want role, company, openings, location, and deadline
    # send all new jobs (after last seen)
    while True:

        temp = IDRegex.search(all[i].getText())
        while temp == None:
            i += 1
            temp = IDRegex.search(all[i].getText())
        # will reach here after finding ID number of job and the associated index in ALL

        # get other relevant details of this job from ALL variable
        role = all[i + 1].getText().strip()
        if role in last_jobs:
            break
        updated_last_jobs.add(role)
        company = all[i + 2].getText()
        openings = all[i + 5].getText()
        location = all[i + 6].getText()
        deadline = all[i + 10].getText()
        # get date and time from deadline
        date = dateRegex.search(deadline).group()
        time = timeRegex.search(deadline).group()
        deadline = date + " " + time
        message += f"Role: {role}\nCompany: {company}\nOpenings: {openings}\nLocation: {location}\nDeadline: {deadline}"
        message += '\n\n'

        # inc i so same id not reused
        i += 12
        # if we have reached the end of jobs

        if i == len(all):
            message = "Unfortunately all of the last seen jobs have been removed and the program cannot judge whether these jobs are new or not\n\n" + message
            break

    # send email if new jobs
    if message != '':
        ezgmail.send(recipient, 'New Summer 2024 SSC Jobs', message)
        print(f"SSC Email sent with message\n\n{message}\n\n")
        # set last seen to new IF message is non-empty else keep as is
        with open("ssc.txt", "w") as f:
            for job in updated_last_jobs:
                f.write(job + '\n')    
    else:
        ezgmail.send(recipient, 'No New Summer 2024 SSC Jobs', 'Hopefully soon :)')
        print("SSC Email sent (no new jobs)\n")

    print("Done.\n")
    print("----------------------------------------------------------")

