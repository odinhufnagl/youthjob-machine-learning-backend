import numpy as np
from numpy.linalg import norm


def cosine_similarity(A, B):
    A = np.array(A)
    B = np.array(B)
    return np.dot(A, B)/(norm(A)*norm(B))


def hotencode(elements_to_encode: list, all_elements: list):
    hotencoded = []
    for elem in all_elements:
        if elem in elements_to_encode:
            hotencoded.append(1)
        else:
            hotencoded.append(0)
    return hotencoded
