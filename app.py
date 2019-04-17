from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scraper

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    data = mongo.db.mars.find_one()
    return render_template("index.html", mars=data)

@app.route("/scrape")
def scrape():
    print("starting web scrape method calls")
    data = mongo.db.mars
    print('database made')
    mars_data = scraper.start_scraper()
    print('finished scraping, now storing in db')
    print(mars_data.values)
    data.update({}, mars_data, upsert=True)
    print("Data successfully scraped")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

