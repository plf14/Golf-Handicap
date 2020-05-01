from flask import Blueprint, render_template, request

from app.handicap import scores

from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from heapq import nsmallest
from heapq import nlargest

golf_routes = Blueprint("golf_routes", __name__)

@golf_routes.route("/handicap/form")
def handicap_form():
    print("VISITED THE HANDICAP FORM...")
    return render_template("handicap_form.html")

@golf_routes.route("/handicap/results", methods=["GET", "POST"])
def handicap_result():
    print("CALCULATING A HANDICAP...")

    if request.method == "POST":
        print("FORM DATA:", dict(request.form))
        email = request.form["email"]
    elif request.method == "GET":
        print("URL PARAMS:", dict(request.args))
        email = request.args["email"]

    results = scores(email)
    print(results.keys())
    return render_template("handicap_result.html", email=email, results=results) 

    