#!/usr/bin/env python
"""
File name: utils.py
Author: Seth Christie
Created: 2024-08-19
Version: 1.0
"""
import json
import os
import time

import requests
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def http_request(url, max_retries=3):
    """Request http data from a provided url."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            return response
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)  # wait 1 second before retrying


def schedule_request(spreadsheet_id, sheet_name):
    """Request data from a Google Spreadsheet for a given url."""
    creds = None
    if os.path.exists("data/token.json"):
        creds = Credentials.from_authorized_user_file("data/token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "data/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("data/token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()  # call the Sheets API
        result = (
            sheet.values()
            .get(spreadsheetId=spreadsheet_id, range=sheet_name)
            .execute()
        )

        if result is None:
            return -1

        schedule = extract_schedule(result, sheet_name)
        return schedule

    except HttpError as http_error:
        print(http_error)
        return -1


def extract_schedule(result, sheet_name):
    """Extracts the schedule data into a dictionary object."""
    data = result.get("values", {})

    schedule = {
        "Name": sheet_name,
        "Courses": {},
        "Transfer": [],
        "External": []
    }

    data_sliced = [row[1:] for row in data if row[0] not in ("External Credits", "Transfer Credits", "")]

    term_num = 0
    for row_index, row in enumerate(data_sliced):
        term = []

        for item_index, item in enumerate(row):
            if item == "":
                term.append("")
                continue
            course_parts = item.split('\n', 1)
            course_id = course_parts[0]
            term.append(course_id)

        schedule["Courses"][term_num] = term
        term_num += 1

    for row in data:
        if row[0] == "External Credits":
            schedule["External"].extend(row[1:])
        elif row[0] == "Transfer Credits":
            schedule["Transfer"].extend(row[1:])

    return schedule


def save_schedule_to_file(schedule):
    """Saves the schedule to a JSON file."""
    filename = f"exports/{schedule["Name"]}.json"
    with open(filename, 'w') as f:
        json.dump(schedule, f, indent=2)


def save_courses_to_file(course_list):
    """Saves the courses dict to a JSON file."""
    filename = f"data/courses.json"
    with open(filename, 'w') as f:
        json.dump(course_list, f, indent=2)


def strip_html(html_text):
    """Strips HTML code from a String."""
    soup = BeautifulSoup(html_text, 'html.parser')
    plain_text = soup.get_text()
    return plain_text
