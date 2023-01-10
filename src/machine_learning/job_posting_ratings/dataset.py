import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from classes import *
from services.main_api import *
from .data_classes import *
from utils import *

"""class JobPostingColumn:
    ID = "id"
    E_TYPES = "e_types"


class UserColumn:
    ID = "id"
    E_TYPES = "e_types"


class RatingColumn:
    ID = "id"
    USER_ID = "user_id"
    JOB_ID = "job_posting_id"
    RATING = "rating"""


class JobPostingRatingsDataSet():
    def __init__(self) -> None:
        self.employment_types = fetch_employment_types()
        """        self.job_postings_df: DataFrame = self.init_job_postings_df(self.job_postings)
        self.users_df: DataFrame = self.init_users_df(self.users)
        self.ratings_df: DataFrame = self.init_ratings_df(self.ratings)
        self.users_job_postings_matrix_df: DataFrame = self.init_users_job_postings_matrix_df()"""

    """
    def init_users_job_postings_matrix_df(self) -> DataFrame:
        user_job_postings_matrix = self.ratings_df.pivot_table(
            index=RatingColumn.USER_ID, columns=RatingColumn.JOB_ID, values=RatingColumn.RATING)
        user_job_postings_matrix.__class__ = DataFrame
        missing_cols = list(set(self.job_postings_df.index) -
                            set(user_job_postings_matrix.columns))
        for col in missing_cols:
            user_job_postings_matrix[col] = np.nan
        return user_job_postings_matrix

    def job_postings_data_for_df(self, job_postings: list[DBJobPosting]):
                return [{JobPostingColumn.ID: job_posting.id, JobPostingColumn.E_TYPES: [e_type.id for e_type in job_posting.employment_types]} for job_posting in job_postings]

            def users_data_for_df(self, users: list[DBUser]):
                return [{UserColumn.ID: user.id, UserColumn.E_TYPES: [e_type.id for e_type in user.employment_types]} for user in users]

            def ratings_data_for_df(self, ratings: list[DBRating]):
                return [{RatingColumn.USER_ID: rating.user.id, RatingColumn.JOB_ID: rating.job_posting.id, RatingColumn.RATING: rating.value} for rating in ratings]

    def init_job_postings_df(self, job_postings: list[DBJobPosting]) -> DataFrame:
        df = DataFrame(
            self.job_postings_data_for_df(job_postings))
        df._multi_one_hot_encode(JobPostingColumn.E_TYPES)
        return df

    def init_users_df(self, users: list[DBUser]) -> DataFrame:
        df = DataFrame(self.users_data_for_df(users))
        df._multi_one_hot_encode(UserColumn.E_TYPES)
        return df

    def init_ratings_df(self, ratings: list[DBRating]) -> DataFrame:
        df = DataFrame(self.ratings_data_for_df(ratings))
        return df

    def get_job_postings_df(self) -> DataFrame:
        return self.job_postings_df

    def get_job_postings_rating_df(self, user: DBUser) -> DataFrame:
        df = self.users_job_postings_matrix_df.iloc[user.id].to_frame(
            name=RatingColumn.RATING)
        df.__class__ = DataFrame
        return df
    """

    def get_job_posting_ratings(self, user_id) -> list[Rating]:
        dbratings: list[DBRating] = fetch_ratings(user_id)
        print("dbratings", dbratings)
        ratings: list[Rating] = []
        for dbrating in dbratings:
            print(dbrating)
            if (dbrating.user_id == user_id):
                ratings.append(Rating(dbrating.value, dbrating.user_id, dbrating.job_posting_id,
                                      dbrating.user, self.dbjob_posting_to_job_posting(dbrating.job_posting)))
        return ratings

    def init_ratings(self, dbratings: list[DBRating]) -> list[Rating]:
        ratings: list[Rating] = []
        for rating in dbratings:
            new_user = self.get_user(rating.user.id)
            new_job_posting = self.get_job_posting(
                rating.job_posting.id)
            new_rating = Rating(rating.value, new_user, new_job_posting)
            ratings.append(new_rating)
        return ratings

    def get_job_postings(self):
        dbjob_postings = fetch_job_postings()
        print("dbjob_postings", dbjob_postings)
        job_postings: list[JobPosting] = []
        for dbjob_posting in dbjob_postings:
            job_postings.append(
                self.dbjob_posting_to_job_posting(dbjob_posting))
        return job_postings

    def dbjob_posting_to_job_posting(self, dbjob_posting: DBJobPosting) -> JobPosting:
        print("dbjob_posting", dbjob_posting)
        job_posting = JobPosting(dbjob_posting.id, dbjob_posting.title.vector, dbjob_posting.description.vector, self.collect_tag_vectors(
            dbjob_posting.tags), self.hotencode_e_types(dbjob_posting.employment_types))
        return job_posting

    def get_user(self, id) -> User:
        dbuser: DBUser = fetch_user(id)
        user = User(dbuser.id, self.collect_tag_vectors(
            dbuser.tags), self.hotencode_e_types(dbuser.employment_types))
        return user

    def get_job_posting(self, id) -> JobPosting:
        dbjob_posting: DBJobPosting = fetch_job_posting(id)
        job_posting = JobPosting(dbjob_posting.id, dbjob_posting.title_vector, self.collect_tag_vectors(
            dbjob_posting.tags), self.hotencode_e_types(dbjob_posting.employment_types))
        return job_posting

    def collect_tag_vectors(self, tags: list[DBTag]):
        return [tag.name.vector for tag in tags]

    def hotencode_e_types(self, e_types: list[DBEmploymentType]):
        return hotencode([e_type.id for e_type in e_types],
                         [e_type.id for e_type in self.employment_types]
                         )
