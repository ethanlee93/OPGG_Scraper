from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from time import sleep
import re

TIME_WASTER_MULTIPLIER = 1

class OPGG_Scraper:
    def __init__(self, subdomain, username, division):
        self.username = username
        self.division = division
        self.subdomain = subdomain
        self.hours = self.minutes = self.seconds = 0

    def load(self):
        print("PLEASE WAIT FOR BROWSER LOAD WEBSITE.\n"
              "DO NOT CLICK ON ANY BUTTONS ON THE WEBSITE.\n"
              "For best performance, keep the browser open as the active window.")
        URL = "https://" + subdomain + "op.gg/summoners/" + division + "/" + username
        useragent = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
        }
        geckoPath = r'C:\Users\Ethan_\PycharmProjects\OPGG_Scraper\venv\WebDriverManager\gecko\v0.29.0\geckodriver-v0.30.0-win64\geckodriver.exe'
        driver = webdriver.Firefox(service=Service(geckoPath))
        driver.get(URL)
        self.update(self, driver)
        while True:
            decision = input("What would you like to do? Type in number.\n"
                             "1: Find total play time\n"
                             "2: Find ranked solo play time\n"
                             "3: Find ranked flex play time\n"
                             "4: Quit\n"
                             "(NOT IMPLEMENTED YET) 5: Change username & region\n").lower()
            if decision == "1":
                self.resetTime(self)
                self.getTotalGameTime(self, driver)
            elif decision == "2":
                self.resetTime(self)
                self.getRankedSoloTime(self, driver)
            elif decision == "3":
                self.resetTime(self)
                self.getRankedFlexTime(self, driver)
            elif decision == "quit" or decision == "4":
                driver.quit()
                return
            else:
                print("Invalid input. Try again. Input should be formatted as one digit.")

            done = input("Are you done? (Y/N) ").lower()
            if done == "y":
                print("Window will close automatically.")
                driver.quit()
                return

    def resetTime(self):
        self.hours = self.minutes = self.seconds = 0

    def showMore(self, driver):
        print("LOADING YOUR MATCH HISTORY. PLEASE WAIT.")
        while len(driver.find_elements(By.CLASS_NAME, 'no-data')) == 0:
            driver.find_element(By.CSS_SELECTOR, 'button.more').click()
        print("NO MORE PAGES TO LOAD")
        driver.execute_script("window.scrollTo(0, 1080);")


    def update(self, driver):
        print("AUTO-UPDATE INITIATED.")
        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/button').click()
            # Even if update cannot be pushed, find_element will return valid element,
            # .click() will just return None object.
        except:
            # Should happen if URL is wrong or has isn't a profile with an update button.
            print("UPDATE BUTTON COULD NOT BE FOUND. (Error code 4)")
        while driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/button').get_attribute("disabled") is None:
            pass
        print("UPDATE COMPLETED.")

    def getTotalGameTime(self, driver):
        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/div[1]/ul/li[1]/button').click()
            print("ALL BUTTON PRESSED")
        except:
            print("ERROR, STOP PROGRAM (Error code 1)")
            return
        sleep(2 * TIME_WASTER_MULTIPLIER)
        self.getGameTime(self, driver)

    def getRankedFlexTime(self, driver):
        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/div[1]/ul/li[3]/button').click()
            print("RANKED FLEX BUTTON PRESSED")
        except:
            print("ERROR, STOP PROGRAM (Error code 3)")
            return

        sleep(2 * TIME_WASTER_MULTIPLIER)
        self.getGameTime(self, driver)

    def getRankedSoloTime(self, driver):
        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/div[1]/ul/li[2]/button').click()
            print("RANKED SOLO BUTTON PRESSED")
        except:
            print("ERROR, STOP PROGRAM (Error code 2)")
            return

        sleep(2 * TIME_WASTER_MULTIPLIER)
        self.getGameTime(self, driver)

    def getGameTime(self, driver):
        print("\nYou should have the browser open as the active window if your OP.GG has a "
              "lengthy match history.")
        self.showMore(self, driver)
        gameTimes = driver.find_elements(By.CLASS_NAME, 'game-length')
        if len(gameTimes) == 0:
            print("There are no games here to count.")
            return
        for element in gameTimes:
            self.timeAdder(self, element.text)
        self.printTime(self)

    def timeAdder(self, string):
        match = re.findall('([1-9]h )?([1-5]?[0-9]m )?([1-5]?[0-9]s)', string)
        arr = match[0]
        if len(arr[2]) != 0:
            self.seconds += int(arr[2][:len(arr[2]) - 1])
            if self.seconds > 59:
                self.minutes += 1
                self.seconds -= 60
        if len(arr[1]) != 0:
            self.minutes += int(arr[1][:len(arr[1]) - 2])
            if self.minutes > 59:
                self.hours += 1
                self.minutes -= 60
        if len(arr[0]) != 0:
            self.hours += int(arr[0][:len(arr[0]) - 2])

    def printTime(self):
        print("Hours: " + str(self.hours) + "\nMinutes: " + str(self.minutes) + "\nSeconds: " + str(self.seconds))


if __name__ == "__main__":
    username = division = subdomain = ""

    while True:
        username = input("\nENTER YOUR USERNAME (not case sensitive): ").lower()
        if len(username) == 0:
            print("You cannot have a blank username!")
        else:
            break

    while True:
        division = input("\nENTER YOUR REGION (e.g. NA, EUSE, KR): ").lower()
        if len(division) == 0:
            print("You cannot have a blank region!")
        else:
            break

    division = division.lower()
    if division != "KR":
        subdomain = division + "."

    myScraper = OPGG_Scraper
    myScraper.__init__(myScraper, subdomain, username, division)
    myScraper.load(myScraper)
