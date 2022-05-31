from typing import List


class Symptom:
    name: str
    question: str

    def __init__(self, name: str, question: str) -> None:
        self.name = name
        self.question = question


class Disease:
    name: str
    probability: float
    symptoms: List[Symptom]

    def __init__(self, name: str, symptoms: List[Symptom]) -> None:
        self.name = name
        self.symptoms = symptoms

    def find_match_percentage(self, text: str) -> float:
        count = 0

        for symptom in self.symptoms:
            count += symptom.name in text

        return count / len(self.symptoms)
