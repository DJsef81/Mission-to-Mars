# Mission-to-Mars
Module 10

# Purpose of Analysis

Robin wants to gather all the information about the Mission to Mars from all over the web, and display it in a central location, without spending all of her free time gathering it manually. 

To do this she wanted to build a web application that will scrape new data and add collect it with a push of a button. 

Before she could do this she needed to 
 - understand how websites are built 
 - to write a python script that can navigate the webpages to collect the right information. 

She needs a place to store the information, a noSQL database, MongoDB - because internet data is "messy" and no professionals like messy presentations. 

To put all that together in a web application of her own, we used Flask, a web framework, that allows her to create the web app with python, then customize it with HTML and CSS.

After we did all this, we also scraped the 4 Mars hemisphere images off https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars, and made them available on our wesite as well. 

## Software 
- Python 3.7.7
- selenium-3.141.0 
- splinter-0.14.0
- webdriver_manager-3.2.2
- bs4-0.0.1
- pymongo-3.11.2
- Bootstrap 3
