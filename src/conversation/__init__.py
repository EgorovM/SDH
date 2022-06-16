import pandas as pd
import numpy as np

from replicas import ReplicasContainer, Replica
from replicas.classifiers import NeighbourClassifier
from utils.vectorizer import get_sentence_vectorizer
from utils.multilanguage import translate_word


class ConversationBot:
    def __init__(self):
        df = pd.read_csv('./conversation/data/good.tsv',  sep='\t')
        np.random.seed(42)
        df = df.sample(10)

        replicas = ReplicasContainer([
            Replica(row['context_0'], row['reply']) for row in df.iloc
        ])
        self.classifier = NeighbourClassifier.from_replicas_container(
            replicas,
            get_sentence_vectorizer()
        )

    def get_answer(self, message: str) -> str:
        replica = Replica.from_sentence(message)
        answer = self.classifier.classify(replica)
        
        return answer
