
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import *
from bs4 import BeautifulSoup
from pathlib import Path
import os
from datetime import datetime,time,timedelta
from time import sleep
import sys

def click_space(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.SPACE)
    actions.perform()

def wait(startTime, offsetMinutes, offsetSeconds):
    #wait until Targettime, altered by the offset
    intTargetHour = int(startTime.split(":")[0])
    intTargetMinute = int(startTime.split(":")[1])
    targetTime = datetime.combine(datetime.today(), time(intTargetHour, intTargetMinute)) + timedelta(minutes=float(offsetMinutes),seconds=float(offsetSeconds))
    while targetTime > datetime.now(): # you can add here any additional variable to break loop if necessary
        sleep(0.5)

if __name__== "__main__":
   
    #Reading skript-parameters
    if len(sys.argv)==3:
        movieURL=sys.argv[1]
        synchTime = sys.argv[2]
    else:
        sys.exit("Keine Parameter übergeben, Programmabbruch!")

    #Webdriver Configuration
    # Remember to copy the Driver.exe (for firefox geckodriver.exe) to the same folder as python.exe
    # Run this script once with Chrome, login and select the "remember me" function so you don't have to login again and again
    options = Options()
    options.add_argument("user-data-dir=/tmp/tarun")
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(movieURL)
    
    #Wait until the video is loaded and determine the movie-state
    #Depending on the state the movie is started
    sleep(5)
    try:
        #Movie has not yet been started before --> starttime = 0s
        playButton = browser.find_element_by_xpath("//button[@tabindex='0' and not(@aria-label)]")
        playButton.click()
    except NoSuchElementException:
        try:
            #Movie has been started and is running at the moment           
            pauseButton=browser.find_element_by_xpath("//button[@aria-label='Pause']")
        except:
            try:                
                #Movie has been started and is paused at the moment
                playButton=browser.find_element_by_xpath("//button[@aria-label='Abspielen']")
                click_space(browser)
            except:
                sys.exit("Play-Button not found, abort!")

    # Another wait function, the movie should be running at the moment
    sleep(0.5)       
    try:
        pauseButton=browser.find_element_by_xpath("//button[@aria-label='Pause']")    
       
    except:
        sys.exit("Pause-Button not found, abort!")



    #Reading the timebar after waiting another few seconds
    sleep(1.5)  
    
    #Pausing the movie
    click_space(browser) 
    

    pageSource = browser.page_source
    PageResponse = BeautifulSoup(pageSource, features="html.parser")
    timeline = PageResponse.find_all('div',{"aria-label" : "Zeitleiste durchsuchen"})
    try:
         timeline=browser.find_element_by_xpath("//*[@aria-label='Zeitleiste durchsuchen']")
    except NoSuchElementException:
        try:            
            sleep(1.5)
            timeline=browser.find_element_by_xpath("//*[@aria-label='Zeitleiste durchsuchen']")
        except:
            sys.exit("time bar not found, abort!")
    
    timePosition = timeline.get_attribute("aria-valuetext")

    #pause the movie
    click_space(browser)

    # read current time from time bar and process the received information
    timePosition = timeline.get_attribute("aria-valuetext")
    
    elapsedMinutes = timePosition.split(" ")[0].split(":")[0]
    elapsedSeconds = timePosition.split(" ")[0].split(":")[1]

    #wait until the synchronization time
    wait(synchTime,elapsedMinutes,elapsedSeconds)

    #start the video
    click_space(browser)

    print("Enjoy!")
