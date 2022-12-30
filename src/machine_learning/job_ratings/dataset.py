import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from classes import *
from services.main_api import fetch_employment_types, fetch_job, fetch_jobs, fetch_ratings, fetch_tags, fetch_user
from .data_classes import *
from utils import *

"""class JobColumn:
    ID = "id"
    E_TYPES = "e_types"


class UserColumn:
    ID = "id"
    E_TYPES = "e_types"


class RatingColumn:
    ID = "id"
    USER_ID = "user_id"
    JOB_ID = "job_id"
    RATING = "rating"""


class JobRatingsDataSet():
    def __init__(self) -> None:
        self.employment_types = fetch_employment_types()
        self.tags = fetch_tags()
        """        self.jobs_df: DataFrame = self.init_jobs_df(self.jobs)
        self.users_df: DataFrame = self.init_users_df(self.users)
        self.ratings_df: DataFrame = self.init_ratings_df(self.ratings)
        self.users_jobs_matrix_df: DataFrame = self.init_users_jobs_matrix_df()"""

    """
    def init_users_jobs_matrix_df(self) -> DataFrame:
        user_jobs_matrix = self.ratings_df.pivot_table(
            index=RatingColumn.USER_ID, columns=RatingColumn.JOB_ID, values=RatingColumn.RATING)
        user_jobs_matrix.__class__ = DataFrame
        missing_cols = list(set(self.jobs_df.index) -
                            set(user_jobs_matrix.columns))
        for col in missing_cols:
            user_jobs_matrix[col] = np.nan
        return user_jobs_matrix

    def jobs_data_for_df(self, jobs: list[DBJob]):
                return [{JobColumn.ID: job.id, JobColumn.E_TYPES: [e_type.id for e_type in job.employment_types]} for job in jobs]

            def users_data_for_df(self, users: list[DBUser]):
                return [{UserColumn.ID: user.id, UserColumn.E_TYPES: [e_type.id for e_type in user.employment_types]} for user in users]

            def ratings_data_for_df(self, ratings: list[DBRating]):
                return [{RatingColumn.USER_ID: rating.user.id, RatingColumn.JOB_ID: rating.job.id, RatingColumn.RATING: rating.value} for rating in ratings]

    def init_jobs_df(self, jobs: list[DBJob]) -> DataFrame:
        df = DataFrame(
            self.jobs_data_for_df(jobs))
        df._multi_one_hot_encode(JobColumn.E_TYPES)
        return df

    def init_users_df(self, users: list[DBUser]) -> DataFrame:
        df = DataFrame(self.users_data_for_df(users))
        df._multi_one_hot_encode(UserColumn.E_TYPES)
        return df

    def init_ratings_df(self, ratings: list[DBRating]) -> DataFrame:
        df = DataFrame(self.ratings_data_for_df(ratings))
        return df

    def get_jobs_df(self) -> DataFrame:
        return self.jobs_df

    def get_jobs_rating_df(self, user: DBUser) -> DataFrame:
        df = self.users_jobs_matrix_df.iloc[user.id].to_frame(
            name=RatingColumn.RATING)
        df.__class__ = DataFrame
        return df
    """

    def get_job_ratings(self, user_id) -> list[Rating]:
        res: list[Rating] = []
        dbratings: list[DBRating] = fetch_ratings(user_id)
        print("dbratings", dbratings)
        ratings: list[Rating] = []
        for dbrating in dbratings:
            ratings.append(Rating(dbrating.value,
                           dbrating.user, self.dbjob_to_job(dbrating.job)))
        return ratings

    def init_ratings(self, dbratings: list[DBRating]) -> list[Rating]:
        ratings: list[Rating] = []
        for rating in dbratings:
            new_user = self.get_user(rating.user.id)
            new_job = self.get_job(rating.job.id)
            new_rating = Rating(rating.value, new_user, new_job)
            ratings.append(new_rating)
        return ratings

    def get_jobs(self):
        dbjobs = fetch_jobs()
        print("dbjobs", dbjobs)
        jobs: list[Job] = []
        for dbjob in dbjobs:
            jobs.append(self.dbjob_to_job(dbjob))
        return jobs

    def dbjob_to_job(self, dbjob: DBJob) -> Job:
        job = Job(dbjob.id, dbjob.title.vector, dbjob.description.vector, self.collect_tag_vectors(
            dbjob.tags), self.hotencode_e_types(dbjob.employment_types))
        return job

    def get_user(self, id) -> User:
        dbuser: DBUser = fetch_user(id)
        user = User(dbuser.id, self.collect_tag_vectors(
            dbuser.tags), self.hotencode_e_types(dbuser.employment_types))
        return user

    def get_job(self, id) -> Job:
        dbjob: DBJob = fetch_job(id)
        job = Job(dbjob.id, dbjob.title_vector, self.collect_tag_vectors(
            dbjob.tags), self.hotencode_e_types(dbjob.employment_types))
        return job

    def collect_tag_vectors(self, tags: list[DBTag]):
        return [tag.name.vector for tag in tags]

    def hotencode_e_types(self, e_types: list[DBEmploymentType]):
        return hotencode([e_type.id for e_type in e_types],
                         [e_type.id for e_type in self.employment_types]
                         )
