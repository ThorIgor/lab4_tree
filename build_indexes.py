import pickle

from argparse import ArgumentParser

from utils.indexes import *

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-i", "--index", help = "type of index (st - suffix tree, pi - permuterm index, ti - trigram index)", type = str, default="st")
    parser.add_argument("-s", "--search", help = "search query", type = str, default="l*d*n")

    args = parser.parse_args()

    with open("output/inv_index.pickle", "rb") as f:
        inv_index = pickle.load(f)
    
    vocabulary = list(inv_index.keys())
    index = None
    if args.index == "st":
        index = SuffixTree(vocabulary)
    elif args.index == "pi":
        index = PermutermTree(vocabulary)
    elif args.index =="ti":
        index = TrigramIndex(vocabulary)
    else:
        raise NotImplementedError()
    
    results = index.search(args.search)
    for i, res in enumerate(results):
        print(f"------{i}------")
        print(f"Result: {res}")
        print(f"Files: {inv_index[res]}")
    
    


    
    


    