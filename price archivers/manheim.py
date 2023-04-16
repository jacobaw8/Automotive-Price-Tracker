import atexit
import time
import datetime
import requests
import csv
import re
import sys
import os
from requests import Session
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


with Session() as s:
    login_data = {"pf.username":"","pf.pass":""}
    s.post("https://api.manheim.com/auth/authorization.oauth2?adaptor=manheim_customer&client_id=qdp6ewmug522t9umyxyqydnx&response_type=code&redirect_uri=https://members.manheim.com/gateway/callback&back_uri=https://www.manheim.com/members/mymanheim/?classic=true",login_data)

chromepath = "/Users/Jacob/Downloads/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Jacob\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
driver = webdriver.Chrome(chromepath, options=options)
driver.get('https://mmr.manheim.com/?WT.svl=m_uni_hdr_buy&country=US&popup=true&source=man')
time.sleep(2)
element = driver.find_element_by_xpath("//*[@id='user_username']")
element.send_keys("")
element = driver.find_element_by_xpath("//*[@id='user_password']")
element.send_keys("")
element.send_keys(Keys.ENTER)

page = requests.get('https://mmr.manheim.com/?WT.svl=m_uni_hdr_buy&country=US&popup=true&source=man')
grab = soup(page.text, "html.parser")
yearSize = Select(driver.find_element_by_xpath("//*[@id='Year']"))
makeSize = Select(driver.find_element_by_xpath("//*[@id='Make']"))
modelSize = Select(driver.find_element_by_xpath("//*[@id='Model']"))
styleSize = Select(driver.find_element_by_xpath("//*[@id='Style']"))

date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

filename = 'files/to_sort/cars_sorted' + '_' + date + '.csv'
f = open(filename, 'w+')

headers = "Year, Make, Model, Style, Completed Code, Price \n"
f.write(headers)

time.sleep(5)

year = 1
make = 1
model = 1
style = 1

