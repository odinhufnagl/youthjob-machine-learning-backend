from sentence_transformers import SentenceTransformer


class SwedishSentenceToVecModel(SentenceTransformer):
    def __init__(self):
        self.model_name = 'KBLab/sentence-bert-swedish-cased'
        super().__init__(self.model_name)
