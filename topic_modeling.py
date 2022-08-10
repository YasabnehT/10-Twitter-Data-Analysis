#%%
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns
import gensim
from gensim.models import CoherenceModel
from gensim import corpora
import pandas as pd
from pprint import pprint
import string
import os
import re
import json

#visualization
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import pickle


class DataLoader():
  def __init__(self,file):
    self.file = file
    
  def read_json(self):
    with open(self.file,'r',encoding = 'utf-8') as jfile:
        # jdata = json.load(jfile)
        jdata_df = pd.read_json(self.file, lines=True)
    return jdata_df

data_loader= DataLoader('data/africa_twitter_data2.json')
jdata_df = data_loader.read_json()
jdata_df.dropna()
# print(len(jdata_df))
# pprint(jdata_df.head())

class Preparation():
    def __init__(self,df):
        self.df=df
    
    def preprocess_data(self):
        jdata_df = self.df.loc[self.df['lang'] =="en"]
        
        #text Preprocessing
        jdata_df['full_text']=jdata_df['full_text'].astype(str)
        jdata_df['full_text'] = jdata_df['full_text'].apply(lambda x: x.lower())
        jdata_df['full_text']= jdata_df['full_text'].apply(lambda x: x.translate(str.maketrans(' ', ' ', string.punctuation)))
        
        #feature engineering from tweets
        sentence_list = [tweet for tweet in jdata_df['full_text']]
        word_list = [sent.split() for sent in sentence_list]
        # pprint(word_list)

        #id:word dictionary
        word_to_id = corpora.Dictionary(word_list)
        # print(word_to_id.token2id) # id:word unique token
        # id:frequency dictionary using bag of words
        corpus_1= [word_to_id.doc2bow(tweet) for tweet in word_list]
        return word_list, word_to_id, corpus_1

prepare_data_obj = Preparation(jdata_df)
word_list, id2word, corpus = prepare_data_obj.preprocess_data()
# pprint(corpus)

id_words = [[(id2word[id],count) for id, count in line] for line in corpus]
# pprint(id_words)

### LDA Modeling ###
# with 3 topics and 20 random_states
lda_model = gensim.models.ldamodel.LdaModel(corpus, id2word=id2word, num_topics=3, random_state=20, 
                                           update_every=1,chunksize=100,passes=10,alpha='auto',
                                           per_word_topics=True)
# pprint(lda_model.print_topics())
# pprint(lda_model.show_topics(formatted=False))

### Model Analysis - perplexity and coherence ###

# the loweer the perplexity, the better the model is
# print('\nPerplexity Measure: ', lda_model.log_perplexity(corpus))  
doc_lda = lda_model[corpus]


# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=word_list, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
# print('\nCoherence Score/Accuracy: ', coherence_lda)

### Data visualization with pyLDAvis ###
pyLDAvis.enable_notebook()
LDAvis_prepared = gensimvis.prepare(lda_model,corpus,id2word)
# LDAvis_prepared


### EDA ###
plot_size = plt.rcParams["figure.figsize"] 
plot_size[0] = 8
plot_size[1] = 6
plt.rcParams["figure.figsize"] = plot_size 

sns.set(rc={'figure.size':(14,10)})

"""
I can't finish it ontime but I will continue and finish it by tomorrow
"""



# %%
