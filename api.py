#curl -i -X GET http://Steven:5998@0.0.0.0:5002/
#curl -H "Authorization: Basic U3RldmVuOjU5OTg=" -X GET http://0.0.0.0:5002/
#echo -n Steven:5998 | base64
import random
import pandas as pd
from flask import Flask
import json
from flask import jsonify
from flask import make_response
from flask import abort, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pickle
import re
import nltk
from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords = set(stopwords.words("english"))
stopwords.update(["park", "ride", "rides", "day", "get", "time", "disney", "disneyland", "one", "queue", "go", "food", "paris"])

##def users
##creation dico users et dico permissions
dico_users = {}
dico_perms = {}
dico_credentials = pd.read_csv('credentials.csv').to_dict()
for key in dico_credentials['username'].keys():
    dico_users[dico_credentials['username'][key]]=generate_password_hash(str(dico_credentials['password'][key]))
    dico_perms[dico_credentials['username'][key]]=[dico_credentials['v1'][key],dico_credentials['v2'][key]]

##fonction utiles
def save_obj(obj, name):
    with open(name+'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name+'.pkl', 'rb') as f:
        return pickle.load(f)

#fonction de scoring de sentiment d'une review
#score[-1, +1] (sentiment négatif: score<0 / sentiment positif: score>0)
def score(review):
    ##load models
    model1 = load_obj('model1')
    vectorizer1 = load_obj('vectorizer1')
    ##pre-processing steps
    processed_text = review.lower() #lowercase
    processed_text = re.findall("[a-zA-Z0-9]+", processed_text) #list
    processed_text = [w for w in processed_text if w not in list(stopwords)] #stopwords
    processed_text = [w for w in processed_text if not w.isnumeric()] #skip numeric
    ##stemming
    stemmer = PorterStemmer()
    processed_text = [stemmer.stem(word) for word in processed_text]
    ##detokenize / list / vectorize
    processed_text = TreebankWordDetokenizer().detokenize(processed_text)
    processed_text = [processed_text]
    processed_text_vect = vectorizer1.transform(processed_text)
    ##predict_proba
    probas = model1.predict_proba(processed_text_vect)
    #score: score<0 => sentiment négatif / score>0 => sentiment positif
    if probas.max()==probas[0][0]:
        score = (0.5-probas[0][0]) *2 #score sentiment négatif : de 0 à -1
    else:
        score = (probas[0][1]-0.5) *2 #score sentiment positif : de 0 à +1
    return score

##API
host="0.0.0.0"
api = Flask(import_name='my_api')
#app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username in dico_users and \
            check_password_hash(dico_users.get(username), password):
        return username

def perm_value():
    v1,v2 = dico_perms[str(auth.current_user())] 
    return make_response(jsonify({'username': str(auth.current_user()), 'v1':bool(v1), 'v2':bool(v2)}), 200)


@api.route('/status', methods=['GET']) #renvoie 1 si l’API fonctionne
def api_in_use():
    return  make_response(jsonify({'it works!': '1'}), 200)

@api.route('/permissions', methods=['GET']) #renvoie la liste des permissions d’un utilisateur authentifié par son username et son password
@auth.login_required
def perm_type():
    #    v1, v2 = perm_value()
    perm_json = perm_value()
#    perm_json = perm_json.json()
    return perm_json

@api.route('/v1/test', methods=['GET']) #renvoie les performance de l'algorithme sur le jeu de test
@auth.login_required
def v1_test_score():
    v1,v2 = dico_perms[str(auth.current_user())]
    if v1==1:
        model1_test_score = load_obj('model1_test_score')
        return  make_response(jsonify({"score model1 sur jeu de test": round(model1_test_score,4)}), 200)
    elif v1==0:
        abort(make_response(jsonify({'error': 'check v1 acces'}), 403))
    else:
        abort(make_response(jsonify({'error': 'check v1 value'}), 400))

@api.route('/v1/sentiment/<sentence>', methods=['GET']) #renvoie le score de sentiment v1 de la phrase proposée
@auth.login_required
def v1_resp(sentence):
    v1,v2 = dico_perms[str(auth.current_user())]
    if v1==1:
        score_v1 = round(score(sentence), 4)
        return  make_response(jsonify({"sentence_sentiment_score": score_v1}), 200)
    elif v1==0:
        abort(make_response(jsonify({'error': 'check v1 acces'}), 403))
    else:
        abort(make_response(jsonify({'error': 'check v1 value'}), 400))

@api.route('/v2/sentiment/<sentence>', methods=['GET']) #renvoie le score de sentiment v2 de la phrase proposée
@auth.login_required
def v2_resp(sentence):
    v1,v2 = dico_perms[str(auth.current_user())]
    if v2==1:
        analyzer = SentimentIntensityAnalyzer()
        sentence = sentence.replace("_", " ").replace("%", " ")
        vs = analyzer.polarity_scores(sentence)
        score_v2 = vs['compound']
        return  make_response(jsonify({"sentence_sentiment_score": score_v2}), 200)
    elif v2==0:
        abort(make_response(jsonify({'error': 'check v2 acces'}), 403))
    else:
        abort(make_response(jsonify({'error': 'check v2 value'}), 400))
    
if __name__ == '__main__':
#    api.debug = True
    api.run(host="0.0.0.0", port=5002)

