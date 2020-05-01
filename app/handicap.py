
from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from heapq import nsmallest
from heapq import nlargest
from app import APP_ENV

load_dotenv()

DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
SHEET_NAME = os.environ.get("SHEET_NAME", "Scores")

def scores(email):
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

    user_rows = []
    for row in rows:
        if email == row["email"]:
            name = row["firstname"] + " " + row["lastname"]
            user_rows.append(row)

    dates = []
    courses = []
    scores = []
    course_ratings = []
    slopes = []
    differentials = []

    for row in user_rows:
        dates.insert(0,row["date"])
    relevant_dates = nlargest(20, dates)
    relevant_dates.sort()

    for date in relevant_dates:
        for row in user_rows:
            if row["date"] == date:
                courses.insert(0,row["course"])
                scores.insert(0,row["score"])
                course_ratings.insert(0,row["rating"])
                slopes.insert(0,row["slope"])
                differentials.insert(0,row["differential"])

    # CALCULATE HANDICAP

    num_scores = len(relevant_dates)
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
    handicap_index = min(round(index, 1), 54.0)
    if handicap_index < 0:
        handicap_index = "+" + str(handicap_index * -1)

    rounded_differentials = []
    for x in differentials:
        rounded_differentials.append(round(x,1))

    relevant_dates.reverse()

    result = {
        "name": name.upper(),
        "handicap_index": f'{handicap_index} HANDCIAP INDEX',
        "headers": "Score    Date          Course Rating/Slope    Differential    Course",
        "rounds": []
    }

    for i in range(num_scores):
        if len(str(rounded_differentials[i])) > 3:
            result["rounds"].append(f'{scores[i]}       {relevant_dates[i]}    {course_ratings[i]}/{slopes[i]}               {rounded_differentials[i]}            {courses[i]}')
        elif len(str(scores[i])) > 2:
            result["rounds"].append(f'{scores[i]}      {relevant_dates[i]}    {course_ratings[i]}/{slopes[i]}               {rounded_differentials[i]}             {courses[i]}')        
        else:
            result["rounds"].append(f'{scores[i]}       {relevant_dates[i]}    {course_ratings[i]}/{slopes[i]}               {rounded_differentials[i]}             {courses[i]}')

    return result

if __name__ == "__main__":

    if APP_ENV == "development":
        email = input("Email: ")
        results = scores(email=email)

    print("-----------------")
    print(results["name"])
    print(results["handicap_index"])
    print("-----------------")
    print(results["headers"])
    for x in results["rounds"]:
        print(x)