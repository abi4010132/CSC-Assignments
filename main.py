import errno
import os
from collections import Counter
from ballot import Ballot
from STV import STV
from STVManipulator import STVManipulator

# convert .txt file to a list of Ballot objects.
def read_votes(file_path):
    with open(file_path, 'r') as file: 
        lines = [line.strip() for line in file if not line.startswith('#')]
        votes = [Ballot(line) for line in lines]
    return votes

if __name__ == '__main__':
    votes = read_votes('data.txt')
    stv = STV(votes)
    print(stv.get_tally())
    winner = stv.start()
    print(f"{winner} is the highest ranked alternative!")
    manip = STVManipulator(votes)
    print(manip.find_manipulation())