with open('last_location.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    rowNum = 1
    for row in reader:
        print(row[0])
        if(rowNum == 1):
            year = int(row[0])
        if(rowNum == 2):
            make = int(row[0])
        if(rowNum == 3):
            model = int(row[0])
        if(rowNum == 4):
            style = int(row[0])
        rowNum = rowNum + 1
print("\nAll together: " + str(year) + " " + str(make) + " " + str(model) + " " + str(style) + " \n")

firstTimeThrough = 1

while year < len(yearSize.options):
    
    selected = Select(driver.find_element_by_xpath("//*[@id='Year']"))
    selected.select_by_index(year)
    time.sleep(1)
    year = year + 1
    if firstTimeThrough == 0:
        make = 1

    while make < len(makeSize.options):

        selected = Select(driver.find_element_by_xpath("//*[@id='Make']"))
        selected.select_by_index(make)
        time.sleep(1)
        make = make + 1
        if firstTimeThrough == 0:
            model = 1

        while model < len(modelSize.options):
                
            selected = Select(driver.find_element_by_xpath("//*[@id='Model']"))
            selected.select_by_index(model)
            time.sleep(0.25)
            model = model + 1
            if firstTimeThrough == 0:
                style = 1

            #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'Style')))
            while style < len(styleSize.options):
                time.sleep(0.75)
                selected = Select(driver.find_element_by_xpath("//*[@id='Style']"))
                selected.select_by_index(style)
                time.sleep(0.75)
                try:
                    price = driver.find_element_by_xpath("//*[@id='root']/div/div/div/div/div[3]/div[3]/div/div[1]/div[2]/div[1]/div/div/div/div[1]/div[1]/div[2]/div")
                    count = 0
                    while (price.text == '- -'):
                        if count >= 10:
                            #driver.refresh()
                            print("shutting down...")
                            loc = open("last_location.csv", "w+")
                            loc.write(str(year-1) + "\n" + str(make-1) + "\n" + str(model-1) + "\n" + str(style) + "\n")
                            loc.close()
                            sys.exit()
                            #time.sleep(5)
                            #count = 0
                            
                        time.sleep(0.5)
                        count += 1
                        print("stuck")
                        price = driver.find_element_by_xpath("//*[@id='root']/div/div/div/div/div[3]/div[3]/div/div[1]/div[2]/div[1]/div/div/div/div[1]/div[1]/div[2]/div")
                    priceText = price.text
                    priceText = priceText.replace(',', '')
                    priceText = priceText.replace('$', '')
                    full_string = (driver.find_element_by_xpath("//*[@data-reactid='201']")).get_attribute('innerHTML') + "," + (driver.find_element_by_xpath("//*[@data-reactid='206']")).get_attribute('innerHTML') + "," + (driver.find_element_by_xpath("//*[@data-reactid='211']")).get_attribute('innerHTML') + "," + (driver.find_element_by_xpath("//*[@data-reactid='216']")).get_attribute('innerHTML') + "," + driver.current_url[83] + driver.current_url[84] + driver.current_url[85] + driver.current_url[86] + driver.current_url[87] + driver.current_url[88] + driver.current_url[89] + driver.current_url[90] + driver.current_url[91] + driver.current_url[92] + driver.current_url[93] + driver.current_url[94] + driver.current_url[95] + driver.current_url[96] + driver.current_url[97] + "," + priceText + "\n"
                    f.write(full_string)
                except NoSuchElementException as exc:
                    print("No Price")
                
                style = style + 1
                firstTimeThrough = 0
              

#                """if(total > 1):
#                    if style == (len(styleSize.options) - 1) and index != 0:
#                        f.write(full_string)  
#                        break
#                    style += 1
#                    total = 0
#                    continue
#                
#                if flag == 1:
#                    time.sleep(3)
#                    flag = 0
#                
#                #try:
#                #    static_string = driver.current_url[83] + driver.current_url[84] + driver.current_url[85] + driver.current_url[86] + driver.current_url[87] + driver.current_url[88] + driver.current_url[89] + driver.current_url[90] + driver.current_url[91] + driver.current_url[92] + driver.current_url[93] + driver.current_url[94] + driver.current_url[95] + driver.current_url[96] + driver.current_url[97]
#                #except IndexError:
#                #    print("Index Error")
#                #    flag = 1
#                #    total += 1
#                #    continue
#                
#                #fullcode = driver.current_url[74] + driver.current_url[75] + driver.current_url[76] + driver.current_url[77] + driver.current_url[78] + driver.current_url[79] + driver.current_url[80] + driver.current_url[81] + driver.current_url[82] + driver.current_url[83] +
#                #(driver.find_element_by_xpath("//*[@data-reactid='211']")).get_attribute('innerHTML') + (driver.find_element_by_xpath("//*[@data-reactid='216']")).get_attribute('innerHTML'))
#                
#                total = 0
#                priceText = price.text
#                if(priceText != "- -"):
#                    currPrice = (int)(re.search(r'\d+', priceText).group())
#                else:
#                    flag = 1
#                    continue
#                if currPrice < lowest:
#                    lowest = currPrice
#                    index = style
#                    full_string = (driver.find_element_by_xpath("//*[@data-reactid='201']")).get_attribute('innerHTML') + ","  + driver.current_url[83] + driver.current_url[84] + driver.current_url[85] + driver.current_url[86] + "," + (driver.find_element_by_xpath("//*[@data-reactid='206']")).get_attribute('innerHTML') + "," + driver.current_url[87] + driver.current_url[88] + driver.current_url[89] + "," + (driver.find_element_by_xpath("//*[@data-reactid='211']")).get_attribute('innerHTML') + "," + driver.current_url[90] + driver.current_url[91] + driver.current_url[92] + driver.current_url[93] + "," + (driver.find_element_by_xpath("//*[@data-reactid='216']")).get_attribute('innerHTML') + "," + driver.current_url[94] + driver.current_url[95] + driver.current_url[96] + driver.current_url[97] + "," + static_string + "," + priceText + "\n"
#                """
                
f.close()

#elem.send_keys(Keys.ENTER)

    #elem = driver.find_element_by_xpath("//*[@id='modelDropdown0']")
    #elem.send_keys(model)
    #elem.send_keys(Keys.ENTER)

    #time.sleep(1)
        
    #driver.find_element_by_link_text('Next').click()
    #elem = driver.find_element_by_xpath("//*[@id='selectedZipCode']")
    #elem.send_keys('29582')
    #elem.send_keys(Keys.ENTER)

    #time.sleep(1)
    #items = grab.findAll('div',{'class':'col-base-10 col-base-offset-1 vertical-spacing-margin-bottom'})

    #time.sleep(1)

    #if ("styles" in driver.current_url):
    #    elem2 = driver.find_element_by_xpath("//*[@id='stylesSection']/div[2]/div[2]/a")
    #    driver.execute_script("arguments[0].click();", elem2)

    #elem3 = driver.find_element_by_xpath("//*[@id='pageContent']/div[3]/div/div[1]/div[2]/div[2]/a")
    #driver.execute_script("arguments[0].click();", elem3)
    #time.sleep(1)
    
    #elem4 = driver.find_element_by_xpath("//*[@id='buyUsedPanel']/div[2]/div/div[3]/a")
    #driver.execute_script("arguments[0].click();", elem4)

        
#f.close()