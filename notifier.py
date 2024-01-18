from datetime import datetime
import oscarplus
import ssc
import mosaic_ta
import mosaic_swp
from selenium import webdriver

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
browser = webdriver.Chrome(r"/usr/lib/chromium-browser/chromedriver", chrome_options = options)

def main():
    # once we sign in in oscarplus main, the program should not need to call again (for ssc)
    oscarplus.main(browser)
    ssc.main(browser)
    mosaic_ta.main(browser)
    # mosaic_swp.main(browser)

main()
browser.quit()
