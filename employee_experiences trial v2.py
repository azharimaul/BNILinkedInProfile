from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

# Creating a webdriver instance
driver = webdriver.Chrome("C:/Users/Lenovo/Downloads/Compressed/chromedriver/chromedriver.exe")
# This instance will be used to log into LinkedIn

# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

# waiting for the page to load
time.sleep(5)

# entering username
username = driver.find_element_by_id("username")
# Enter Your Email Address
username.send_keys("insert email here")

# entering password
pword = driver.find_element_by_id("password")
# Enter Your Password
pword.send_keys("insert password here")	

# Clicking on the log in button
# Format (syntax) of writing XPath -->
# //tagname[@attribute='value']
driver.find_element_by_xpath("//button[@type='submit']").click()
# In case of an error, try changing the
# XPath used here.

df = pd.DataFrame()

profile_urls = [line.strip() for line in open('links.txt', 'r')]

for urls in profile_urls: 

    driver.get(urls)
    # this will open the link

    time.sleep(3)
    
    initialScroll = 0
    finalScroll = 1000
    
    driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll}) ")

    try:

        src = driver.page_source
        
        # Now using beautiful soup
        soup = BeautifulSoup(src, 'lxml')

        # Extracting the HTML of the complete introduction box
        # that contains the name, company name, and the location
        intro = soup.find('ul', {'class': 'pvs-list'})

        name = soup.find('div', {'class': 'artdeco-entity-lockup__title'})

        name = ''.join(re.split("[\n\s]{2,}", name.text)).replace("(He/Him)",'').replace("(She/Her)",'')

        experience = intro.find_all('li', {'class': 'pvs-list__paged-list-item'})

        n=0
        for k in experience:
            if k.find('li', {'class': ['pvs-list__paged-list-item','artdeco-list__item','pvs-list__item--line-separated']}):
                company = k.find('span', {'class': 'visually-hidden'}).text
                n=len(k.find_all('li', {'class': ['pvs-list__paged-list-item','artdeco-list__item','pvs-list__item--line-separated']}))
                continue
            else:
                if n>0:
                    if not any(char.isdigit() for char in k.find_all('span', {'class': 'visually-hidden'})[1].text):
                        duration = k.find_all('span', {'class': 'visually-hidden'})[2].text
                    else:
                        duration = (k.find_all('span', {'class': 'visually-hidden'})[1].text)
                    df = df.append({"Nama": name,
                                    "Perusahaan": company,
                                    "Posisi": k.find_all('span', {'class': 'visually-hidden'})[0].text,
                                    "Durasi": duration,
                                    "Link": urls
                                    }, ignore_index=True)
                    n-=1
                else:
                    try:
                        df = df.append({"Nama": name,
                                    "Posisi": k.find_all('span', {'class': 'visually-hidden'})[0].text,
                                    "Perusahaan": k.find_all('span', {'class': 'visually-hidden'})[1].text,
                                    "Durasi": k.find_all('span', {'class': 'visually-hidden'})[2].text,
                                    "Link": urls
                                    }, ignore_index=True)
                    except:
                        continue
    except:
        continue