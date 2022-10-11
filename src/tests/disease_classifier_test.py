import pandas as pd

from diseases.classificators import DiseasesClassification


def test_disease_classifier():
    df = pd.read_csv("./diseases/data/diseases.csv", sep=";")
    diseases_classificator = DiseasesClassification()

    guess_count = 0

    for text, diagnosis in df.iloc:
        disease, prob = diseases_classificator.most_possible_disease(text)
        guess_count += disease.name == diagnosis

    assert guess_count / df.shape[0] > 0.7


def test_ask_question():
    diseases_classificator = DiseasesClassification()

    assert (
        diseases_classificator.find_symptom_to_ask(
            "затруднённое прохождение пищи по пищеводу",
            ["язва"],
        ).name
        == "изжога"
    )
