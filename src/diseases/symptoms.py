from typing import List, Dict
import joblib

from diseases import Symptom
from utils.multilanguage import translate_word, en_vectorizer


def describe_symptom(name: str) -> Symptom:
    # если английский
    name = translate_word(name)
    return Symptom(name, question=f"Чувствуете ли вы '{name}'?")


# получили с модели

DISEASE_VECTORIZER = joblib.load("./diseases/models/vectorizer.joblib")
# en_vectorizer(DISEASE_VECTORIZER)
SYMPTOMS_NAMES = DISEASE_VECTORIZER.get_feature_names_out()


class SymptomsCollection:
    # TODO: расписать как будем спрашивать о наличиии для каждого
    symptoms: Dict[str, Symptom] = {
        name: describe_symptom(name) for name in SYMPTOMS_NAMES
    }

    @staticmethod
    def get_by_name(name: str) -> Symptom:
        return SymptomsCollection.symptoms[name]

    @staticmethod
    def get_by_names(names: List[str]) -> List[Symptom]:
        return [SymptomsCollection.get_by_name(name) for name in names]
