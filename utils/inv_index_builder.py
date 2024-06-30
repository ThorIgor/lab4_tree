from nltk.tokenize import word_tokenize

import multiprocessing
from collections import defaultdict


class InvIndexBuilder:

    def map(self, file: str):
        with open(file, "r", encoding='utf8') as f:
            words = word_tokenize(f.read().lower().replace("\n", " "))
            pairs = [(word, file) for word in words if word.isalpha()]
            return pairs

    def reduce(self, pairs: list):
        term_doc_dict = defaultdict(set)
        for term, file in pairs:
            term_doc_dict[term].add(file)
        return term_doc_dict

    def map_reduce(self, files: list[str]):
        with multiprocessing.Pool() as pool:
            map_results = pool.map(self.map, files)
            flattened_map_results = [p for l in map_results for p in l]
            term_doc_dict = self.reduce(flattened_map_results)

        return term_doc_dict