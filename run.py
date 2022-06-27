from preprocess import preprocess
from train import search
from generateTables import pivot

def main():
    preprocess()
    search()
    pivot()

if __name__ == "__main__":
    main()