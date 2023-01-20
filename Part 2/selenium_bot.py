#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 19:00:06 2023

@author: carlosgarcia
"""
#%% Tools
from selenium.webdriver.chromium.service import ChromiumService
from selenium import webdriver
import time

#%% Setting Up Driver
chrome_service = ChromiumService(executable_path="Part 2/chromedriver")
driver = webdriver.Chrome(service=chrome_service)
kaggle_competition_homepage = "https://www.kaggle.com/competitions?listOption=completed&sortOption=recentlyClosed&prestigeFilter=money"
driver.get(kaggle_competition_homepage)
time.sleep(2)
driver.quit()
