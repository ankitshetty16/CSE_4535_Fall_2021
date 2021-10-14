'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.doc_token_freq = OrderedDict({})
        self.corpus_length = 0

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        self.doc_token_freq[doc_id] = len(tokenized_document)
        print(self.doc_token_freq[doc_id])
        for t in tokenized_document:
            self.add_to_index(t, doc_id)

    def add_to_index(self, term_, doc_id_):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        if(term_ not in self.inverted_index):
            # for new entry in inverted_index
            linked_list = LinkedList()
            linked_list.insert_at_end(doc_id_)
            self.inverted_index[term_] = linked_list
            print('NEW TERM->>>>>>>>>>>>>>>>>>>>>'+term_)
            # print(linked_list.print_linklist())
        
        else:
            # for existing entry in inverted index
            linked_list = self.inverted_index[term_]
            value = linked_list.tf_increment(doc_id_)
            if(value == -1):
                linked_list.insert_at_end(doc_id_)
            print('EXISTING TERM->>>>>>>>>>>>>>>>>>>>>'+term_)
            # print(linked_list.print_linklist())

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for item in self.inverted_index:
            self.inverted_index[item].add_skip_connections()
            

    def calculate_tf_idf(self,total_length):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        for item in self.inverted_index:
            print('calculated tf_idf')
            self.inverted_index[item].cal_tf_idf(self.doc_token_freq,total_length)

    def get_postings(self,term,skip):
        if(skip):
            return self.inverted_index[term].traverse_skips()
        else:            
            return self.inverted_index[term].traverse_list()

