#!/usr/bin/env python
# coding: utf-8

# In[1]:


import base64
import getpass
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# In[2]:


# Access the chrome webdriver and open the browser to the microsoft login page
# Note: Chrome instance DOES know it is being automated
driver = webdriver.Chrome('./chromedriver')
driver.get("https://timesheet.amsoftware.com/EApplications/esecurity/Login.jsp")


# In[3]:


# Attempt to gather the username and password from a file
if os.path.exists("creds.dat"):
    try:
        # Attempts to gather username/password from file, otherwise requires user input 
        credentials = open("creds.dat", "rb+") 
        
        for line in credentials:
            # Simple decrypt of credentials
            cred = base64.b64decode(line).decode()
            
            username = cred.split(":")[0]
            password = cred.split(":")[1]
    except:
        # Once the else functionality is made into a function, can use that function here
        print("broke")
else:
    # If no file exists, manually gather username/password
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    with open("creds.dat","wb") as file:
        fullCred = username + ':' + password
        file.write(base64.b64encode(fullCred.encode()))


# In[4]:


# Fills in credentials and logs in
userField = driver.find_element_by_name("UserId")
passField = driver.find_element_by_name("Password")

userField.send_keys(username)
passField.send_keys(password)

driver.find_element_by_class_name('standardbutton').click()


# In[5]:


# Navigate to TimeSheet menu
driver.get("https://timesheet.amsoftware.com/EApplications/etimesheet/TimeSheetMenu.jsp")


# In[6]:


# Insert the data for the next Saturday and create a new timesheet
dateField = driver.find_element_by_name("WEDate")

nextSunday = datetime.date.today()

# Finds the closest Saturday
while nextSunday.weekday() != 5:
    nextSunday += datetime.timedelta(1)

# String prep for input
nextSunday = '{0}/{1}/{2}'.format(nextSunday.month, nextSunday.day, nextSunday.year)
    
dateField.send_keys(str(nextSunday))
    
buttons = driver.find_elements_by_class_name('StandardButton')
buttons[1].click()


# In[7]:


# Contract Information
jobField = driver.find_element_by_name('ContractNumber1')
jobField.send_keys('10325P0001')

driver.find_element_by_xpath('//*[@id="ActivityCode1"]').click()
driver.find_element_by_xpath('//*[@id="ActivityCode1"]/option[2]').click()


# In[8]:


time = driver.find_elements_by_class_name('input5')[0]

# Shitty way of changing the entire chunk of values
driver.execute_script("document.getElementById('HoursMon1').setAttribute('value', '8')")
driver.execute_script("document.getElementById('HoursTue1').setAttribute('value', '8')")
driver.execute_script("document.getElementById('HoursWed1').setAttribute('value', '8')")
driver.execute_script("document.getElementById('HoursThu1').setAttribute('value', '8')")
driver.execute_script("document.getElementById('HoursFri1').setAttribute('value', '8')")

# Submit
#driver.execute_script("document.getElementById('HoursFri1').setAttribute('value', '8')")

