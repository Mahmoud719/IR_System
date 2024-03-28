#---------------------------------------------------------------------------
import string
from nltk.corpus import stopwords
import nltk
#---------------------------------------------------------------------------
class PreProcessText(object):

    def __init__(self):
        pass

    def __remove_punctuation(self, text):
        """
        Takes a String
        return : Return a String
        """
        message = []
        for x in text:
            if x in string.punctuation:
                pass
            else:
                message.append(x)
        message = ''.join(message)

        return message

    def __remove_stopwords(self, text):
        """
        Takes a String
        return List
        """
        words= []
        for x in text.split():

            if x.lower() in stopwords.words('english'):
                pass
            else:
                words.append(x)
        return words

    def token_words(self,text=''):
        """
        Takes String
        Return Token also called  list of words that is used to
        Train the Model
        """
        message = self.__remove_punctuation(text)
        words = self.__remove_stopwords(message)
        return words 
#---------------------------------------------------------------------------
def main():
    import nltk

    with open("file/file1.txt","r") as m ,open("file/file2.txt","r") as h, open("file/file3.txt","r") as a :
        f1 = m.read()
        f2 = h.read()
        f3 = a.read()
        news1 = f1  + '\n' + f2 + '\n' + f3
        helper = PreProcessText()
        words = helper.token_words(text=news1)
        print(words)
#---------------------------------------------------------------------------
if __name__ == "__main__":
    main()