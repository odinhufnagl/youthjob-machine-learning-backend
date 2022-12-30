class Job():
    def __init__(self, id, title_vector, description_vector, tag_vectors, e_types_hotencoded) -> None:
        self.id = id
        self.title_vector = title_vector
        self.description_vector = description_vector
        self.e_types_hotencoded = e_types_hotencoded
        self.tag_vectors = tag_vectors

    def __str__(self) -> str:
        return str(self.id) + " " + "e_types " + str(self.e_types_hotencoded) + " " + "tags " + str(self.tag_vectors)


class User():
    def __init__(self, id, tag_vectors: list[str], e_types_hotencoded: list[int]) -> None:
        self.id = id
        self.e_types_hotencoded = e_types_hotencoded
        self.tag_vectors = tag_vectors


class Rating():
    def __init__(self, value: float, user: User, job: Job) -> None:
        self.value = value
        self.user = user
        self.job = job
