from cmath import exp
from email.policy import HTTP
import re
from urllib import response
from flask import jsonify
from requests import request
import requests
from sqlalchemy import true
from classes.http import HttpError, HTTPSuccess
from classes.main_api_models import DBPredictedRating
from constants import ENDPOINT
from urllib.parse import urlencode
import json

from classes import *
from typing import Union


def fetch_user(id) -> Union[DBUser, HttpError]:
    try:
        res = requests.get(ENDPOINT.USER(id))
        res.raise_for_status()
        data = res.json()
        return DBUser.from_json(data)
    except requests.exceptions.HTTPError as e:
        print("error fetching user")
        return HttpError(str(e), res.status_code)


def fetch_jobs() -> Union[list[DBJob], HttpError]:
    try:
        res = requests.get(ENDPOINT.JOBS)
        res.raise_for_status()
        data = res.json()
        return DBJob.from_json_list(data)
    except requests.exceptions.HTTPError as e:
        print("error fetching jobs")
        return HttpError(str(e), res.status_code)


def fetch_job(job_id) -> Union[DBJob, HttpError]:
    try:
        res = requests.get(ENDPOINT.JOB(job_id))
        res.raise_for_status()
        data = res.json()
        return DBJob.from_json(data)
    except requests.exceptions.HTTPError as e:
        print("error fetching jobs")
        return HttpError(str(e), res.status_code)


def fetch_ratings(user_id) -> Union[list[DBRating], HttpError]:
    try:
        url = f"{ENDPOINT.RATINGS}?{urlencode({'userId': user_id})}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return DBRating.from_json_list(data)
    except requests.exceptions.HTTPError as e:
        print(res.url, res.text)
        print("error fetching ratings")
        return HttpError(str(e), res.status_code)


def fetch_employment_types() -> Union[list[DBEmploymentType], HttpError]:
    try:
        res = requests.get(ENDPOINT.EMPLOYMENT_TYPES)
        res.raise_for_status()
        data = res.json()
        return DBEmploymentType.from_json_list(data)
    except requests.exceptions.HTTPError as e:
        print("error fetching e_types")
        return HttpError(str(e), res.status_code)


def fetch_tags() -> Union[list[DBTag], HttpError]:
    try:
        res = requests.get(ENDPOINT.TAGS)
        res.raise_for_status()
        data = res.json()
        return DBTag.from_json_list(data)
    except requests.exceptions.HTTPError as e:
        print("error fetching tags")
        return HttpError(str(e), res.status_code)


def create_predicted_ratings(ratings: list[DBPredictedRating]) -> Union[HTTPSuccess, HttpError]:
    try:
        ratings = list(map(lambda r: r.to_json(),  ratings))
        res = requests.post(ENDPOINT.PREDICTED_RATINGS,
                            json.dumps(ratings))
        res.raise_for_status()
        return HTTPSuccess(res.text, res.status_code)
    except requests.exceptions.HTTPError as e:
        print("error creating predicted ratings")
        return HttpError(str(e), res.status_code)
