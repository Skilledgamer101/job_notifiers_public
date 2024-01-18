from datetime import datetime
import oscarplus
import ssc
import mosaic_ta
import mosaic_swp
from selenium import webdriver
import pyinputplus as pyp

curr = datetime.now()
print(f"\nRunning notifier.py on {curr}...\n")

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument("force-device-scale-factor=0.75")
options.add_argument("high-dpi-support=0.75")
# for pi: /usr/lib/chromium-browser/chromedriver
# for Windows: C:\Windows\System32\chromedriver.exe

path = pyp.inputFilepath("Please enter the full path to chromedriver:\n")
path.encode('unicode_escape')
email = pyp.inputEmail("Please enter your McMaster email address:\n")
password = pyp.inputPassword("Please enter your McMaster password:\n")
recipient = pyp.inputEmail("Please enter the email address you want to send the jobs to:\n")

browser = webdriver.Chrome(path, chrome_options = options)

def main():
    oscarplus.main(browser, email, password, recipient)
    ssc.main(browser, recipient)
    mosaic_ta.main(browser, email, password, recipient)
    # mosaic_swp.main(browser, recipient)

main()
browser.quit()
