# web_app/routes/home_routes.py

from flask import Blueprint, render_template, redirect, request, flash

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    print("VISITED THE HOME PAGE")
    #return "Welcome Home (TODO)"
    return render_template("home.html")


@home_routes.route("/about")
def about():
    print("VISITED THE ABOUT PAGE")
    #return "About Me (TODO)"
    return render_template("about.html")
    

@home_routes.route("/users/new")
def new_user():
    print("VISITED THE REGISTRATION PAGE")
    # return "Sign Up for our Product! (TODO)"
    return render_template("new_user_form.html")

@home_routes.route("/users/create", methods=["POST"])
def create_user():
    print("CREATING A NEW USER...")
    print("FORM DATA:", dict(request.form)) #> {'full_name': 'Example User', 'email_address': 'me@example.com', 'country': 'US'}
    user = dict(request.form)
    # todo: store in a database or google sheet!
    #flash(f"User '{user['full_name']}' created successfully!", "success")
    flash(f"User '{user['full_name']}' created successfully!", "success") #success = green color alert
    return redirect("/")

