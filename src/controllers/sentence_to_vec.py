import json
from flask import jsonify
from machine_learning.sentence_to_vec import SwedishSentenceToVecModel
from services.openai import sentence_to_vec as openai_sentence_to_vec
import services


def sentence_to_vec(request):
    print(request.json)
    sentence = request.json['sentence']
    vec = services.texts_to_embeddings([sentence])
    return jsonify(vec[0].tolist())
