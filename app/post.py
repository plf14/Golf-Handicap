from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from app import APP_ENV

def post_score(email, firstname, lastname, date, course, score, rating, slope, differential):

    # AUTHORIZATION

    AUTH_SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
        "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
    ]

    load_dotenv()

    DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
    SHEET_NAME = os.environ.get("SHEET_NAME", "Scores")
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, AUTH_SCOPE)

    # READ SHEET VALUES

    client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>
    doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>
    sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
    rows = sheet.get_all_records() #> <class 'list'>

    # WRITE SHEET VALUES

    next_object = {
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
        "date": date,
        "course": course,
        "score": score,
        "rating": rating,
        "slope": slope,
        "differential": differential
    }

    next_row = list(next_object.values())
    next_row_number = len(rows) + 2
    response = sheet.insert_row(next_row, next_row_number)

if __name__ == "__main__":

    if APP_ENV == "development":
        email = input("Email: ")
        firstname = input("First Name: ")
        lastname = input("Last Name: ")
        date = input("Date (YYYY-MM-DD): ")
        course = input("Course: ")
        score = eval(input("Score: "))
        rating = eval(input("Course Rating: "))
        slope = eval(input("Slope: "))

        differential = (score-rating)*(113/slope)

        post_score(email,firstname, lastname, date, course, score, rating, slope, differential)