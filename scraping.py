
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
# add this because next cell says chromedrivermanager is not defined
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
# Set the executable path and initialize chrome browser in splinter (alternate way)
executable_path = {'executable_path': ChromeDriverManager().install()}

# create function to initilize browser, create a data dictionary, and end the webdriver and return the scraped data
def scrape_all():
   # Initiate headless driver for deployment
    browser = Browser('chrome', **executable_path, headless=True)
    # set our news title and paragraph variables     
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": scrape_hd(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Create Function (with "browser" variable we created in parenthesis and indent the code to adhere to function syntax)
def mars_news(browser):
    #  we'll assign the url and instruct the browser to visit it.
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # set up the HTML parser: Convert the browser html to a soup object and then quit the browser

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # The data we're looking for is the content title, which we've specified by saying, "The specific data is in a <div /> 
        # with a class of 'content_title'."

        #  run this cell. The output should be the HTML containing the content title and anything else nested inside of 
        # that <div />.

        # Use the parent element to find the first `a` tag and save it as `news_title`
        # the get_text(). when used is chained onto .find(), so only the text of the element is returned. 
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # news_title (we got rid of this here so we can include it in the return statement of the function)

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        # news_p (we got rid of this here so we can include it in the return statement of the function)
    
    except AttributeError:
        return None, None

    #return statement 
    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):
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

    # Add try/except for error handling
    try:
        # We'll use all three of these tags (<figure />, <a />, and <img />) to build the URL to the full-size image. 
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # img_url_rel
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    # img_url

    return img_url
    
# ## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe    
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None    

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    # use pandas .to_html() function to add the DataFrame to web app. 
    return df.to_html(classes="table table-striped")

# ## Scrape Hemisphere Data

def scrape_hd(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemis_soup = soup(html, 'html.parser')
    hemisphere_image_urls = []
    all_hemis = hemis_soup.select("div.description a")
    try:
        for hemis in all_hemis:
            hemis_link = "https://astrogeology.usgs.gov" + hemis.get("href")
            browser.visit(hemis_link)
            html = browser.html
            one_hemis_soup = soup(html, 'html.parser')
            
            title = one_hemis_soup.select_one("h2.title").text
            image = one_hemis_soup.select_one("div.downloads a").get("href")
            
            hemispheres = {"img_url":image, "title":title}       
            hemisphere_image_urls.append(hemispheres)
        return hemisphere_image_urls
    except:
        return None

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

