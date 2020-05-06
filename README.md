# Golf Handicap Master

## Overview

This web application functions as a handicap calculator for golfers to post and store scores on.  Users can visit the 'Post Score' tab to enter details about a previous round of golf.  After entering the information, users will be directed to a results page showing their current handicap index and details about all their rounds that were eligible to be including in the calculation.  Additionally, if users would like to view their handicap without entering a new round, they can visit the 'View Handicap' tab and enter the email address their scores are associated with to view it.  All handicap calculations are consitent with USGA protocol found within the Rules of Golf.

Currently, the web application is running on:

```sh
https://golf-handicap-plf14.herokuapp.com/
```

## Installation

Fork this repo, then clone your fork to download it locally onto your computer.  Then navigate there from the command line.

```sh
cd ~/Documents/OPIM-244/GitHub/golf-handicap
```
## Setup

### Environment Setup

Setup a virtual enviorment called something like "golf-env" and from within it install the requirements

```sh
conda create -n golf-env python=3.7 # (first time only)
conda activate golf-env

pip install requirements.txt
```
### .env Setup

First you need to obtain credentials so that you are able to read from and write to the Google Sheet.

Follow these instructions to obtain such credentials:  https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/gspread.md

Now that you have your credentials, use your text editor or the command-line to create a file in that repo called ".env", and then place the following contents inside:

```sh
APP_ENV="development" # or set to "production" on Heroku server

GOOGLE_SHEET_ID = "*Unique Identifer at end of the URL*"
SHEET_NAME = "*Sheet Name*"

GOOGLE_CREDENTIALS='{*Contents of the credentials.json file*}'
```

## Usage

To run the python scripts on terminal, use the following commands:

```sh
python -m app.handicap
python -m app.post
```

To open and run the website locally on your computer, use the following command:

```sh
FLASK_APP=web_app flask run
```

To visit the website while runninig locally, enter the followinig into your browser:

```sh
http://127.0.0.1:5000/
```