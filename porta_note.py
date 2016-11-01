#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Get exact grade from Porta Uni Trier Portal
# Author: Jan Pascal Kunkler (s4jakunk@uni-trier.de)
# Date: 10/12/2016
# REQUIREMENTS:
# - Selenium (pip install selenium)
# - Firefox 45
# - Working Internet Connection
#---------------------
from __future__ import division
from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import getpass

#---------------------

# Porta Uni Trier Login URL
baseurl = "https://porta-system.uni-trier.de/qisserver/pages/cs/sys/portal/hisinoneStartPage.faces?chco=y"

# Ask for Login Credentials
print "Bitte melden Sie sich mit ihrer ZIMK Kennung an.\n"
username = str(raw_input("Benutzer: "))
password = getpass.getpass()

# OPTION to only show final grade.
option = raw_input("\nAlle Noten anzeigen? (j/n): ")

# Define Login form xpaths
xpaths = { 'usernameTxtBox' : "//input[@name='asdf']",
           'passwordTxtBox' : "//input[@name='fdsa']",
           'submitButton' :   "//input[@name='submit']"
         }

# Define driver as mydriver variable
mydriver = webdriver.Firefox()
mydriver.get(baseurl)
mydriver.maximize_window()

#Clear Username TextBox if already allowed "Remember Me"
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).clear()

#Write Username in Username TextBox
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(username)

#Clear Password TextBox if already allowed "Remember Me"
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).clear()

#Write Password in password TextBox
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)

#Submit form
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).submit()

# wait for Mein Studium dropdown menu to appear, then hover it
mein_studium = WebDriverWait(mydriver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@name='repeat:1:notSelectedLink1']")))
ActionChains(mydriver).move_to_element(mein_studium).perform()
mein_studium.click()

# wait for Leistungen menu item to appear, then click it
leistungen = WebDriverWait(mydriver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@name='repeat:1:j_id_3g_1b_e:3:link2']")))
leistungen.click()

# Open up Grades File Tree via Button Click
mydriver.find_element_by_xpath("//button[@name='examsReadonly:overviewAsTreeReadonly:tree:ExamOverviewForPersonTree:0:0:0:0:t2g_0-0-0-0']").click()

# Get Page Conent as html to parse
html = mydriver.page_source

# Quit Firefox Browser
mydriver.quit()

# ------------------------- BEAUTIFUL SOUP PARSING ----------------------------

x = 0
points_sum = 0

# Initialize BS on parsed content
soup = BeautifulSoup(html, "lxml")

# Get the DIV Container with Exam Grades Table
div = soup.find('div', id='examsReadonly:overviewAsTreeReadonly')


for tr in div.find_all('tr')[6:]:
    tds = tr.find_all('td')

    exam = tds[5].text
    exam_uni = exam.encode('utf-8')
    grade = tds[9].text
    points = tds[10].text
    grade_float = float(grade.replace(',', '.'))
    points_float = float(points.replace(',', '.'))

    x += grade_float * points_float
    points_sum += points_float

    if 'j' in option:
        print "- {:60s} {:7s} {:3.1f} {:9s} {:3.1f}".format(exam_uni[0:50], "Note:", grade_float, "Punkte:", points_float)
    else:
        pass

# Calculate exact grade
total = x/points_sum

print "\n"
print "-"*30
print "Gesamtnote:", total
print "-"*30
print "\n"
