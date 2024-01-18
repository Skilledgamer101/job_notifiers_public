# InternAlert
This program notifies the user if there are new job postings or not. It can be set to run automatically using Windows Task Scheduler (Windows built-in application) or similar software.

### Disclaimers: 
1. This code works only for the McMaster official co-op/SSC/Mosaic job board website [(OscarPlus)](https://www.oscarplusmcmaster.ca) as of January 18, 2024. 
2. You will require Google Chrome Version 117 as it is compatible with the chromedriver in this repository. Newer versions of Chrome may be supported with newer chromedrivers, which can be found [here](https://chromedriver.chromium.org/downloads/version-selection).
3. You need to have at least one saved search in the co-op board or the Student Success Centre. This program looks for new jobs in the top-most saved search (i.e., the most recent saved search made).
4. You need to have 2FA enabled on your McMaster account with an option to call your phone. 

## How to Use

### 1. Download all of the files in this folder to a single folder

### 2. Install Required Dependencies
`pip install selenium==2.53.6 BeautifulSoup4==4.12.2 ezgmail==2022.10.10 lxml==4.9.3 pyinputplus`

### 3. Set up EZGmail
Please follow the instructions on this [link](https://pypi.org/project/EZGmail/). Make sure the `credentials.json` and `token.json` files are in the same folder as all of the files in this project.

### Run the python file `notifier.py`
This program will search for jobs from OscarPlus, SSC, Mosaic SWP and Mosaic TA.
The program will ask you to enter your:
1. Full path to the chromerdriver ('path-to-where-you-downloaded-this-repository/chromedriver.exe')
1. McMaster Email Address
2. Password
3. Email address to which you want new jobs to be sent

Note: The empty text files in this folder are used to store the most recently 'seen' jobs. The program can use these to evaluate whether future jobs are newer or not.
