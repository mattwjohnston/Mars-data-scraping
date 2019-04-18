from flask import Flask, render_template, redirect
import requests
import time
import scraper
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    print("trying to find one")
    mars_info = mongo.db.mars_app.find_one()
    print("past the finding point")

    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():
    print("starting web scrape method calls")
    mars_info = mongo.db.mars_app
    print('database made')
    mars_data = {}
    mars_data = scraper.start_scraper()
    print(f'MARS DATA{mars_data}')
    print('finished scraping, now storing in db')
    mars_info.update({}, mars_data, upsert=True)
    print("Data successfully scraped")
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
