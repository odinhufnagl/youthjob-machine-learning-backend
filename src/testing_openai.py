import random
from statistics import mean
from services.openai import sentence_to_vec
from services.machine_learning import texts_to_embeddings

from utils import cosine_similarity
import numpy as np

from services.openai import text_completion
from scipy.spatial import distance
from sklearn.metrics import jaccard_score
"""f = open("svenska-ord.txt", "r")
texts = random.sample(f.readlines(), 2000)
"""
"""texts = list(map(lambda txt: txt.replace("\n", " "), texts))"""
texts = ["Vill du jobba med programmering i ett startup",
         "Är du den vi söker? Vi söker en problemlösare med erfarenhet inom Python och SQL",
         "Har du städat mycket och tycker att du är bra på det? Då sökert vi dig som älskar att städa",
         "Vill du ta ett större ansvar även om du inte är så gammal? Då kanske du vill jobba hos oss där du får flera uppgifter, såsom diska, och tvätta toaletter"]
embeddings1 = sentence_to_vec(texts)
"""vec5 = openai_sentence_to_vec([tag1])[0]
vec6 = openai_sentence_to_vec([tag2])[0]
vec7 = openai_sentence_to_vec([tag3])[0]
vec8 = openai_sentence_to_vec([tag4])[0]
vec9 = openai_sentence_to_vec([tag5])[0]"""


sims = []
for i, emb in enumerate(embeddings1):
    for j, emb2 in enumerate(embeddings1):
        if (i == j):
            continue
        sims.append(
            cosine_similarity(emb, emb2))
"""        if (cosine_similarity(emb, emb2)) > 0.95:
            print("similar", texts[i], texts[j])
        if (cosine_similarity(emb, emb2)) < -0.12:
            print("not", texts[i], texts[j])"""
print(sims)
"""print(mean(sims))
print(min(sims))
print(max(sims))"""
"""print(np.std(sims))"""
"""tag_vecs = [vec5, vec6, vec7, vec8, vec9]
for vec in tag_vecs:
    for other_vec in tag_vecs:
        print(cosine_similarity(vec, other_vec))"""
"""txt1 = text_completion("Beskriv jobtiteln Programmerare på Youtube")
txt2 = text_completion("Beskriv jobtiteln Städare i Göteborg")
txt3 = text_completion("Beskriv jobtiteln Utvecklare och web-designer")
vec1 = sentence_to_vec(txt1)
vec2 = sentence_to_vec(txt2)
vec3 = sentence_to_vec(txt3)
sim1 = cosine_similarity(vec1, vec2)
sim2 = cosine_similarity(vec1, vec3)
sim3 = cosine_similarity(vec2, vec3)
print(cosine_similarity(vec1, vec2), cosine_similarity(
    vec2, vec3), cosine_similarity(vec1, vec3))
print(txt1)
print("---")
print(txt2)
print("---")
print(txt3)
print("---")
"""
