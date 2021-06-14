"""
Script contains a bot that systematically screenshots all the cases.
Author: Bram Löbker
Version: 1.0.0 (07-14-2021)
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pyautogui
import time


def main():
    """
    Opens Chromedriver, selects the 'ratio1' radiobutton and then systematically goes through all cases and then takes a screenshot.
    """

    PATH = "chromedriver.exe"

    driver = webdriver.Chrome(PATH)
    driver.get("http://127.0.0.1:5000/")

    counter=0
    while counter <240:

        print(counter, "/ 240")
        print('Wait')
        time.sleep(2)
        print("Done Waiting")
        element = driver.find_element_by_id("cases")
        drp = Select(element)
        drp.select_by_index(counter)

        vistype = driver.find_element_by_id("ratio1")
        vistype.click()

        sub = driver.find_element_by_id("submit")
        sub.click()
        counter+=1
        time.sleep(1)
        myScreenshot = pyautogui.screenshot()
        case=driver.find_element_by_id('current_case').text
        print(case)
        path="Dataset\\Compleet\\"+case+".png"
        myScreenshot.save(path)

main()