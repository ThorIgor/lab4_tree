from collections import defaultdict
from suffix_tree import Tree

class SuffixTree:
    def __init__(self, vocabulary: list[str]):
        self.vocabulary = vocabulary
        self.tree = Tree({i: " " + w + " " for i, w in enumerate(self.vocabulary)})

    def search(self, query: str):
        parts = query.split("*")
        parts[0] = " " + parts[0]
        parts[-1] += " "

        results = None
        for part in parts:
            if results:
                results &= set([k for k, path in self.tree.find_all(part) if path])
            else:
                results = set([k for k, _ in self.tree.find_all(part)])
        results = [self.vocabulary[k] for k in results]
        return results

class TreeNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_term = False
        self.original_term = None

class PermutermTree:
    def __init__(self, vocabulary: list[str]):
        self.root = TreeNode()
        for word in vocabulary:
            self.add_term(word)

    def add_permutation(self, perm: str, original_term: str):
        node = self.root
        for char in perm:
            if char not in node.children:
                node.children[char] = TreeNode()
            node = node.children[char]
        node.is_end_of_term = True
        node.original_term = original_term

    def add_term(self, term: str):
        term = term + ' '
        for i in range(len(term)):
            perm = term[i:] + term[:i]
            self.add_permutation(perm, term[:-1])

    def collect_terms(self, node):
        results = set()
        if node.is_end_of_term:
            results.add(node.original_term)
        for child_node in node.children.values():
            results.update(self.collect_terms(child_node))
        return results

    def search(self, pattern):
        parts = pattern.split("*")
        pattern = parts[-1] + " " + parts[0]
        unused_parts = []
        if len(parts) > 2:
          unused_parts = parts[1:-1]
        node = self.root
        for char in pattern:
            if char in node.children:
                node = node.children[char]
            else:
                return []

        results = list(self.collect_terms(node))
        for part in unused_parts:
          results = [w for w in results if part in w]
        
        return results

class TrigramIndex:
    def __init__(self, vocabulary: list[str]):
        self.vocabulary = vocabulary
        self.index = defaultdict(set)
        for word in vocabulary:
            key = "  " + word + "  "
            for k in [key[i:i+3]for i in range(len(key)-2)]:
                self.index[k].add(word)
    
    def search (self, query:str):
        parts = query.split("*")
        if parts[0]:
            parts[0] = "  " + parts[0]
        if parts[-1]:
            parts[-1] += "  "
        
        check_for = []
        parts_with_trigram = []
        for part in parts:
            if len(part) < 3:
                check_for.append(part)
            else:
                parts_with_trigram.append(part)

        results = None
        for part in parts_with_trigram:
            for trigram in [part[i:i+3] for i in range(len(part)-2)]:
                if results:
                    results &= self.index[trigram]
                else:
                    results = self.index[trigram]

        if results is None:
            results = set(self.vocabulary)

        for p in check_for:
            results = [w for w in results if p in w]
        
        return results


         