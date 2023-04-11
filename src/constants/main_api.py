import os
from dotenv import load_dotenv
load_dotenv()

API_PATH = os.getenv('MAIN_API_PATH')
MAIN_API_HEADER_KEY = "x-access-key"


class ENDPOINT:
    def USER(id): return API_PATH + f"/users/{id}"
    def JOB(id): return API_PATH + f"/jobPostings/{id}"

    PREDICTED_RATINGS = API_PATH + "/predictedUserJobPostingRatings"
    JOBS = API_PATH + "/jobPostings"
    EMPLOYMENT_TYPES = API_PATH + "/employmentTypes"
    TAGS = API_PATH + "/tags"
    RATINGS = API_PATH + "/ratings"
