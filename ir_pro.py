# importing .... 
import nltk
import os
nltk.download('stopwords')
import math
from nltk.corpus import stopwords
#------------------------------------------------------------------------------------
stop_word=set(stopwords.words('english'))
words=[]
term_id={}


#-------------------------------------------------------------------------------------


def clean(line):
    y=''
    x=['.',',','-']
    for i in line:
        for n in i:
            if n in x:
                continue
            else:
                y+=n
    return y
ln=0

#------------------------------------------------------------------------------------

def low(z):
    return z.lower()

#------------------------------------------------------------------------------------
print('---------------------------------------------------part1--------------------------------------------------')
for i in range(1,11,1):
    ln+=1
    file = open('file/file%d.txt'%(i))
    read = file.read()
    read=clean(read)
    lines=read.split()
    index=0
    for word in lines:
        if word in set(stopwords.words('english')):
            continue
        else:
            index += 1
            if word not in term_id:
                term_id[word] = []
                term_id[word].append(1)
                term_id[word].append({ln:[1,index]})
            else:
                if ln in term_id[word][1]:
                    term_id[word][0] += 1
                    term_id[word][1][ln][0] += 1
                    term_id[word][1][ln].append(index)
                else:
                    term_id[word][0] += 1
                    term_id[word][1][ln] = [1,index]
#------------------------------------------------------------------------------------
for i in term_id.keys():
    print(i.ljust(5,' '),end=' ')

print()
print('------------------------------------------------part2----------------------------------------------')

#-------------------------------------------------------------------------------------

def check(word_stop,bol='',index=0,doc=0):
    if bol =='and':
        x=0
        y=0
        ans=[]
        while True:
            try:
                doc1 = list(term_id[word_stop[index - 1]][1].keys())
                doc2 = list(term_id[word_stop[index + 1]][1].keys())
                if doc1[x]==doc2[y]:
                    ans.append(doc2[y])
                    x+=1
                    y+=1
                elif doc1[x]>doc2[y]:
                    y+=1
                else:
                    x+=1
            except Exception:
                break

        if len(ans)>0:
            return ans
        return None

# #--------------------------------------------------------------------------------------
    elif bol=='or':
        non=True
        non2=True
        try:
            doc2 = list(term_id[word_stop[index + 1]][1].keys())
        except Exception:
            non=False
        try:
            doc1 = list(term_id[word_stop[index - 1]][1].keys())
        except Exception:
            if non:
                non2=False
                pass
            else:
                return None
        if non:
            if non2:
                for i in doc2:
                    if i not in doc1:
                        doc1.append(i)
                return sorted(doc1)
            else:
                return doc2
        else:
            return doc1
# ----------------------------------------------------------------------------
    else:
        ans={}
        x=0
        y=0
        try:
            doc1 = term_id[word_stop[0]][1]
            doc2 = term_id[word_stop[1]][1]
            key1=list(doc1.keys())
            key2=list(doc2.keys())
            while True:
                try:
                    if key1[x] == key2[y]:
                        n = 1
                        m = 1
                        while True:
                            try:
                                if doc2[key2[y]][n] - doc1[key1[x]][m] == 1:
                                    ans[key2[y]]=[doc2[key2[y]][n], doc1[key1[x]][m]]
                                    n += 1
                                    m += 1
                                elif doc2[key2[y]][n] > doc1[key1[x]][m]:
                                    m += 1
                                else:
                                    n += 1
                            except Exception:
                                break
                        x += 1
                        y += 1
                    elif key1[x] > key2[y]:
                        y += 1
                    else:
                        x += 1
                except Exception:
                    break
            return ans
        except Exception:
            return None

#-----------------------------------------------------------------------------
def idf(tf):
    t=math.log10(10/tf)
    return t

#-----------------------------------------------------------------------------


def tf_idf(idf,tf):
    return idf*tf

