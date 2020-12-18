
import wikipediaapi
import wikipedia
import re

wikipedia.set_lang('ru')
print(wikipedia.random())

wiki_wiki = wikipediaapi.Wikipedia(
        language='ru',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)
with open('predict.txt','r',encoding='utf-8') as f:
    a_predict=''
    for line in f:#текст который нужно соотнести
        print(line)

corpus=dict()
corpus['Заглавная_страница']=[i.lower() for i in wiki_wiki.page(wikipedia.random()).text.split()]
print(re.sub(r'\W', '',"corpus['Python_(programming_language)'][i]"))
print(set(corpus['Заглавная_страница']))