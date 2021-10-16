'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math

from nltk.grammar import Nonterminal


class Node:

    def __init__(self, value=None,tf=None, next=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.tf = tf
        self.next = next
        self.skip_pointers = None
        self.score  = 0.0


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list.
                To be implemented."""
            node = self.start_node
            while node is not None:
                traversal.append(node.value)
                node = node.next
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            node = self.start_node
            while node is not None:
                print(node.value)
                print('----------------')
                print(node.skip_pointers)
                print('---------**********-----')

                traversal.append(node.value)
                node = node.skip_pointers
            print(len(traversal))
            return traversal

    def add_skip_connections(self):
        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""
        self.skip_length = (int)(round(math.sqrt(self.length), 0))
        # if(n_skips < 2):
        #     return
        # print('Total length = ' + str(self.length))
        # print('Skip length = ' + str(self.skip_length))
        p1 = self.start_node
        p2 = self.start_node
        while p1 is not None and p2 is not None:
            current = 0
            while p2 is not None and current < self.skip_length:
                current = current + 1
                p2 = p2.next
                if (p2 is None):
                    break

            if p2 is not None:
                p1.skip_pointers = p2
                # print("Node 2 doc value: " + str(p2.value))  
                p1 = p2 

    ## TODO
    def insert_at_end(self, value):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        new_node = Node(value=value, tf = 1)
        self.length += 1
        n = self.start_node

        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return

        elif self.start_node.value >= value:
            self.start_node = new_node
            self.start_node.next = n
            return

        elif self.end_node.value <= value:
            self.end_node.next = new_node
            self.end_node = new_node
            return

        else:
            while n.value < value < self.end_node.value and n.next is not None:
                n = n.next

            m = self.start_node
            while m.next != n and m.next is not None:
                m = m.next
            m.next = new_node
            new_node.next = n

            return
    
    def tf_increment(self,doc_id):
        #to increase the tf value for term in document
        n = self.start_node
        while n is not None:
            if n.value != doc_id:
                n = n.next
            else:
                n.tf = n.tf + 1
                return n.tf
        
        return -1

    def cal_tf_idf(self,freq_list,corpus_length):
        # Tf = (freq of token in a doc after pre-processing / total tokens in the doc after pre-processing)
        # Idf = (total num docs / length of postings list) 
        # tf-idf = Tf*Idf
        n = self.start_node
        while n is not None:
            doc_id = n.value
            # print('My document id is >',doc_id,'corpus_length>>',corpus_length)
            tf = n.tf/freq_list[doc_id]
            idf = corpus_length/self.length
            n.score = tf*idf
            # print('SCORE->>>',n.score)
            n = n.next

    def print_linklist(self):
        print('PRINTING MY LIST>>')
        n = self.start_node
        list = []
        tf = []
        while n:
            list.append(n.value)
            tf.append(n.tf)
            n = n.next

        print('PRINTING DATA**************')
        print(tf)
        print(list)
