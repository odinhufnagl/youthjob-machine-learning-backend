import json

from pandas import period_range
from classes.main_api_models import DBPredictedRating
from machine_learning.job_posting_ratings import JobPostingRatingsDataSet, JobPostingRatingsPredicter
from flask import Request, jsonify
from machine_learning.job_posting_ratings.data_classes import Rating

from services.main_api import create_predicted_ratings, fetch_job_posting, fetch_job_postings


# should be in .env
# possibly go trough constants folder
E_TYPE_WEIGHT = 0.25
TAG_WEIGHT = 0.25
DESCRIPTION_VECTOR_WEIGHT = 0.25
TITLE_VECTOR_WEIGHT = 0.25
USERS_E_TYPE_WEIGHT = 10
USERS_TAG_WEIGHT = 10


def update_predictions(user_id):

    user_id = int(user_id)

    training_dataset = JobPostingRatingsDataSet()

    user = training_dataset.get_user(user_id)
    job_posting_ratings = training_dataset.get_job_posting_ratings(user.id)

    # init predicted
    model = JobPostingRatingsPredicter(
        e_type_weight=E_TYPE_WEIGHT,
        tag_weight=TAG_WEIGHT,
        title_vector_weight=TITLE_VECTOR_WEIGHT,
        description_vector_weight=DESCRIPTION_VECTOR_WEIGHT,
        users_e_type_weight=USERS_E_TYPE_WEIGHT,
        users_tag_weight=USERS_TAG_WEIGHT,
        title_vector_similarity_normalization=lambda x: x,
        description_vector_similarity_normalization=lambda x: x,
        tag_similarity_normalization=lambda x: x,
    )

    # train model
    model.train(user, job_posting_ratings)
    print("job_posting_ratings", job_posting_ratings)

    # make predictions
    job_postings = training_dataset.get_job_postings()
    predicted_ratings: list[float] = model.predict_ratings(job_postings)
    res = []
    for job_posting, rating_value in zip(job_postings, predicted_ratings):
        res.append(
            {"jobPostingId": job_posting.id, "value": rating_value})
    # add predictions to database
    predicted_ratings_to_create: list[DBPredictedRating] = [DBPredictedRating(
        rating_value, user.id, job_posting.id) for job_posting, rating_value in zip(job_postings, predicted_ratings)]
    create_predicted_ratings(predicted_ratings_to_create)
    return jsonify(res)
