# These will not perhaps be needed in the future
# As the data will be given to us from the NodeJS
# in JSON. Then , we can manipulate the JSON directly
# from the dataset to convert it to the objects for the model
import json
from typing import Optional

from flask import jsonify


class DBWordVector():
    def __init__(self, name, vector: list[float]) -> None:
        self.name = name
        self.vector = vector

    @classmethod
    def from_json(cls, data):
        vector = [float(x) for x in data['vector']]
        word = data['word']
        return cls(word, vector)


class DBEmploymentType():
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(data['id'], data['name'])

    @classmethod
    def from_json_list(cls, lst):
        e_types: list[cls] = []
        for e_type_data in lst:
            e_types.append(cls.from_json(e_type_data))
        return e_types


class DBCompany():
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    @classmethod
    def from_json(cls, data):
        return cls(data['id'], data['name'])


class DBTag():
    def __init__(self, id, name: DBWordVector) -> None:
        self.id = id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if (type(other) != DBTag):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(('name', self.name))

    @classmethod
    def from_json(cls, data):
        id = data['id']
        name_vector = DBWordVector.from_json(data['nameWordVector'])
        return cls(id, name_vector)

    @classmethod
    def from_json_list(cls, lst):
        tags: list[cls] = []
        for tag_data in lst:
            tags.append(cls.from_json(tag_data))
        return tags


class DBUser():
    def __init__(self, id, tags: list[DBTag], employment_types: list[DBEmploymentType]) -> None:
        self.id = id
        self.tags = tags
        self.employment_types = employment_types

    @classmethod
    def from_json(cls, data):
        id = data['id']
        tags: list[DBTag] = list(
            map(lambda tag: DBTag.from_json(tag), data['tags']))
        e_types: list[DBEmploymentType] = list(
            map(lambda e_type: DBEmploymentType.from_json(e_type), data['employmentTypes']))
        return cls(id, tags, e_types)


class DBJobPosting():
    def __init__(self, id, title: DBWordVector, description: DBWordVector, tags: list[DBTag], employment_types: list[DBEmploymentType]) -> None:
        self.id = id
        self.tags = tags
        self.employment_types = employment_types
        self.title = title
        self.description = description

    @classmethod
    def from_json(cls, data):
        print(data.keys())
        id = data['id']
        title = DBWordVector.from_json(data['titleWordVector'])
        description = DBWordVector.from_json(data['descriptionWordVector'])
        tags: list[DBTag] = list(
            map(lambda tag: DBTag.from_json(tag), data['tags']))
        e_types: list[DBEmploymentType] = list(
            map(lambda e_type: DBEmploymentType.from_json(e_type), data['employmentTypes']))
        return cls(id, title, description, tags, e_types)

    @classmethod
    def from_json_list(cls, lst):
        job_postings: list[cls] = []
        for job_posting_data in lst:
            job_postings.append(cls.from_json(job_posting_data))
        return job_postings


class DBRating():
    def __init__(self, value: float, user_id, job_posting_id, user: Optional[DBUser], job_posting: Optional[DBJobPosting]) -> None:
        self.value = value
        self.user = user
        self.user_id = user_id
        self.job_posting = job_posting
        self.job_posting_id = job_posting_id

    @classmethod
    def from_json(cls, data):
        value = data['value']
        if ('user' in data):
            user = DBUser.from_json(data['user'])
            user_id = user.id
        else:
            user = None
            user_id = data['userId']
        if ('jobPosting' in data):
            job_posting = DBJobPosting.from_json(
                data['jobPosting'])
            job_posting_id = job_posting.id
        else:
            job_posting = None
            job_posting_id = data['jobPostingId']
        return cls(value,  user_id, job_posting_id, user, job_posting)

    @classmethod
    def from_json_list(cls, lst):
        ratings: list[cls] = []
        for rating_data in lst:
            ratings.append(cls.from_json(rating_data))
        return ratings


class DBPredictedRating():
    def __init__(self,  value: float, user_id: int, job_posting_id: int) -> None:
        self.id = id
        self.value = value
        self.user_id = user_id
        self.job_posting_id = job_posting_id

    @classmethod
    def from_json(cls, data):
        id = data['id']
        value = data['value']
        user = DBUser.from_json(data['user'])
        job_posting = DBJobPosting.from_json(data['jobPosting'])
        return cls(id, value, user, job_posting)

    def to_json(self):
        data = {
            'value': self.value,
            'userId': self.user_id,
            'jobPostingId': self.job_posting_id,
        }
        return json.dumps(data)
