from flask import Flask, render_template
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongodb = PyMongo(app)

@app.route("/")
def index():
    data = mongodb.db.data.find_one()
    return render_template("index.html", listings=data)

@app.route("/scrape")
def scrape():
    try:
        print("starting web scrape method calls")
        data = mongo.db.data
        mars_data = news(), image(), facts(), weather(), hemispheres()
        data.update({}, mars_data, upsert=True)
        print("Data successfully scraped")
        return redirect("/", code=302)
    except:
        return('data scraping failed')

if __name__ == "__main__":
    app.run(debug=True)


def news():
