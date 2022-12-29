from machine_learning.sentence_to_vec import SwedishSentenceToVecModel


def texts_to_embeddings(texts: list[str]):
    model = SwedishSentenceToVecModel()
    vecs = model.encode(texts)
    return vecs
