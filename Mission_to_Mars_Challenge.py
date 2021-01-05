#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# The script we're building is designed to scrape the most recent data—that means that each time we run the script, 
# we'll pull the newest data available.


# In[27]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#add this because next cell says chromedrivermanager is not defined
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time 


# In[6]:


# Set the executable path and initialize the chrome browser in splinter (code from the reading, uses a manual path but 
# when i attempted to use the downloadabele chromedriver and installed it into the path, my mac said it didn't trust it.

# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path)

# Set the executable path and initialize chrome browser in splinter (alternate way)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[7]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[8]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[9]:


slide_elem.find("div", class_='content_title')


# In[10]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[11]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[12]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[13]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[14]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[15]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[16]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[17]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[18]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[19]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[20]:


df.to_html()


# ### Mars Weather

# In[21]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[22]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[23]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[24]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[32]:


# set up the HTML parser:
html=browser.html
hemis_soup=soup(html,'html.parser')


# In[33]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
all_hemis = hemis_soup.select("div.description a")

def scrape_hd():
    for hemis in all_hemis:
        hemis_link = "https://astrogeology.usgs.gov" + hemis.get("href")
        browser.visit(hemis_link)
        html = browser.html
        one_hemis_soup = soup(html, 'html.parser')
        
        title = one_hemis_soup.select_one("h2.title").text
        image = one_hemis_soup.select_one("div.downloads a").get("href")
        
        dic = {"img_url":image, "title":title}       
        hemisphere_image_urls.append(dic)
    return hemisphere_image_urls
scrape_hd()


# In[34]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[35]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




