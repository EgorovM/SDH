from typing import List, Dict

import joblib

from diseases import Symptom


# получили с модели
DISEASE_VECTORIZER = joblib.load('./diseases/models/vectorizer.joblib')
SYMPTOMS_NAMES = DISEASE_VECTORIZER.get_feature_names_out()


class SymptomsCollection:
    # TODO: расписать как будем спрашивать о наличиии для каждого
    symptoms: Dict[str, Symptom] = {
        name: Symptom(name, question=f'Может у вас наблюдается \'{name}\'?')
        for name in SYMPTOMS_NAMES
    }

    @staticmethod
    def get_by_name(name: str) -> Symptom:
        return SymptomsCollection.symptoms[name]

    @staticmethod
    def get_by_names(names: List[str]) -> List[Symptom]:
        return [SymptomsCollection.get_by_name(name) for name in names]

