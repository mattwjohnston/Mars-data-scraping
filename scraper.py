from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

def start_scraper():
    #I put all the methods before the visualization to avoid passing around any variables
    def news():
        # news article
        url = 'https://mars.nasa.gov/news/'
        print("got to method")
        browser.visit(url)
        print("got past browser")
        html = browser.html
        news_bucket = BeautifulSoup(html, 'html.parser')

        slider = news_bucket.select_one('ul.item_list li.slide')
        #found these tags by sifting through thee html
        slider.find("div", class_='content_title')
        list_date = slider.find("div", class_='list_date').get_text()
        title = slider.find("div", class_='content_title').get_text()
        '''titlelink=slider.find("div", class_='content_title')[0].find_children("a", recursive=False)
        #link = titlelink.descendents.
        print(titlelink)
        link2 = link.get_link()
        print(link2)
        link = link.descendents.find_all('href')'''
        article = slider.find('div', class_="article_teaser_body").get_text()
        return [title, article, list_date]

    def image():
        # featured picture
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        image = browser.find_by_id('full_image')
        image.first.click()
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info = browser.find_link_by_partial_text('more info')
        more_info.first.click()
        html = browser.html
        image_bucket = BeautifulSoup(html, 'html.parser')
        image_location = image_bucket.select_one('figure.lede a img').get("src")
        #add image location to url
        image_url = 'https://www.jpl.nasa.gov'+image_location
        print(image_url)
        return(image_url)

    def twitter_weather():
        #mars weather twitter scrape
        url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        html = browser.html
        weather_bucket = BeautifulSoup(html, 'html.parser')
        weather_tweet = weather_bucket.find('div', attrs={"class":"tweet", "data-name":"Mars Weather"})
        weather = weather_tweet.find('p', 'tweet-text').get_text()
        print(weather)
        return(weather)

    def facts():
        df = pd.read_html('http://space-facts.com/mars/')[0]
        df.columns=['description', 'value']
        df.set_index('description', inplace=True)
        fact_html = df.to_html()
        print(fact_html)
        return(fact_html)

    def hemispheres():
        ## Mars hemispheres
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        links = browser.find_by_css("a.product-item h3")

        hemisphere_hrefs = []
        for i in range(len(links)):
            browser.find_by_css("a.product-item h3")[i].click()
            image_preview = browser.find_link_by_text('Sample').first
            hemisphere_image = {}
            hemisphere_image['url'] = image_preview['href']
            hemisphere_image['title'] = browser.find_by_css("h2.title").text
            hemisphere_hrefs.append(hemisphere_image)
            browser.back()
        print(hemisphere_hrefs)
        return(hemisphere_hrefs)

    path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **path)
    news_data = news()
    data = {
        'news_title': news_data[0],
        'news_article': news_data[1],
        'news_post_date': news_data[2],
        'image':image(),
        'weather':twitter_weather(),
        'facts':facts(),
        'hemispheres':hemispheres(),
        "last_modified": dt.datetime.now()
    }
    return data
