import numpy as np
from urllib3 import Retry
from ..sentence_to_vec import *
from .data_classes import *
from utils import *
from typing import Callable


class WeightedObject():
    def __init__(self, weight) -> None:
        self.weight = weight


class TagWeight(WeightedObject):
    def __init__(self, weight: float, tag_vector: str) -> None:
        super().__init__(weight)
        self.tag_vector = tag_vector


class TitleVectorWeight(WeightedObject):
    def __init__(self, weight, title_vector: str) -> None:
        super().__init__(weight)
        self.title_vector = title_vector


class FeatureSet():
    def __init__(self, e_types_hotencoded: list[float], tag_weights: list[TagWeight], title_vector_weights: list[TitleVectorWeight]) -> None:
        self.e_types_hotencoded = e_types_hotencoded
        self.tag_weights = tag_weights
        self.title_vector_weights = title_vector_weights


class FieldWeightsCollection():
    def __init__(self, e_type_weight=0, tag_weight=0, title_vector_weight=0) -> None:
        self.e_type_weight = e_type_weight
        self.tag_weight = tag_weight
        self.title_vector_weight = title_vector_weight


class JobRatingsPredicter():
    def __init__(self, e_type_weight, tag_weight, title_vector_weight, users_e_type_weight, users_tag_weight, title_vector_similarity_normalization: Callable[[int], int], tag_similarity_normalization: Callable[[int], int]) -> None:
        self.title_vector_embeddings = []
        self.tag_embeddings = []
        self.field_weights = FieldWeightsCollection(
            e_type_weight, tag_weight, title_vector_weight)
        self.predefined_weights = FieldWeightsCollection(
            e_type_weight=users_e_type_weight, tag_weight=users_tag_weight, title_vector_weight=0)
        self.feature_set: FeatureSet = None
        self.weighted_feature_set: FeatureSet = None
        self.title_vector_similarity_normalization = title_vector_similarity_normalization
        self.tag_similarity_normalization = tag_similarity_normalization

    def predict_ratings(self, jobs: list[Job]) -> list[float]:
        print(self.weighted_feature_set.title_vector_weights)
        ratings: list[Rating] = []
        for job in jobs:
            rating_value_e_types = self.get_rating_value_for_e_types(job)
            rating_value_tags = self.get_rating_value_for_tags(job)
            rating_value_title_vector = self.get_rating_value_for_title_vector(
                job)
            rating_value = rating_value_e_types + \
                rating_value_tags + rating_value_title_vector
            ratings.append(rating_value)
        return ratings

    def get_rating_value_for_title_vector(self, job: Job):
        rating_value = 0.0
        for title_vector_weight in self.weighted_feature_set.title_vector_weights:
            similarity = self.title_vector_similarity_normalization(self.similarity_between_vectors(
                job.title_vector, title_vector_weight.title_vector))
            rating_value += similarity * title_vector_weight.weight
        return rating_value

    def get_rating_value_for_e_types(self, job: Job):
        return sum([a*b for a, b in zip(self.weighted_feature_set.e_types_hotencoded, job.e_types_hotencoded)])

    def get_rating_value_for_tags(self, job: Job):
        rating_value = 0.0
        job_tag_vectors = job.tag_vectors.copy()
        if len(job_tag_vectors) == 0:
            return 0.0
        for tag_weight in self.weighted_feature_set.tag_weights:
            best_similarity = 0.0
            for job_tag_vector in job_tag_vectors:
                similarity = self.tag_similarity_normalization(self.similarity_between_vectors(
                    job_tag_vector, tag_weight.tag_vector))
                if (similarity > best_similarity):
                    best_similarity = similarity
            rating_value += best_similarity * tag_weight.weight
        return rating_value

    def similarity_between_vectors(self, v1: list[float], v2: list[float]) -> float:
        print(cosine_similarity(v1, v2))
        return cosine_similarity(v1, v2)

    def get_weighted_feature_set(self, feature_set: FeatureSet, user: User):
        # add weight from onboarding to e_types
        if (len(feature_set.e_types_hotencoded) == 0):
            feature_set_e_types = np.array(
                [0.0] * len(user.e_types_hotencoded))
        else:
            feature_set_e_types = feature_set.e_types_hotencoded.copy()
        for i in range(0, len(feature_set_e_types)):
            feature_set_e_types[i] += self.predefined_weights.e_type_weight * \
                user.e_types_hotencoded[i]
        # add weight from onboarding to tags
        feature_set_tags = feature_set.tag_weights.copy()
        for tag_vector in user.tag_vectors:
            feature_set_tags.append(
                TagWeight(self.predefined_weights.tag_weight, tag_vector))
        # calculate the weights for both categories
        feature_set_title_vectors = feature_set.title_vector_weights.copy()
        weighted_e_types = self.e_type_ratings_to_weighted(feature_set_e_types)
        weighted_tag_weights = self.tag_weights_to_weighted(feature_set_tags)
        weighted_title_vector_weights = self.title_vector_weights_to_weighted(
            feature_set_title_vectors)
        # concatenate the new weights for the fields
        # fieldweights represent how much a user likes different fields
        weighted_feature_set = FeatureSet(
            e_types_hotencoded=weighted_e_types, tag_weights=weighted_tag_weights, title_vector_weights=weighted_title_vector_weights)
        return weighted_feature_set

    def e_type_ratings_to_weighted(self, e_types_hotencoded_weights: list[float]):
        if (e_types_hotencoded_weights.sum() == 0):
            return [0.0] * len(e_types_hotencoded_weights)
        return e_types_hotencoded_weights * self.field_weights.e_type_weight / e_types_hotencoded_weights.sum()

    def weight_objects_to_weighted(self, weight_objects: list[WeightedObject], weight_sum) -> list[WeightedObject]:
        sum_of_ratings = sum([
            weight_obj.weight for weight_obj in weight_objects])
        weighted_weight_objects = weight_objects.copy()
        for weight_obj in weighted_weight_objects:
            if (sum_of_ratings == 0):
                weight_obj.weight = 0.0
                continue
            weight_obj.weight *= weight_sum / sum_of_ratings
        return weighted_weight_objects

    def tag_weights_to_weighted(self, tag_weights: list[TagWeight]):
        return self.weight_objects_to_weighted(tag_weights, self.field_weights.tag_weight)

    def title_vector_weights_to_weighted(self, title_vector_weights: list[TitleVectorWeight]):
        return self.weight_objects_to_weighted(title_vector_weights, self.field_weights.title_vector_weight)

    def get_feature_set(self, ratings: list[Rating]) -> FeatureSet:
        print("ratings", ratings)
        jobs_hotencoded: list[Job] = []
        for rating in ratings:
            job = rating.job
            jobs_hotencoded.append(job)
        if (len(ratings) == 0):
            e_types_hotencoded = []
        else:
            e_types_hotencoded = np.dot(
                [rating.value for rating in ratings], [job.e_types_hotencoded for job in jobs_hotencoded])
        tag_weights: list[TagWeight] = []
        for rating in ratings:
            for tag_vector in rating.job.tag_vectors:
                tag_weights.append(TagWeight(rating.value, tag_vector))
        title_vector_weights: list[TitleVectorWeight] = []
        for rating in ratings:
            print("rating", rating, rating.value, rating.job.title_vector)
            title_vector_weights.append(TitleVectorWeight(
                rating.value, rating.job.title_vector))
        return FeatureSet(e_types_hotencoded, tag_weights, title_vector_weights)

    def train(self, user: User, ratings: list[Rating]):
        feature_set = self.get_feature_set(ratings)
        print("feture_set", feature_set.title_vector_weights)
        weighted_feature_set = self.get_weighted_feature_set(feature_set, user)
        self.feature_set = feature_set
        self.weighted_feature_set = weighted_feature_set
