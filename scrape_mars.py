from splinter import Browser
from bs4 import BeautifulSoup

# @NOTE: NASA Mars News
import requests

# @NOTE: Initialize chromedriver
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()


    # @NOTE: NASA Mars News
    nasa_mars_news_url ='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(nasa_mars_news_url)
    soup = BeautifulSoup(response.text,'html.parser')
    # results are returned as an iterable list
    news_title  = soup.find('div', class_="content_title").text  ###wl-troubleshoot - pulling wrong text
    news_p  = soup.find('div', class_="image_and_description_container").text   ###wl-troubleshoot - pulling wrong text
    #print(news_p)
    
    # @NOTE: JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    main_url='https://www.jpl.nasa.gov/'
    browser = Browser('chrome', **executable_path, headless=False)
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    #load beautiful soup
    JPL_response = requests.get(JPL_url)
    JPL_soup = BeautifulSoup(JPL_response.text,'html.parser')
    #print(JPL_soup.prettify())
    #get img src
    img_url = JPL_soup.find("img",class_='thumb')
    #print(img_url) ###wl-comment: some reason this works
    #print(img_url['src']) ###wl-comment: some reason this works
    featured_image_url = main_url+img_url['src']
    #print(featured_image_url)
    # Close the browser after scraping
    browser.quit()

    # @NOTE: Mars Weather
    weather_url ='https://twitter.com/marswxreport?lang=en'
    #load beautiful soup
    weather_response = requests.get(weather_url)
    weather_soup = BeautifulSoup(weather_response.text,'html.parser')
    #get tweet text
    weather_text = weather_soup.find_all("div",class_="js-tweet-text-container")
    text = weather_text[0]
    p = text.find('p').text
    remove_link = p.split('pic')
    weather = remove_link[0]
    time_stamp = weather_soup.find("a",class_="tweet-timestamp")
    ###wl - final ###
    mars_weather = str(weather) + " " + '\n' + str(time_stamp['title'])
    #print(mars_weather)

    # @NOTE: Mars Facts
    # @NOTE: Mars Hemispheres

    executable_path = {'executable_path': 'chromedriver.exe'}
    hemispheres_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemispheres_main='https://astrogeology.usgs.gov'
    #load beautiful soup
    hemispheres_response = requests.get(hemispheres_url)
    hemispheres_soup = BeautifulSoup(hemispheres_response.text,'html.parser')
    #get the 4 image links
    hemispheres_links = hemispheres_soup.find_all("div",class_="item")
    hemisphere_image_urls  = []
    for link in hemispheres_links:
        hemispheres_partial_link = link.find("a",class_="itemLink product-item")
        hemispheres_partial_link = hemispheres_partial_link['href']
        full_img_url = hemispheres_main + hemispheres_partial_link
        ##### Open Beautiful Soup on sub-product page #####
        sub_product_response = requests.get(full_img_url)
        sub_product_soup = BeautifulSoup(sub_product_response.text,'html.parser')
        ##### Find sub product image url #####
        sub_product_partial_link = sub_product_soup.find_all("img",class_="wide-image")
        sub_product_full_link = hemispheres_main + sub_product_partial_link[0]['src']
        # @@@print(sub_product_full_link)
        title = link.find("h3").text
        hemisphere_image_urls.append({ "title" : title,"img_url" : sub_product_full_link})
    #print(hemisphere_image_urls)

    # @NOTE: closing
    # Quite the browser after scraping
    browser.quit()

    # @NOTE: Test Data
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url" : featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    # Return results
    return mars_data

#Test

