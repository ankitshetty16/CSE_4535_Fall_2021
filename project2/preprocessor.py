'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
        tokensList = []
        cleansedText = ''
        cleansedText = re.sub("[^A-Za-z0-9]+", ' ', text.lower()).strip()
        for token in cleansedText.split(" "):
            if(token not in self.stop_words):
                stemmedToken = self.ps.stem(token)
                tokensList.append(stemmedToken)

        return tokensList