#----------------------------------------------------------------------------
def td():
    
    ln=0
    term_id1 = {}
    for i in range(1, 11, 1):
        ln += 1
        file = open('file/file%d.txt' % (i))
        read = file.read()
        read = clean(read)
        lines = read.split()
        index = 0
        for word in lines:
            if not word :
                continue
            else:
                index += 1
                if word not in term_id1:
                    term_id1[word] = []
                    term_id1[word].append(1)
                    term_id1[word].append({ln: [1, index]})
                else:
                    if ln in term_id1[word][1]:
                        term_id1[word][0] += 1
                        term_id1[word][1][ln][0] += 1
                        term_id1[word][1][ln].append(index)
                    else:
                        term_id1[word][0] += 1
                        term_id1[word][1][ln] = [1, index]
 
    print('\t\tDoc1')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 1:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 1:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')   
    
    print('\t\tDoc2')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 2:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 2:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n') 



    print('\t\tDoc3')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 3:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 3:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')
    print('\t\tDoc4')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 4:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 4:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')
    print('\t\tDoc5')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 5:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 5:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')
    print('\t\tDoc6')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 6:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 6:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')
    print('\t\tDoc7')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 7:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 7:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')
    
    
    
    print('\t\tDoc8')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 8:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 8:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')
    print('\t\tDoc9')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 9:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 9:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')
    print('\t\tDoc10')
    ln = []
    len = []
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 10:
                print(key.ljust(15,' '), end='  ')
                print('%d'.ljust(5, ' ') % (term_id1[key][1][key1][0]), end=' ')
                print('%f'.ljust(5,' ') % (1 + math.log10(term_id1[key][1][key1][0])),end=' ')
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                ln.append((idf(term_id1[key][0]) * term_id1[key][1][key1][0]) ** 2)
                len.append(tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0]))))
                print(t, ''.ljust(5, ' '), end=' ')
                print(t1)
    print("-------------------- Simlarity -----------------------")
    ans1 = 0
    avv = 0
    for i in ln:
        ans1 =  +i
    print(math.sqrt(ans1))
    print("-------------------- Doc Length -----------------------")

    for x in len:
        avv = avv + (x*x)
    print(math.sqrt(avv))
    print()
    
    print("--------------------Normalized tf.idf-----------------------")
    for key in term_id1.keys():
        for key1 in term_id1[key][1].keys():
             if key1 == 10:
                t=idf(term_id1[key][0])
                t1 = tf_idf(idf(term_id1[key][0]), (1 + math.log10(term_id1[key][1][key1][0])))
                print(key.ljust(15,' '), end='  ')
                print(t1/math.sqrt(avv), '\n '.ljust(0, ' '), end=' ')
    print("------------------------------------------------------------------------------", '\n')

for i in term_id.keys():
    print(i,end='')
    for n in term_id[i][1].keys():
        print(': Doc%d : %d'%(n,term_id[i][1][n][1]),end=' ,')
    print()

id=list(term_id)
id.sort(key=low)
print('\n---------------------------------------------------------------------')
query=input('plese enter the query : ')
word_stop=query.split()

bol=['and','or','not']
if 'and' in word_stop or 'or' in word_stop or 'not' in word_stop:
    i=0
    for w in word_stop:
        if w in bol:
            ans=check(word_stop,w,i)
            if ans is list:
                for a in ans:
                    print('Doc',str(a))
            else:
                print(ans)
        i += 1
else:
    if len(word_stop)==1:
        try:
            word_stop = [w for w in query.split() if w not in set(stopwords.words('english'))]
            if len(word_stop) == 1:
                for w in word_stop:
                    for i in term_id[w][1]:
                        print('Doc%d :' % (i), end='')
                        for n in range(1, len(term_id[w][1][i]), 1):
                            print(term_id[w][1][i][n], end=',')
                        print()
        except Exception:
            print(None)
    else:
        word_stop = [w for w in query.split() if w not in set(stopwords.words('english'))]
        ans=check(word_stop)
        if ans==None:
            print(ans)
        else:
            for i in ans:
                print('Doc%d' % (i))


print('-----------------------------------------------------part3-----------------------------------------------')

td()















