import numpy as np
from numpy.linalg import norm


def cosine(v1, v2):
    return np.dot(v1, v2) / (norm(v1) * norm(v2))