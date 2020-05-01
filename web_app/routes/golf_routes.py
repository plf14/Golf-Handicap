from flask import Blueprint, render_template, request

from app.handicap import scores

golf_routes = Blueprint("golf_routes", __name__)

@golf_routes.route("/handicap/form")
def weather_form():
    print("VISITED THE WEATHER FORM...")
    return render_template("handicap_form.html")

@golf_routes.route("/handicap/results", methods=["GET", "POST"])
def weather_forecast():
    print("GENERATING A WEATHER FORECAST...")

    if request.method == "POST":
        print("FORM DATA:", dict(request.form)) #> {'zip_code': '20057'}
        email = request.form["email"]
    elif request.method == "GET":
        print("URL PARAMS:", dict(request.args))
        email = request.args["email"]

    results = scores(email)
    print(results.keys())
    return render_template("handicap_result.html", email=email, results=results)