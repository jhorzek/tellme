from chatlas import ChatGoogle
from dotenv import load_dotenv


import wikipedia              
import spacy
#nlp = spacy.load("en_core_web_sm")

load_dotenv()
chat = ChatGoogle()
wikisearch = wikipedia.page("Humboldt Forum")             
wikicontent = wikisearch.content
command='summarize one content in 2 sentence:'+str(wikicontent)
chat.chat(command)
#print(wikicontent)