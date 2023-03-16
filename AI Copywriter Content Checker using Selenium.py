#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing all the important libraries
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re as re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[ ]:


#initialise the web driver
browser = webdriver.Chrome(ChromeDriverManager().install())


# In[ ]:


#importing the input data and converting it into a list
scorebuddy = pd.read_csv(r"your file path goes here")
blog_urls=scorebuddy["Blog_URLs"].tolist()
blog_headline=scorebuddy["Blog_Headline"].tolist()


# In[ ]:


# Lists that we will iterate to
Blog_URL = []
Blog_Headline = []
Blog_Texts = []
Real_Percent = []
Fake_Percent = []


# In[ ]:


#defining a function to pre-process and clean the textual data
def cleantext(x):
    text=re.sub("\n"," ",x)
    text=text.split()
    text=" ".join(text)
    return(text)


# In[ ]:


#looping through the data 
for url in range(len(blog_urls)):
    browser.get(blog_urls[url])
    time.sleep(5)
    
    try:
        blog_text=browser.find_element(By.XPATH,"//span[@id='hs_cos_wrapper_post_body']").text
    except:
        pass
    cleaned_text = cleantext(blog_text)
    
    """
    here we are spliting the data because in a free version we are only be able to anlayse the textual data
    lenght of around 2000 tokens.
    """
    
    if len(cleaned_text.split())>2000:
        Blog_Texts_1= cleaned_text.split()[:2000]
        Blog_Texts_2= cleaned_text.split()[2000:]
        
        list= [Blog_Texts_1, Blog_Texts_2 ]
        
        for i in list:
            #website from where we are going to fetch the information
            browser.get("https://openai-openai-detector.hf.space/")
            Blog_Texts.append(i)
            enter_text = browser.find_element(By.XPATH,"//textarea[@id='textbox']")
            enter_text.send_keys(i)
            time.sleep(4)
            
            Blog_URL.append(blog_urls[url])
            Blog_Headline.append(blog_headline[url])
            
            try:
                real_per=browser.find_element(By.XPATH,"//td[@id='real-percentage']").text
                Real_Percent.append(real_per)
            except:
                Real_Percent.append("error")
    
            try:
                fake_per=browser.find_element(By.XPATH,"//td[@id='fake-percentage']").text
                Fake_Percent.append(fake_per)
            except:
                Fake_Percent.append("error")
        
    else:
        Blog_URL.append(blog_urls[url])
        Blog_Headline.append(blog_headline[url])
        
        Blog_Texts.append(blog_text)
        
        browser.get("https://openai-openai-detector.hf.space/")
        enter_text = browser.find_element(By.XPATH,"//textarea[@id='textbox']")
        enter_text.send_keys(cleaned_text)
        time.sleep(4)
        
        try:
            real_per=browser.find_element(By.XPATH,"//td[@id='real-percentage']").text
            Real_Percent.append(real_per)
        except:
            Real_Percent.append("error")
    
        try:
            fake_per=browser.find_element(By.XPATH,"//td[@id='fake-percentage']").text
            Fake_Percent.append(fake_per)
        except:
            Fake_Percent.append("error")
        
    
    print(blog_urls[url])
    
    


# In[ ]:


#creating a dataframe to store the outputs
data = {
    "Blog_URL":Blog_URL,
    "Blog_Headline": Blog_Headline,
    "Blog_Texts": Blog_Texts,
    "Real_Percent": Real_Percent,
    "Fake_Percent": Fake_Percent
}

df = pd.DataFrame(data)


# In[ ]:


#displaying the head of the dataframe
df.head(30)


# In[ ]:


#writing the dataframe to local machine
df.to_csv(r'your desired storage path goes here', index=False)

