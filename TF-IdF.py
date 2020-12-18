import math
#import export
import wikipediaapi
import re
import wikipedia

num_a=50#количество рандомных статей

def tf(word_dict, l):
    tf = dict()
    sum_nk = len(l)
    for word, count in word_dict.items():
        tf[word] = math.log1p(count / sum_nk+1)
    return tf

def idf(word_dict,a_name):
    n = len(word_dict)
    idf = dict.fromkeys(word_dict[a_name[0]].keys(), 0)
    for l in word_dict:
        for word, count in word_dict[l].items():
            if count > 0:
                idf[word] += 1
    for word, v in idf.items():
        idf[word] = math.log1p(n / float(v)+1)
    return idf

def predictions(corpus,tf_idf):#самодельный модуль предсказаний
    pred=dict()
    for i in tf_idf:
        pred[i] = 0
        for j in corpus['predict']:
            if j in tf_idf[i]:
                pred[i]+=tf_idf[i][j]
    maxx=0
    maxx_name='None'
    for i in pred:
        if pred[i]>maxx:
            maxx=pred[i]
            maxx_name=i
    return maxx_name



wikipedia.set_lang('ru')

wiki_wiki = wikipediaapi.Wikipedia(
        language='ru',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

# f = open('name article.txt')
# a_name=[line.strip() for line in f]#Читаем названия статей
# f.close()

a_name=[]
for i in range(num_a):
    a_name.append(wikipedia.random())

corpus=dict()#Страницы вики
for k in a_name:
    corpus[k]=[i.lower() for i in wiki_wiki.page(k).text.split()]#чистим и токенезируем
    for i in corpus:
        for j in range(len(corpus[i])):
            corpus[i][j]=re.sub(r'\W', '',corpus[i][j])#устраняет символы кроме цифр, букв и _

word_set=set()#Множество слов
for i in corpus:
    for j in corpus[i]:
        word_set.add(j)

word_dict=dict()#словарь для каждого текста
for i in corpus:
    word_dict[i] = dict.fromkeys(word_set, 0)

for i in corpus:#подсчитываем слова
    for word in corpus[i]:
        word_dict[i][word] += 1

tf_f=dict()
for i in corpus:
    tf_f[i] = tf(word_dict[i], corpus[i])



idf_f=idf(word_dict,a_name)
tf_idf=dict()
for i in corpus:
    tf_idf[i]=dict.fromkeys(word_dict[i],0)
    for j in tf_idf[i]:
        tf_idf[i][j]=tf_f[i][j]*idf_f[j]

with open('predict.txt','r',encoding='utf-8') as f:
    a_predict=''
    for line in f:#текст который нужно соотнести
        a_predict += line.strip().lower()+' '
corpus['predict']=a_predict.split()
for j in range(len(corpus['predict'])):
    corpus['predict'][j] = re.sub(r'\W', '', corpus['predict'][j])  # устраняет символы кроме цифр, букв и _

print(predictions(corpus,tf_idf))