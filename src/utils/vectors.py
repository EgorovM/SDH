import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def vectors_similarity(vector1: np.array, vector2: np.array):
    return cosine_similarity([vector1], [vector2])[0]
