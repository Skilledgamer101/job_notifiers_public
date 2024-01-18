from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import ezgmail
import re
from time import sleep

curr = datetime.now()

EMAILFIELD = (By.ID, "i0116")
PASSWORDFIELD = (By.ID, "i0118")
NEXTBUTTON = (By.ID, "idSIButton9")
CALL = (By.CSS_SELECTOR, "div[data-value = 'TwoWayVoiceMobile']")
FIRST_NOT_IN = (By.CSS_SELECTOR, "a[id = 'signInAnotherWay']")
NOT_SIGNED_IN = (By.CSS_SELECTOR, "img[src='https://aadcdn.msftauth.net/shared/1.0/content/images/arrow_left_43280e0ba671a1d8b5e34f1931c4fe4b.svg']")
MENU = (By.CSS_SELECTOR, "button[type = 'button'][class ='btn__hero btn--info drop-down__btn js--btn-toggle-side-menu has--ripple btn--ripple  has-ripple'][style='padding:8px; box-shadow:none;'][aria-label='Toggle Main Menu']")
ENG = (By.CSS_SELECTOR, "a[href = '/myAccount/eng.htm']")
WORK = (By.CSS_SELECTOR, "a[href = '/myAccount/eng/coop.htm']")
POSTINGS = (By.CSS_SELECTOR, "a[href = '/myAccount/eng/coop/postings.htm']")
SPRING = (By.CSS_SELECTOR, "a[href = '#runMultipleSearchesDialog']")
TEST = (By.CSS_SELECTOR, "select[id = 'savedSearchId']")
TEST2 = (By.CSS_SELECTOR, "option[value = '994']")

BOX = (By.CSS_SELECTOR, "input[type = 'checkbox']")
SEARCH = (By.CSS_SELECTOR, "button[type = 'submit']")

# for Windows: C:\Windows\System32\chromedriver.exe

def signin(browser):
    try:
        browser.get('https://www.oscarplusmcmaster.ca/Shibboleth.sso/Login?entityID=https://sso.mcmaster.ca/idp/shibboleth&target=https://www.oscarplusmcmaster.ca/secure/ssoStudent.htm')

        # wait for email field and enter email
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys("lunawadm@mcmaster.ca")

        # Click Next
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

        # wait for password field and enter password
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys("Talabat4651")

        # Click Login - same id?
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

        # Call
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(CALL)).click()
        # Wait for me to pick up call
        sleep(60)
        # If not picked up. keep calling again
        # "first not in" is the "sign in another way"
        first_not_in = browser.find_elements(FIRST_NOT_IN[0], FIRST_NOT_IN[1])
        if first_not_in:
            WebDriverWait(browser, 60).until(EC.element_to_be_clickable(FIRST_NOT_IN)).click()
            WebDriverWait(browser, 60).until(EC.element_to_be_clickable(CALL)).click()
            sleep(60)
        # "not in" is the back arrow
        not_in = browser.find_elements(NOT_SIGNED_IN[0], NOT_SIGNED_IN[1])
        while not_in:
            WebDriverWait(browser, 60).until(EC.element_to_be_clickable(NOT_SIGNED_IN)).click()
            WebDriverWait(browser, 60).until(EC.element_to_be_clickable(CALL)).click()
            sleep(60)
            not_in = browser.find_elements(NOT_SIGNED_IN[0], NOT_SIGNED_IN[1])

        # max times called = inf? (6 tested)

        # Stay signed in
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable(NEXTBUTTON)).click()
        # Logged into OscarPlus
        # Redirect to Co-Op Postings page

        browser.get("https://www.oscarplusmcmaster.ca/myAccount/eng/coop/postings.htm")
        # case 1: not stale
        try:
            WebDriverWait(browser, 60).until(EC.element_to_be_clickable(TEST)).click()
            return True
        # case 2: stale --> go to sign in link again
        except:
            browser.get('https://www.oscarplusmcmaster.ca/Shibboleth.sso/Login?entityID=https://sso.mcmaster.ca/idp/shibboleth&target=https://www.oscarplusmcmaster.ca/secure/ssoStudent.htm')
            browser.get("https://www.oscarplusmcmaster.ca/myAccount/eng/coop/postings.htm")
            # if we can access oscar then return true, otherwise false
            try:
                WebDriverWait(browser, 60).until(EC.element_to_be_clickable(TEST)).click()
                return True
            except:
                return False
    # unable to sign in for any reason        
    except:
        return False

def main(browser):
    print(f"\nRunning oscarplus.py on {curr}...\n")
    status = signin(browser)
    while status == False:
        browser.delete_all_cookies()
        status = signin(browser)

    WebDriverWait(browser, 60).until(EC.element_to_be_clickable(TEST2)).click()

    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    all = soup.select('td')
    elems = soup.select('td[data-totitle]')
    durationRegex = re.compile(r'^\d{1,}-month$')
    # first group in deadlineRegex matches DATE and second matches TIME (w/o unnecessary spaces) 
    dateRegex = re.compile(r'(\w+\s\d+,\s\d+)', re.I)
    timeRegex = re.compile(r'(\d+:\d+\s\w+)', re.I)
    f = open("coop.txt", "r")
    last_jobs = set()
    for line in f.readlines():
        # add prev seen job after removing \n from end
        last_jobs.add(line.strip())
    f.close()

    i = 0
    j = 0
    message = ''
    updated_last_jobs = set()
    titles = ['Role: ', 'Company: ', 'Division: ']
    # send all new jobs (after last seen)
    # elems[i].get('data-totitle') has role, company, division
    while elems[i].get('data-totitle') not in last_jobs:
        
        message += (titles[i % 3] + (elems[i].get('data-totitle')) + '\n')
        # only want to add role names of new jobs to updated_last_jobs
        if i % 3 == 0:
            updated_last_jobs.add(elems[i].get('data-totitle'))
        # if next entry (in next iteration) is going to be a new role
        if i % 3 == 2:
            duration = durationRegex.search(all[j].getText())
            # search text of each td element till we find duration
            while duration == None:
                j += 1
                duration = durationRegex.search(all[j].getText())
            # after finding duration, get actual text
            duration = duration.group()
            #location, applications, and app deadline right after location
            location = all[j + 1].getText()
            applications = all[j + 2].getText()
            deadline = all[j + 3].getText()
            date = dateRegex.search(deadline).group()
            time = timeRegex.search(deadline).group()
            deadline = date + " " + time
            # put j on non-duration text so it doesn't reuse current in next iteration
            j += 4
            # add duration, location...
            message += f"Duration: {duration}\nLocation: {location}\nApplications: {applications}\nDeadline: {deadline}"
            message += '\n\n'
        i += 1
        # if we have reached the end of jobs in BS obj
        if i == len(elems):
            message = "Unfortunately all of the last seen jobs have been removed and the program cannot judge whether these jobs are new or not\n\n" + message
            break

    if message != '':

        ezgmail.send('oscarplus@googlegroups.com', 'New Summer 2024 OscarPlus Jobs', message)
        print(f"OSCARPLUS Email sent with message\n\n{message}\n\n")
        # set last seen to new IF message is non-empty else keep as is
        with open("coop.txt", "w") as f:
            for job in updated_last_jobs:
                f.write(job + '\n')

    else:
        ezgmail.send('oscarplus@googlegroups.com', 'No New Summer 2024 OscarPlus Jobs', 'Hopefully soon :)')
        print("OSCARPLUS Email sent (no new jobs)\n")

    print("Done.\n")
    print("----------------------------------------------------------")