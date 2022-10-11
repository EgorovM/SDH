import re
import joblib
from typing import List, Tuple

import numpy as np

from diseases import Disease
from diseases.symptoms import Symptom, SymptomsCollection, DISEASE_VECTORIZER
from utils.preprocessing import CachedNormalizer


DISEASE_CLASSIFIER = joblib.load("./diseases/models/disease_clf.joblib")

DISEASES = DISEASE_CLASSIFIER.classes_
SYMPTOMS_WEIGHTS = DISEASE_CLASSIFIER.coef_


class DiseasesClassification:
    diseases: List[Disease] = {
        name: Disease(name, weights)
        for name, weights in zip(DISEASES, SYMPTOMS_WEIGHTS)
    }

    def __init__(self) -> None:
        self.normalizer = CachedNormalizer()
        self.vectorizer = DISEASE_VECTORIZER
        self.clf = DISEASE_CLASSIFIER

    def text_to_vector(self, text: str) -> np.array:
        text = re.sub("[^A-Za-zА-Яа-я]", " ", text)
        text = " ".join([w for w in text.split() if len(w) > 1])
        text = self.normalizer.normalize([text])
        vector = self.vectorizer.transform(text)
        return vector

    def most_possible_disease(self, text: str) -> Tuple[Disease, float]:
        vector = self.text_to_vector(text)
        probas = self.clf.predict_proba(vector)[0]
        label = DISEASES[np.argmax(probas)]
        probability = np.max(probas)
        disease = self.diseases[label]

        return disease, probability

    def find_symptom_to_ask(
        self, text: str, except_diseases: List[str] = []
    ) -> List[Symptom]:
        """Самые первые симптомы из каждой болезни"""
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
                vector.toarray()[0],
            )
            if not already_mentioned
        ]
        tokens_impact.sort(key=lambda x: abs(x[1]), reverse=True)

        return SymptomsCollection.get_by_name(tokens_impact[0][0])
