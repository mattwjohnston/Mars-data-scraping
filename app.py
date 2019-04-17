from flask import Flask, render_template
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongodb = PyMongo(app)
path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **path)

@app.route("/")
def index():
    data = mongodb.db.data.find_one()
    return render_template("index.html", listings=data)

@app.route("/scrape")
def scrape():
    try:
        print("starting web scrape method calls")
        data = mongodb.db.data
        print('database made')
        news()
        print("news works")
        mars_data = news(), image(), twitter_weather(), facts(), hemispheres()
        
        data.update({}, mars_data, upsert=True)
        print("Data successfully scraped")
        return redirect("/", code=302)
    except:
        return('data scraping failed')

if __name__ == "__main__":
    app.run(debug=True)


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
    title = slider.find("div", class_='content_title').get_text()
    article = slider.find('div', class_="article_teaser_body").get_text()
    print(title)
    print(article)

def image():
    # featured picture
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    image = browser.find_by_id('full_image')
    image.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()
    html = browser.html
    image_bucket = BeautifulSoup(html, 'html.parser')
    image_location = image_bucket.select_one('figure.lede a img').get("src")
    #add image location to url
    image_url = 'https://www.jpl.nasa.gov'+image_location
    print(image_url)

def twitter_weather():
    #mars weather twitter scrape
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    weather_bucket = BeautifulSoup(html, 'html.parser')
    weather_tweet = weather_bucket.find('div', attrs={"class":"tweet", "data-name":"Mars Weather"})
    weather = weather_tweet.find('p', 'tweet-text').get_text()
    print(weather)

def facts():
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    fact_html = df.to_html()
    print(fact_html)

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