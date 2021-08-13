####import des librairies
import pandas as pd
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

##fonction utiles
def save_obj(obj, name):
    with open(name+'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name+'.pkl', 'rb') as f:
        return pickle.load(f)

#### Entrainement model1 ####
## chargement du jeu de données des reviews
df = pd.read_csv("./reviews.csv")
# df = pd.read_csv("https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/reviews.csv")
##on scinde le jeu de données en "avis positif" (rating 4 et 5 = +1) et "avis négatifs" (rating 1 et 2 = -1). On supprime les avis neutre (rating 3)
df2 = df[df['Rating'] != 3]
df2['sentiment'] = df['Rating'].apply(lambda rating : +1 if rating > 3 else -1)
##preprocessing pipeline
break_into_words = lambda x : re.findall("[a-zA-Z0-9]+", x)
skip_stop_words = lambda x: [w for w in x if w not in list(stopwords)]
skip_numeric = lambda x : [w for w in x if not w.isnumeric()]
##apply pre-processing steps
processed_text=df2['Review_Text'].str.lower()\
        .map(break_into_words)\
        .map(skip_stop_words)\
        .map(skip_numeric)
df2['processed']=processed_text
##stemming
stemmer = PorterStemmer()
df2['processed'] = [[stemmer.stem(word) for word in sentence] for sentence in df2['processed']]
## train/test
X = df2["processed"].apply(lambda x : TreebankWordDetokenizer().detokenize(x))
y = df2["sentiment"]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=13, train_size = 0.70)
##TfidfVectorizer
vectorizer = TfidfVectorizer()
vectorizer = vectorizer.fit(X_train)
##transform X train and test
X_train_CV = vectorizer.transform(X_train)
X_test_CV = vectorizer.transform(X_test)
##fit model
model = LogisticRegression(max_iter=200).fit(X_train_CV, y_train)
##save train score
model_test_score = model.score(X_test_CV,y_test)
save_obj(model_test_score, 'model1_test_score')
##save model
save_obj(model, 'model1')
save_obj(vectorizer, 'vectorizer1')
print("model training => 'OK'")
print("'model1_test_score.pkl', 'model1.pkl', 'vectorizer1.pkl' successfully saved")
