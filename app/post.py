from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
SHEET_NAME = os.environ.get("SHEET_NAME", "Scores")

# AUTHORIZATION

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "auth", "spreadsheet_credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

# READ SHEET VALUES

client = gspread.authorize(credentials) #> <class 'gspread.client.Client'>
doc = client.open_by_key(DOCUMENT_ID) #> <class 'gspread.models.Spreadsheet'>
sheet = doc.worksheet(SHEET_NAME) #> <class 'gspread.models.Worksheet'>
rows = sheet.get_all_records() #> <class 'list'>

# WRITE SHEET VALUES

email = input("Email: ")
firstname = input("First Name: ")
lastname = input("Last Name: ")
date = input("Date (ex. 2020-01-01): ")
course = input("Course: ")
score = eval(input("Score: "))
rating = eval(input("Course Rating: "))
slope = eval(input("Slope: "))

differential = (score-rating)*(113/slope)

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