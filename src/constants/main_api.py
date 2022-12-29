import os
from dotenv import load_dotenv
load_dotenv()

API_PATH = os.getenv('MAIN_API_PATH')


class ENDPOINT:
    def USER(id): return API_PATH + f"/users/{id}"
    def JOB(id): return API_PATH + f"/job/{id}"

    PREDICTED_RATINGS = API_PATH + "/predictedUserJobRatings"
    JOBS = API_PATH + "/jobs"
    EMPLOYMENT_TYPES = API_PATH + "/employmentTypes"
    TAGS = API_PATH + "/tags"
    RATINGS = API_PATH + "/userJobRatings"
