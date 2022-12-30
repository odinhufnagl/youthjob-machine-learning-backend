import json

from pandas import period_range
from classes.main_api_models import DBPredictedRating
from machine_learning.job_ratings import JobRatingsDataSet, JobRatingsPredicter
from flask import jsonify
from machine_learning.job_ratings.data_classes import Rating

from services.main_api import create_predicted_ratings, fetch_job, fetch_jobs


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

    training_dataset = JobRatingsDataSet()

    user = training_dataset.get_user(user_id)
    job_ratings = training_dataset.get_job_ratings(user.id)

    # init predicted
    model = JobRatingsPredicter(
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
    model.train(user, job_ratings)
    print("job_ratings", job_ratings)

    # make predictions
    jobs = training_dataset.get_jobs()
    predicted_ratings: list[float] = model.predict_ratings(jobs)
    res = []
    for job, rating_value in zip(jobs, predicted_ratings):
        res.append(
            {"jobId": job.id, "value": rating_value})
    # add predictions to database
    predicted_ratings_to_create: list[DBPredictedRating] = [DBPredictedRating(
        rating_value, user.id, job.id) for job, rating_value in zip(jobs, predicted_ratings)]
    create_predicted_ratings(predicted_ratings_to_create)
    return jsonify(res)
