import sys
import time
import webbrowser
from multiprocessing import Process
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, render_template, request

from .combined_dataset import CompanyDataset

"""
Simple browser application for exploring the game companies dataset
"""

DEBUG = True
PORT = 8228

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

dataset = CompanyDataset()

@app.route("/analysis", methods=["POST"])
def analysis():
    countries = request.form.getlist("country_dropdown")    
    platforms = request.form.getlist("platform_dropdown")
    print("set filter->")
    dataset.set_filter(platforms, countries)
    print(list(dataset.companies.most_common(30)))
    return render_template(
        "analysis.html", 
        platforms=platforms, 
        countries=countries,
        companies_n=len(dataset.companies),
        most_common=list(dataset.companies.most_common(30)),
        company_games=dict(dataset.companies_games),
        company_countries=list(dataset.countries_accumulated.most_common(200)),
        companies_with_country=dataset.companies_with_country
        )


@app.route("/")
def index():
    return render_template("index.html", platforms=dataset.platforms, countries=dataset.countries)


def start_backend():
    try:
        app.run(debug=DEBUG, port=PORT, use_reloader=False)
    except OSError as e:
        print("Cannot start provis server.")
        sys.exit(1)  


def start_webbrowser():
    time.sleep(1)
    webbrowser.open("http://localhost:{}".format(PORT))        

def start_browser():
    backend_process = Process(target=start_backend)
    backend_process.start()
    start_webbrowser()

