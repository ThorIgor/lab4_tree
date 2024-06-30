import os
import pickle

from utils.inv_index_builder import InvIndexBuilder 


if __name__ == "__main__":
    iib = InvIndexBuilder()
    input = [os.path.join("input", f) for f in os.listdir("input") if os.path.isfile(os.path.join("input", f)) and f[-3:] == 'txt']

    inv_index = iib.map_reduce(input)

    with open("output/inv_index.pickle", "wb") as f:
        pickle.dump(inv_index, f)