import spacy
from spacy import displacy
nlp = spacy.load("es_dep_news_trf")
#nlp = spacy.load("en_core_web_sm")
#raw_text = nlp('Trata de entender primero cómo está programado hoy @Francisco Barría (lo que implica que tendrás que hablar con @Diego Montt o @Agustin Bereciartua ya que no sé quien hizo la inteligencia), pero creo que debiese tener al menos 3 secciones el mail: - Notificaciones no leídas recibidas en las últimas 24 horas - Tareas donde eres responsable que vencen en el día. Y una sección de avisos con los siguientes avisos: - "Tienes XX clientes faltos de gestión y ZZ clientes con tareas atrasadas o urgentes" y un botón "ir a clientes" - "Tienes XX ventas faltas de gestión y ZZ ventas con tareas atrasadas o urgentes" y un botón "ir a ventas')
nlp.create_pipe('sentencizer')
nlp.add_pipe('sentencizer') # updated
def makeGraphs(raw_text):
    doc = nlp(raw_text)
    sentences = [sent.text.strip()for sent in doc.sents]
    for sentence in sentences:
        
        doc_to_dis=nlp(sentence)
        options = {'compact': True} 
        resultent=displacy.render(doc_to_dis, style="ent",options=options)
        result_dep=displacy.render(doc_to_dis, style="dep",options=options)

        with open("resultent.html", "w") as file:
            file.write(resultent)
        with open("result_dep.html", "w") as file:
            file.write(result_dep)
        result={"result_dep":result_dep,"resultent":resultent}
        return result


