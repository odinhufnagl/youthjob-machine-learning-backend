from flask import jsonify
import requests
from classes.http import HttpError
from constants import *
import json
import openai

openai.api_key = OPEN_AI_API_KEY


def sentence_to_vec(sentences):
    sentences = list(
        map(lambda sentence: sentence.replace("\n", " "), sentences))
    embeddings = list(map(lambda x: x['embedding'], openai.Embedding.create(input=sentences, model=OPEN_AI_MODEL.ADA)[
        'data']))
    return embeddings


def text_completion(text):
    openai.api_key = OPEN_AI_API_KEY
    description_1 = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=1024
    ).get('choices')[0].get('text')
    return description_1
