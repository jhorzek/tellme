from gensim.summarization.summarizer import summarize                  
from gensim.summarization import keywords
from collections.abc import Mapping

from collections.abc import MutableMapping
from collections.abc import Sequence
import wikipedia              
import en_core_web_sm      

try:
    from collections.abc import Mapping
except ImportError:
    print("Percent summary")        
    from collections import Mapping


wikisearch = wikipedia.page("https://de.wikipedia.org/wiki/Humboldt_Forum")             
wikicontent = wikisearch.content             
nlp = en_core_web_sm.load()            
doc = nlp(wikicontent) 

summ_per = summarize(wikicontent, ratio = 0.6)         
print("Percent summary")            
print(summ_per)   
