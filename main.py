import errno
import os
from collections import Counter
from ballot import Ballot
from STV import STV

def read_votes(file_path):
    """Convert .txt file to a list of Ballot objects."""
    
    with open(file_path, 'r') as file: 
        lines = [line.strip() for line in file if not line.startswith('#')]
        votes = [Ballot(line) for line in lines]
    return votes

if __name__ == '__main__':
    votes = read_votes('data.txt')
    stv = STV(votes)
    stv.start()