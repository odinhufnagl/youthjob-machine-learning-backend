import numpy as np
from urllib3 import Retry
from ..sentence_to_vec import *
from .data_classes import *
from utils import *
from typing import Callable


class WeightedObject():
    def __init__(self, weight) -> None:
        self.weight = weight


class WeightedVector():
    def __init__(self, weight, vector) -> None:
        self.weight = weight
        self.vector = vector


class FeatureSet():
    def __init__(self, e_types_hotencoded: list[float], tag_weights: list[WeightedVector], title_vector_weights: list[WeightedVector], description_vector_weights: list[WeightedVector]) -> None:
        self.e_types_hotencoded = e_types_hotencoded
        self.tag_weights = tag_weights
        self.title_vector_weights = title_vector_weights
        self.description_vector_weigths = description_vector_weights


class FieldWeightsCollection():
    def __init__(self, e_type_weight=0, tag_weight=0, title_vector_weight=0, description_vector_weight=0) -> None:
        self.e_type_weight = e_type_weight
        self.tag_weight = tag_weight
        self.title_vector_weight = title_vector_weight
        self.description_vector_weight = description_vector_weight


class JobPostingRatingsPredicter():
    def __init__(self, e_type_weight, tag_weight, title_vector_weight, description_vector_weight, users_e_type_weight, users_tag_weight, title_vector_similarity_normalization: Callable[[int], int], description_vector_similarity_normalization: Callable[[int], int], tag_similarity_normalization: Callable[[int], int]) -> None:
        self.title_vector_embeddings = []
        self.tag_embeddings = []
        self.field_weights = FieldWeightsCollection(
            e_type_weight, tag_weight, title_vector_weight, description_vector_weight)
        self.predefined_weights = FieldWeightsCollection(
            e_type_weight=users_e_type_weight, tag_weight=users_tag_weight, title_vector_weight=0, description_vector_weight=0)
        self.feature_set: FeatureSet = None
        self.weighted_feature_set: FeatureSet = None
        self.title_vector_similarity_normalization = title_vector_similarity_normalization
        self.tag_similarity_normalization = tag_similarity_normalization
        self.description_vector_similarity_normalization = description_vector_similarity_normalization

    def predict_ratings(self, job_postings: list[JobPosting]) -> list[float]:
        print(self.weighted_feature_set.title_vector_weights)
        ratings: list[Rating] = []
        for job_posting in job_postings:
            rating_value = self.calculate_rating_value(job_posting)
            ratings.append(rating_value)
        return ratings

    def calculate_rating_value(self, job_posting: JobPosting):
        rating_value_e_types = self.get_rating_value_for_e_types(
            job_posting.e_types_hotencoded)
        rating_value_tags = self.get_rating_value_for_tags(
            job_posting.tag_vectors)
        rating_value_title_vector = self.get_rating_value_for_title_vector(
            job_posting.title_vector)
        rating_value_desc_vector = self.get_rating_value_for_description_vector(
            job_posting.description_vector)
        rating_value = rating_value_e_types + \
            rating_value_tags + rating_value_title_vector + rating_value_desc_vector
        return rating_value

    def calculate_rating_value_vectors(self, weighted_vectors: list[WeightedVector], target_vector: list[float], normalize: Callable[[int], int]):
        rating_value = 0.0
        for weighted_vector in weighted_vectors:
            similarity = normalize(self.similarity_between_vectors(
                weighted_vector.vector, target_vector))
            rating_value += similarity * weighted_vector.weight
        return rating_value

    def calculate_rating_value_hotencoded(self, hotencoded: list[float], target_hotencoded):
        return np.dot(hotencoded, target_hotencoded)

    def calculate_rating_value_multiple_vectors(self, weighted_vectors: list[WeightedVector], target_vectors: list[list[float]], normalize: Callable[[int], int]):
        rating_value = 0.0

        if len(target_vectors) == 0:
            return 0.0
        for weighted_vector in weighted_vectors:
            best_similarity = 0.0
            for target_vector in target_vectors:
                similarity = normalize(self.similarity_between_vectors(
                    target_vector, weighted_vector.vector))
                if (similarity > best_similarity):
                    best_similarity = similarity
            rating_value += best_similarity * weighted_vector.weight
        return rating_value

    def get_rating_value_for_title_vector(self, title_vector: list[float]):
        rating_value = self.calculate_rating_value_vectors(
            self.weighted_feature_set.title_vector_weights, title_vector, self.title_vector_similarity_normalization)
        return rating_value

    def get_rating_value_for_description_vector(self, desc_vector: list[float]):
        rating_value = self.calculate_rating_value_vectors(
            self.weighted_feature_set.description_vector_weigths, desc_vector, self.description_vector_similarity_normalization)
        return rating_value

    def get_rating_value_for_e_types(self, e_types_hotencoded: list[float]):
        rating_value = self.calculate_rating_value_hotencoded(self.weighted_feature_set.e_types_hotencoded,
                                                              e_types_hotencoded)
        return rating_value

    def get_rating_value_for_tags(self, tag_vectors: list[list[float]]):
        rating_value = self.calculate_rating_value_multiple_vectors(
            self.weighted_feature_set.tag_weights, tag_vectors, self.tag_similarity_normalization)
        return rating_value

    def similarity_between_vectors(self, v1: list[float], v2: list[float]) -> float:
        print(cosine_similarity(v1, v2))
        return cosine_similarity(v1, v2)

    def get_weighted_feature_set(self, feature_set: FeatureSet, user: User):
        # add weight from onboarding to e_types
        feature_set_e_types = feature_set.e_types_hotencoded.copy()
        feature_set_e_types = self.add_user_hotencoded_to_hotencoded(
            feature_set_e_types, user.e_types_hotencoded, self.predefined_weights.e_type_weight)
        # add weight from onboarding to tags
        feature_set_tags = feature_set.tag_weights.copy()
        feature_set_tags = self.add_user_vectors_to_weighted_vectors(
            feature_set_tags, user.tag_vectors, self.predefined_weights.tag_weight)

        # calculate the weights for all fields
        feature_set_title_vectors = feature_set.title_vector_weights.copy()
        feature_set_desc_vectors = feature_set.description_vector_weigths.copy()
        weighted_e_types = self.e_type_ratings_to_weighted(feature_set_e_types)
        weighted_tag_weights = self.tag_weights_to_weighted(feature_set_tags)
        weighted_title_vector_weights = self.title_vector_weights_to_weighted(
            feature_set_title_vectors)
        weighted_desc_vector_weights = self.desc_vector_weight_to_weighted(
            feature_set_desc_vectors)
        # concatenate the new weights for the fields
        # fieldweights represent how much a user likes different fields
        weighted_feature_set = FeatureSet(
            e_types_hotencoded=weighted_e_types,
            tag_weights=weighted_tag_weights,
            title_vector_weights=weighted_title_vector_weights,
            description_vector_weights=weighted_desc_vector_weights)

        return weighted_feature_set

    def add_user_hotencoded_to_hotencoded(self, hotencoded: list[float], user_hotencoded: list[float], user_weight: float):
        return (np.array(user_hotencoded) * user_weight) * hotencoded

    def add_user_vectors_to_weighted_vectors(self, weighted_vectors: list[WeightedVector], user_vectors: list[list[float]], user_weight: float):
        weighted_vectors_copy = weighted_vectors.copy()
        for vector in user_vectors:
            weighted_vectors_copy.append(
                WeightedVector(user_weight, vector))
        return weighted_vectors_copy

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

    def tag_weights_to_weighted(self, tag_weights: list[WeightedVector]):
        return self.weight_objects_to_weighted(tag_weights, self.field_weights.tag_weight)

    def title_vector_weights_to_weighted(self, title_vector_weights: list[WeightedVector]):
        return self.weight_objects_to_weighted(title_vector_weights, self.field_weights.title_vector_weight)

    def desc_vector_weight_to_weighted(self, desc_vector_weights: list[WeightedVector]):
        return self.weight_objects_to_weighted(desc_vector_weights, self.field_weights.description_vector_weight)

    def get_feature_set(self, ratings: list[Rating], user: User) -> FeatureSet:
        print("ratings", ratings)
        job_postings: list[JobPosting] = [
            rating.job_posting for rating in ratings]
        e_types_hotencoded = self.feature_set_hotencoding(
            [job_posting.e_types_hotencoded for job_posting in job_postings], ratings, user)
        tag_weights: list[WeightedVector] = []
        title_vector_weights: list[WeightedVector] = []
        desc_vector_weights: list[WeightedVector] = []
        for rating in ratings:
            for tag_vector in rating.job_posting.tag_vectors:
                tag_weights.append(WeightedVector(rating.value, tag_vector))
            title_vector_weights.append(WeightedVector(
                rating.value, rating.job_posting.title_vector))
            desc_vector_weights.append(WeightedVector(
                rating.value, rating.job_posting.description_vector))

        return FeatureSet(e_types_hotencoded, tag_weights, title_vector_weights, desc_vector_weights)

    def feature_set_hotencoding(self, hotencoded_lst: list[list[float]], ratings: list[Rating], user: User):
        if (len(ratings) == 0):
            return np.zeros(len(user.e_types_hotencoded))
        dot_product = np.dot(
            [rating.value for rating in ratings], hotencoded_lst)
        return dot_product

    def train(self, user: User, ratings: list[Rating]):
        feature_set = self.get_feature_set(ratings, user)
        weighted_feature_set = self.get_weighted_feature_set(feature_set, user)
        self.feature_set = feature_set
        self.weighted_feature_set = weighted_feature_set
