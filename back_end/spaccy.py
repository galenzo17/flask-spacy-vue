# import spacy


# # Carga el pipeline pequeño de español
# nlp = spacy.load("es_core_news_sm")

# # Procesa un texto
# doc = nlp("Ella comió pizza")

# # Itera sobre los tokens
# for token in doc:
#     # Imprime en pantalla el texto y la etiqueta gramatical predicha
#     print(token.text, token.pos_)

# doc = nlp(
#     "Apple es la marca que más satisfacción genera en EE.UU., "
#     "pero el iPhone, fue superado por el Galaxy Note 9"
# )

# # Itera sobre las entidades predichas
# for ent in doc.ents:
#     # Imprime en pantalla el texto y la etiqueta de la entidad
#     print(ent.text, ent.label_)

# print(spacy.explain("LOC"))
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest


docA ="""Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data, known as "training data", in order to make predictions or decisions without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning, and focuses on exploratory data analysis through unsupervised learning.In its application across business problems, machine learning is also referred to as predictive analytics."""
nlp = spacy.load("es_core_news_sm")
#nlp = spacy.load('en_core_web_sm')
def spacyTopFive(noteToproces):
    doc = nlp(noteToproces)
    #print(len(list(doc.sents)))
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)

    freq_word = Counter(keyword)
    #print(freq_word.most_common(5))
    textToTopfive=freq_word.most_common(5)
    obj=[]
    for i,value in textToTopfive:
        print(i,value)
        thisdict = {
            i: value
        }
        amount=str(value)
        obj.append(thisdict)
        #for a in i:
            
    #print(obj) 
    return obj

#spacyTopFive(docA)