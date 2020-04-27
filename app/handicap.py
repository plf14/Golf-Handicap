
from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from heapq import nsmallest

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

email = input("What is your email?  ")
relevant_rows = []
for row in rows:
    if email == row["email"]:
        name = row["firstname"] + " " + row["lastname"]
        relevant_rows.append(row)

dates = []
courses = []
scores = []
course_ratings = []
slopes = []
differentials = []
num_scores = len(relevant_rows)

for row in relevant_rows:
    dates.append(row["date"])
    courses.append(row["course"])
    scores.append(row["score"])
    course_ratings.append(row["rating"])
    slopes.append(row["slope"])
    differentials.append(row["differential"])

if num_scores <= 5:
    x = 1
elif num_scores <= 8:
    x =2
elif num_scores <= 11:
    x = 3
elif num_scores <= 14:
    x = 4
elif num_scores <= 16:
    x = 5
elif num_scores <= 18:
    x = 6
elif num_scores == 19:
    x =7
elif num_scores >= 20:
    x = 8

relevant_differentials = nsmallest(x, differentials)
index = (sum(relevant_differentials[:x])/x)
handicap_index = round(index, 1)

print("-----------------")
print(name.upper())
print(handicap_index, "HANDCIAP INDEX")
print("-----------------")
print("Score     Date     Course Rating/Slope     Differential     Course")
for i in range(num_scores):
    print(f'{scores[i]}        {dates[i]}      {course_ratings[i]}/{slopes[i]}                {round(differentials[i], 1)}              {courses[i]}')