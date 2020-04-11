"""
Simple browser application for exploring the game companies dataset
"""
import sys
import time
import webbrowser

from multiprocessing import Process
from flask_cors import CORS
from flask import Flask, render_template, request
from .combined_dataset import get_combined_dataset
from .settings import BROWSER_DEBUG, BROWSER_PORT
from .utils import load_gamelist

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

dataset = get_combined_dataset()


@app.route("/analysis", methods=["POST"])
def analysis():

    gamelist_file = request.form.getlist("gamelist_file")[0]
    countries = request.form.getlist("country_dropdown")
    platforms = request.form.getlist("platform_dropdown")

    if not gamelist_file:

        print("set filter->")
        dataset.set_filter(platforms, countries)
        print("get overview data")

    else:
        gamelist = load_gamelist(gamelist_file)
        dataset.set_gamelist_filter(gamelist)
        print("gamelist file")

    data = dataset.get_overview()

    try:
        companies_ratio = data["companies_with_country"] / len(data["companies"])
    except Exception:
        companies_ratio = 0

    return render_template(
        "analysis.html",
        platforms=platforms,
        countries=countries,
        companies_n=len(data["companies"]),
        most_common=data["companies_most_common"],
        company_games=data["company_games"],
        company_countries=data["company_countries"],
        companies_with_country=data["companies_with_country"],
        companies_country_ratio=companies_ratio,
        production_roles=data["production_roles"],
        games_table=data["games_table"],
    )


@app.route("/")
def index():
    return render_template(
        "index.html", platforms=dataset.platforms, countries=dataset.countries
    )


def start_backend():
    try:
        app.run(debug=BROWSER_DEBUG, port=BROWSER_PORT, use_reloader=False)
    except OSError as e:
        print("Cannot start provis server.")
        sys.exit(e)


def start_webbrowser():
    time.sleep(1)
    webbrowser.open("http://localhost:{}".format(BROWSER_PORT))


def start_browser():
    backend_process = Process(target=start_backend)
    backend_process.start()
    start_webbrowser()
