from flask import Blueprint, render_template, request, flash, redirect

from app.handicap import scores
from app.post import post_score

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

@golf_routes.route("/post")
def new_user():
    print("VISITED THE POST SCORE PAGE...")
    # return "Sign Up for our Product! (TODO)"
    return render_template("post.html")

@golf_routes.route("/post/done", methods=["POST"])
def create_user():
    print("ENTERING SCORE...")
    print("FORM DATA:", dict(request.form)) #> {'full_name': 'Example User', 'email_address': 'me@example.com', 'country': 'US'}
    user = dict(request.form)
    differential = (eval(user["score"])-eval(user["rating"]))*(113/eval(user["slope"]))
    post_score(user["email_address"], user["first_name"], user["last_name"], user["date"], user["course"], user["score"], user["rating"], user["slope"], differential)
    email=user["email_address"]
    results = scores(email)
    flash(f"Your score of {user['score']} at {user['course']} on {user['date']} was entered successfully!", "success") #success = green color alert
    return render_template("handicap_result.html", email=email, results=results)