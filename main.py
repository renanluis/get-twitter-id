#!/usr/bin/python3
import sys
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions

def getTwitterUserID(driver):
    try:
        getUserID = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element("css selector", "div[role=button][aria-label*='@'][data-testid]"))
        user_id = getUserID.get_attribute("data-testid").split("-")[0]
        return user_id
    except exceptions.TimeoutException:
        error = {'status': False}
        error["error"] = "suspended" if isSuspended(driver) else "not_found"
        return error

def isSuspended(driver):
    try:
        getRulesLink = driver.find_element("css selector", "a[href*='twitter-rules'][rel='noopener noreferrer nofollow'][role='link']")
        return getRulesLink.text
    except exceptions.NoSuchElementException:
        return False

def main():
    if(len(sys.argv) < 2):
        return "Uso: "+os.path.basename(__file__)+" usuarioDoTwitter"
    twitterScreenName = sys.argv[1].strip("@")
    url = 'https://twitter.com/'+twitterScreenName
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    twitterID = getTwitterUserID(driver)
    if (type(twitterID) is dict):
        driver.quit()
        match twitterID["error"]:
            case 'suspended':
                return 'Erro: O usuário informado foi suspenso'
            case 'not_found':
                return 'Erro: Usuário não encontrado'
    return "Twitter User's ID: "+ twitterID
    
print(main())