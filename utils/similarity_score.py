import numpy as np
from numpy.linalg import norm


def cosine(v1, v2):
    score = np.dot(v1, v2) / (norm(v1) * norm(v2))
    return (score + 1)/2


def match(v1, v2):
    if isinstance(v1, list) and isinstance(v2, list):
        unique = set(v1).intersection(v2)
        num = len(v1) + len(v2) - len(unique)

        return len(unique) / num

    return int(v1 == v2)


def manhattan_distance(v1, v2, scale=1):
    return 1 - (np.sum(np.abs(v1 - v2)) / scale)


def inverse_manhattan_distance(v1, v2, scale=100):
    return 1 / (1 + (np.sum(np.abs(v1 - v2) / scale)))