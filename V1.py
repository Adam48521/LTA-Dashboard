# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:42:22 2023

@author: adaml
"""
# %%
import sys
import datetime
from selenium.webdriver.support.ui import Select
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt

tic = time.perf_counter()

def data_download():
    # Chromedriver
    options = webdriver.ChromeOptions()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get("https://competitions.lta.org.uk/ranking/category.aspx?id=31251&category=4544")
    driver.find_element(By.XPATH, value='/html/body/div/div/div/main/form/div[1]/button[1]').click()
    
    
    
    r = driver.find_element(By.NAME, value = 'ctl00$ctl00$ctl00$cphPage$cphPage$cphPage$dlPublication')#.get_attribute('value').split('\n')
    d=Select(r)
    
    date=[]
    date_value=[]
    
    #Extract dates and web value from link
    for opt in d.options:
        print(opt.text,opt.get_attribute('value')+"\n" )
        date.append(opt.text)
        date_value.append(opt.get_attribute('value'))
    
    
    #############################
    
    rank = []
    sing=[]
    doub=[]
    tourn=[]
    tourn_used=[]
    #tot_pts=[]
    points=[]
    
    for i in date_value:
    
        driver.get("https://competitions.lta.org.uk/ranking/player.aspx?id=%s&player=4541751" % i) #Navigate to each calender week
        
        #Extract table and tidy
        df = pd.read_html(driver.page_source)[0]
        df.columns = df.iloc[0]
        df.drop([0],inplace=True)
        df.dropna(axis=1, how='all',inplace=True)
        #Identify rank out of the table and append to list
        rank.append(df.iloc[0]['Rank'])
       # print(df.iloc[0]['Rank'])
        sing.append(df.iloc[0]['Singles Points'])
        doub.append(df.iloc[0]['Doubles points'])
        tourn.append(df.iloc[0]['Tournaments'])
        tourn_used.append(df.iloc[0]['Tournaments used for this calculation'])
        points.append(df.iloc[0]['Total points'])
    
    
    #Append lists to dataframe
    df = pd.DataFrame(
        {'Date': date,
         'Rank': rank,
         'Singles Points': sing,
         'Doubles Points': doub,
         'Tournaments': tourn,
         'Tournaments used': tourn_used,
         'Total Points':points
        })
    
    #Convert date format from object WW-YYY to datetime
    df['Date'] = df['Date'] + "-1" #Start of the week
    df["Date"] = pd.to_datetime(df["Date"],format='%U-%Y-%w')
    df.sort_values(by='Date', ascending = True, inplace = True) #Sort for date being ascending

    #Export data to csv
    df.to_csv(r'C:\Users\alain\Documents\Python Scripts\LTA-Dashboard/data.csv')
    driver.close()

    print('New data successfully downloaded')
    return(df)

#Read existing data
#df = pd.read_csv(r'C:\Users\alain\Documents\Python Scripts\LTA-Dashboard/data.csv')

#Run Fresh Download
df = data_download()





df = df.astype({"Rank": int, "Singles Points": int,"Doubles Points": int, "Tournaments": int, "Tournaments used": int, "Total Points": int})

#print(df.dtypes)

# %%
Ranking=df[['Date','Rank']]
Ranking.plot(x='Date',y='Rank')
plt.show()

toc = time.perf_counter()

print(f"Completed the script in {toc - tic:0.2f} seconds")
