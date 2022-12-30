# These will not perhaps be needed in the future
# As the data will be given to us from the NodeJS
# in JSON. Then , we can manipulate the JSON directly
# from the dataset to convert it to the objects for the model
import json


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
        name_vector = DBWordVector.from_json(data['name'])
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


class DBJob():
    def __init__(self, id, title: DBWordVector, description: DBWordVector, tags: list[DBTag], employment_types: list[DBEmploymentType]) -> None:
        self.id = id
        self.tags = tags
        self.employment_types = employment_types
        self.title = title
        self.description = description

    @classmethod
    def from_json(cls, data):
        id = data['id']
        title = DBWordVector.from_json(data['title'])
        description = DBWordVector.from_json(data['description'])
        tags: list[DBTag] = list(
            map(lambda tag: DBTag.from_json(tag), data['tags']))
        e_types: list[DBEmploymentType] = list(
            map(lambda e_type: DBEmploymentType.from_json(e_type), data['employmentTypes']))
        return cls(id, title, description, tags, e_types)

    @classmethod
    def from_json_list(cls, lst):
        jobs: list[cls] = []
        for job_data in lst:
            jobs.append(cls.from_json(job_data))
        return jobs


class DBRating():
    def __init__(self, id, value: float, user: DBUser, job: DBJob) -> None:
        self.id = id
        self.value = value
        self.user = user
        self.job = job

    @classmethod
    def from_json(cls, data):
        id = data['id']
        value = data['value']
        user = DBUser.from_json(data['user'])
        job = DBJob.from_json(data['job'])
        return cls(id, value, user, job)

    @classmethod
    def from_json_list(cls, lst):
        ratings: list[cls] = []
        for rating_data in lst:
            ratings.append(cls.from_json(rating_data))
        return ratings


class DBPredictedRating():
    def __init__(self,  value: float, userId: int, jobId: int) -> None:
        self.id = id
        self.value = value
        self.userId = userId
        self.jobId = jobId

    @classmethod
    def from_json(cls, data):
        id = data['id']
        value = data['value']
        user = DBUser.from_json(data['user'])
        job = DBJob.from_json(data['job'])
        return cls(id, value, user, job)

    def to_json(self):
        data = {
            'value': self.value,
            'userId': self.userId,
            'jobId': self.jobId,
        }
        return json.dumps(data)
