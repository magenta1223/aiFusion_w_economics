from preprocess import preprocess
from train import search
from generateTables import pivot



if __name__ == "__main__":
    preprocess()
    search()
    pivot()