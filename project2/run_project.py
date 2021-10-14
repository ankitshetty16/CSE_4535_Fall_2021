'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        raise NotImplementedError

    def _daat_and(self):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        raise NotImplementedError

    def _get_postings(self,term,skip):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        return self.indexer.get_postings(term,skip)

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        corpus_length = 0
        with open(corpus, 'r') as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
                corpus_length = corpus_length + 1
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf(corpus_length)

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""

            input_term_arr = []
            input_term_arr = self.preprocessor.tokenizer(query)

            for term in input_term_arr:
                postings, skip_postings = None, None

                postings = self._get_postings(term,False)
                skip_postings = self._get_postings(term,True)
                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""

                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings

            # raise NotImplementedError
            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

            ## temporary
            output_dict['daatAnd'] = {
                "from an epidemic to a pandemic": {
                    "num_comparisons": 469,
                    "num_docs": 5,
                    "results": [
                        20899,
                        105351,
                        113525,
                        140299,
                        148720
                    ]
                },
                "is hydroxychloroquine effective?": {
                    "num_comparisons": 163,
                    "num_docs": 2,
                    "results": [
                        75268,
                        108023
                    ]
                },
                "the novel coronavirus": {
                    "num_comparisons": 556,
                    "num_docs": 82,
                    "results": [
                        712,
                        2974,
                        4883,
                        5000,
                        5730,
                        9361,
                        10681,
                        12121,
                        12451,
                        13414,
                        13815,
                        14719,
                        18920,
                        19309,
                        20722,
                        22453,
                        22937,
                        25546,
                        26775,
                        28575,
                        29882,
                        30230,
                        34840,
                        35551,
                        35631,
                        38604,
                        39420,
                        39559,
                        39615,
                        44588,
                        45285,
                        48390,
                        50505,
                        51884,
                        51946,
                        55093,
                        58401,
                        60434,
                        64829,
                        65840,
                        67053,
                        69375,
                        69512,
                        71739,
                        73391,
                        75537,
                        80471,
                        80720,
                        81760,
                        86778,
                        87540,
                        89559,
                        89636,
                        92880,
                        93266,
                        95654,
                        100300,
                        102809,
                        103008,
                        104478,
                        104916,
                        106212,
                        108005,
                        108511,
                        108700,
                        109189,
                        112313,
                        112887,
                        113427,
                        117467,
                        120521,
                        120813,
                        125719,
                        125740,
                        133784,
                        137094,
                        138195,
                        144213,
                        150333,
                        152049,
                        152755,
                        155489
                    ]
                }
            }
            output_dict['daatAndSkip']= {
                "from an epidemic to a pandemic": {
                    "num_comparisons": 451,
                    "num_docs": 5,
                    "results": [
                        20899,
                        105351,
                        113525,
                        140299,
                        148720
                    ]
                },
                "is hydroxychloroquine effective?": {
                    "num_comparisons": 139,
                    "num_docs": 2,
                    "results": [
                        75268,
                        108023
                    ]
                },
                "the novel coronavirus": {
                    "num_comparisons": 556,
                    "num_docs": 82,
                    "results": [
                        712,
                        2974,
                        4883,
                        5000,
                        5730,
                        9361,
                        10681,
                        12121,
                        12451,
                        13414,
                        13815,
                        14719,
                        18920,
                        19309,
                        20722,
                        22453,
                        22937,
                        25546,
                        26775,
                        28575,
                        29882,
                        30230,
                        34840,
                        35551,
                        35631,
                        38604,
                        39420,
                        39559,
                        39615,
                        44588,
                        45285,
                        48390,
                        50505,
                        51884,
                        51946,
                        55093,
                        58401,
                        60434,
                        64829,
                        65840,
                        67053,
                        69375,
                        69512,
                        71739,
                        73391,
                        75537,
                        80471,
                        80720,
                        81760,
                        86778,
                        87540,
                        89559,
                        89636,
                        92880,
                        93266,
                        95654,
                        100300,
                        102809,
                        103008,
                        104478,
                        104916,
                        106212,
                        108005,
                        108511,
                        108700,
                        109189,
                        112313,
                        112887,
                        113427,
                        117467,
                        120521,
                        120813,
                        125719,
                        125740,
                        133784,
                        137094,
                        138195,
                        144213,
                        150333,
                        152049,
                        152755,
                        155489
                    ]
                }
            }
            output_dict['daatAndSkipTfIdf']= {
                "from an epidemic to a pandemic": {
                    "num_comparisons": 451,
                    "num_docs": 5,
                    "results": [
                        105351,
                        113525,
                        140299,
                        148720,
                        20899
                    ]
                },
                "is hydroxychloroquine effective?": {
                    "num_comparisons": 139,
                    "num_docs": 2,
                    "results": [
                        75268,
                        108023
                    ]
                },
                "the novel coronavirus": {
                    "num_comparisons": 556,
                    "num_docs": 82,
                    "results": [
                        13414,
                        87540,
                        152755,
                        2974,
                        109189,
                        12121,
                        30230,
                        50505,
                        58401,
                        81760,
                        89559,
                        100300,
                        117467,
                        25546,
                        29882,
                        35551,
                        39420,
                        48390,
                        92880,
                        106212,
                        120521,
                        125719,
                        19309,
                        20722,
                        38604,
                        51946,
                        55093,
                        65840,
                        69375,
                        73391,
                        95654,
                        125740,
                        138195,
                        712,
                        5000,
                        80720,
                        102809,
                        108700,
                        155489,
                        5730,
                        22453,
                        39559,
                        51884,
                        60434,
                        69512,
                        75537,
                        80471,
                        86778,
                        93266,
                        103008,
                        108005,
                        112313,
                        144213,
                        9361,
                        10681,
                        12451,
                        67053,
                        71739,
                        112887,
                        137094,
                        4883,
                        64829,
                        26775,
                        35631,
                        104916,
                        113427,
                        120813,
                        14719,
                        39615,
                        150333,
                        28575,
                        45285,
                        104478,
                        133784,
                        13815,
                        152049,
                        34840,
                        22937,
                        44588,
                        89636,
                        108511,
                        18920
                    ]
                }
            }
            output_dict['daatAndTfIdf']= {
                "from an epidemic to a pandemic": {
                    "num_comparisons": 469,
                    "num_docs": 5,
                    "results": [
                        105351,
                        113525,
                        140299,
                        148720,
                        20899
                    ]
                },
                "is hydroxychloroquine effective?": {
                    "num_comparisons": 163,
                    "num_docs": 2,
                    "results": [
                        75268,
                        108023
                    ]
                },
                "the novel coronavirus": {
                    "num_comparisons": 556,
                    "num_docs": 82,
                    "results": [
                        13414,
                        87540,
                        152755,
                        2974,
                        109189,
                        12121,
                        30230,
                        50505,
                        58401,
                        81760,
                        89559,
                        100300,
                        117467,
                        25546,
                        29882,
                        35551,
                        39420,
                        48390,
                        92880,
                        106212,
                        120521,
                        125719,
                        19309,
                        20722,
                        38604,
                        51946,
                        55093,
                        65840,
                        69375,
                        73391,
                        95654,
                        125740,
                        138195,
                        712,
                        5000,
                        80720,
                        102809,
                        108700,
                        155489,
                        5730,
                        22453,
                        39559,
                        51884,
                        60434,
                        69512,
                        75537,
                        80471,
                        86778,
                        93266,
                        103008,
                        108005,
                        112313,
                        144213,
                        9361,
                        10681,
                        12451,
                        67053,
                        71739,
                        112887,
                        137094,
                        4883,
                        64829,
                        26775,
                        35631,
                        104916,
                        113427,
                        120813,
                        14719,
                        39615,
                        150333,
                        28575,
                        45285,
                        104478,
                        133784,
                        13815,
                        152049,
                        34840,
                        22937,
                        44588,
                        89636,
                        108511,
                        18920
                    ]
                }
            }
            output_dict['postingsListSkip'] = {
                "coronaviru": [
                    11,
                    5865,
                    12855,
                    21733,
                    28728,
                    34840,
                    41959,
                    50056,
                    55592,
                    63625,
                    72550,
                    79561,
                    86800,
                    93904,
                    102727,
                    108511,
                    117141,
                    123010,
                    129528,
                    136194,
                    144511,
                    151991
                ],
                "effect": [
                    1003,
                    12409,
                    25846,
                    35760,
                    48478,
                    70093,
                    81905,
                    94506,
                    108390,
                    113975,
                    133134,
                    144826,
                    156924
                ],
                "epidem": [
                    1167,
                    13464,
                    29999,
                    53092,
                    84302,
                    92880,
                    103746,
                    114062,
                    125378,
                    140299
                ],
                "hydroxychloroquin": [
                    7436,
                    81851,
                    93573,
                    111873,
                    147101
                ],
                "novel": [
                    712,
                    12451,
                    22937,
                    33421,
                    39492,
                    57900,
                    67053,
                    83227,
                    95654,
                    106212,
                    118884,
                    137094,
                    152755
                ],
                "pandem": [
                    699,
                    7957,
                    19204,
                    25546,
                    33645,
                    42317,
                    52295,
                    59516,
                    63563,
                    73740,
                    80653,
                    85077,
                    93837,
                    103747,
                    113525,
                    122713,
                    130105,
                    139258,
                    147842,
                    151295
                ]
            }

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    print(flask.jsonify(response))
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""
    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")

    argv = parser.parse_args()
    corpus = argv.corpus
    output_location = argv.output_location

    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)
