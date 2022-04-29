from typing import List, Dict

from diseases import Symptom


# получили с модели
SYMPTOMS_NAMES = [
    'запор', 'боль живот', 'температура', 'потеря аппетит',
    'рвота диарея', 'вздутие', 'подреберье', 'право', 'тошнота',
    'горечь', 'изжога', 'изжога отрыжка', 'возникновение изжога',
    'глотание', 'затруднение', 'болеть', 'живота', 'понос', 'диарея',
    'животе', 'еда', 'веса', 'склонность', 'приём', 'тяжесть'
]


class SymptomsCollection:
    # TODO: расписать как будем спрашивать о наличиии для каждого
    symptoms: Dict[str, Symptom] = {
        name: Symptom(name, question='')
        for name in SYMPTOMS_NAMES
    }

    @staticmethod
    def get_by_name(name: str) -> Symptom:
        return SymptomsCollection.symptoms[name]

    @staticmethod
    def get_by_names(names: List[str]) -> List[Symptom]:
        return [SymptomsCollection.get_by_name(name) for name in names]

