from typing import List, Tuple
import joblib

import numpy as np

from diseases import Disease
from diseases.symptoms import Symptom, SymptomsCollection
from utils.preprocessing import CachedNormalizer


DISEASES = ['аппендицит', 'холицестит', 'эзофагит', 'энтерит', 'язва']
SYMPTOMS_WEIGHTS = [
    [1.32, 1.44, 0.83, 0.88, 0.51, -0.53, -0.11, 0.77, 0.17, -0.15, -0.7, -0.23, -0.02, -0.23, -0.09, -0.27, 0.17, -0.23, 0.11, -0.58, -0.45, -0.45, -0.25, -0.39, -0.42],
    [-0.45, -0.83, 0.23, -0.03, -0.35, 1.38, 1.38, 0.47, 0.9, 1.03, -1.19, -0.11, -0.02, -0.23, -0.12, -0.56, -0.12, -0.47, -0.2, -0.09, -0.3, -0.54, -0.37, 0.1, 0.5],
    [-0.6, -0.22, -0.12, -0.23, -0.1, -0.33, -0.29, -0.11, -0.58, -0.2, 2.04, 0.16, 0.22, 1.04, 0.79, 0.37, -0.53, -0.33, -0.32, -0.95, -0.32, -0.36, -0.44, 0.09, -0.67],
    [-0.32, -0.56, 0.12, -0.25, 0.18, -0.43, -0.43, -0.39, -0.64, -0.12, -0.5, 0.26, -0.03, -0.14, -0.17, 0.87, 0.97, 1.31, 1.32, 0.98, -0.06, -0.21, -0.09, -0.41, -0.25],
    [0.05, 0.17, -1.05, -0.38, -0.23, -0.09, -0.55, -0.73, 0.15, -0.56, 0.35, -0.08, -0.15, -0.44, -0.41, -0.41, -0.48, -0.28, -0.91, 0.63, 1.13, 1.56, 1.15, 0.61, 0.84]
]


class DiseasesClassification:
    diseases: List[Disease] = {
        name: Disease(name, weights)
        for name, weights in zip(DISEASES, SYMPTOMS_WEIGHTS)
    }

    def __init__(self) -> None:
        self.normalizer = CachedNormalizer()
        self.vectorizer = joblib.load('./diseases/models/vectorizer.joblib')
        self.clf = joblib.load('./diseases/models/disease_clf.joblib')

    def text_to_vector(self, text: str) -> np.array:
        text = self.normalizer.normalize([text])
        vector = self.vectorizer.transform(text)
        return vector

    def most_possible_disease(self, text: str) -> Tuple[Disease, float]:
        vector = self.text_to_vector(text)
        probas = self.clf.predict_proba(vector)[0]
        label = self.clf.classes_[np.argmax(probas)]
        probability = np.max(probas)
        disease = self.diseases[label]

        return disease, probability

    def find_symptom_to_ask(self, text: str, except_diseases: List[str] = []) -> Symptom:
        vector = self.text_to_vector(text)
        diseases_probability = self.clf.predict_proba(vector)

        # обнуляем вероятности для except_diseases

        diseases_probability = [
            diseases_probability[0][i] * int(DISEASES[i] not in except_diseases)
            for i in range(len(diseases_probability[0]))
        ]
        ask_for_id = np.argmax(diseases_probability)

        tokens_impact = [
            (token, impact, already_mentioned)
            for token, impact, already_mentioned in zip(
                self.vectorizer.get_feature_names_out(),
                SYMPTOMS_WEIGHTS[ask_for_id],
                vector.toarray()[0]
            )
            if not already_mentioned
        ]
        tokens_impact.sort(key=lambda x: abs(x[1]), reverse=True)

        return SymptomsCollection.get_by_name(tokens_impact[0][0])
