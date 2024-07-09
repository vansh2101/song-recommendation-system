import numpy as np
from numpy.linalg import norm


def cosine(v1, v2):
    score = np.dot(v1, v2) / (norm(v1) * norm(v2))
    return (score + 1)/2


def match(v1, v2):
    if isinstance(v1, list) and isinstance(v2, list):
        scores = []
        for i in range(len(v1)):
            scores.append(int(v1[i] == v2[i]))

        return sum(scores) / len(scores)

    return int(v1 == v2)


def manhattan_distance(v1, v2):
    return 1 - np.sum(np.abs(v1 - v2))