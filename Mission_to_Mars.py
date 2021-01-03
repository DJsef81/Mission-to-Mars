
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#add this because next cell says chromedrivermanager is not defined
# from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Set the executable path and initialize the chrome browser in splinter (code from the reading, uses a manual path but 
# when i attempted to use the downloadabele chromedriver and installed it into the path, my mac said it didn't trust it.

# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
# browser = Browser('chrome', **executable_path)

# Set the executable path and initialize chrome browser in splinter (alternate way)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#  we'll assign the url and instruct the browser to visit it.

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# set up the HTML parser: Convert the browser html to a soup object and then quit the browser

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')



# The data we're looking for is the content title, which we've specified by saying, "The specific data is in a <div /> 
# with a class of 'content_title'."

#  run this cell. The output should be the HTML containing the content title and anything else nested inside of 
# that <div />.

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
# the get_text(). when used is chained onto .find(), so only the text of the element is returned. 
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ## JPL Space Images Featured Image

# Visit URL
# A new automated browser should open to the featured images webpage.

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Because we want to click the full-size image button, we can go ahead and use the id in our code. 

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the 
# full-size image URL. 

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# We'll use all three of these tags (<figure />, <a />, and <img />) to build the URL to the full-size image. 

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel



# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ## Mars Facts

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

# use pandas .to_html() function to add the DataFrame to web app. 

df.to_html()


browser.quit()
