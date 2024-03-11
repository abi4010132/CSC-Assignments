from collections import Counter
from ballot import Ballot
from STV import STV
from STVManipulator import STVManipulator
import random
import copy
import timeit

#random.seed(5)

N_VOTERS = 30
LARGE_VALUE = 999999
VERBOSE = True

def read_votes(file_path):
    """Convert .txt file to a list of Ballot objects."""
    with open(file_path, 'r') as file: 
        lines = [line.strip() for line in file if not line.startswith('#')]
        votes = [Ballot(line) for line in lines]
    return votes


def reduce_votes(votes, alts, n):
    """Reduce the considered alternatives and/or the number of votes (randomly)"""
    
    remove_alts = [x for x in list(range(1, 11 + 1)) if x not in alts] # The alternatives that should be removed
    new_votes = [] # The votes to return later
    count = 0 # The number of removed votes
    random.shuffle(votes) # To make the removed votes random
    for ballot in votes:
        for alt in remove_alts:
            ballot.eliminate_alternative(alt)
        if ballot.ranking != []:
            count += ballot.count
            if count > n:
                ballot.count -= count - n
            ballot_count_copy = ballot.count
            ballot.count = 1
            new_votes.extend([copy.deepcopy(ballot) for _ in range(ballot_count_copy)])
            if count >= n:
                return new_votes


if __name__ == '__main__':
    t_start = timeit.default_timer()
    votes = read_votes('data.txt')
    alts = [8,2,3,4,5,1]
    votes = reduce_votes(votes, alts, N_VOTERS)
    print(f"submitted ballots: {list(map(lambda x: x.ranking, votes))}")
    
    manip = STVManipulator(votes, alts, verbose=VERBOSE)
    print(f"initial winner: {manip.init_winner}")
    
    alt, s, manip_ballot, manipulators = manip.find_manipulation()
    if s != LARGE_VALUE: # Manipulation is possible
        print(f"Manipulation found! {s} voters who prefer alternative {alt} can change the results:")
        print(f"{[x.ranking for x in manipulators]} change their votes to {manip_ballot.ranking}")

        # Confirm the solution by first running stv on the initial votes
        stv = STV(votes)
        winner = stv.start()

        # And then on votes including manipulated ones
        manipulated = 0
        manipulators = list(manipulators)
        for ballot in votes:
            if ballot in manipulators:
                manipulators.remove(ballot)
                manipulated += ballot.count
                ballot.count = 0
                if manipulated > s:
                    ballot.count += manipulated - s
                if manipulated >= s:
                    break
        manip_ballot.count = s
        votes.append(manip_ballot)
        stv = STV(votes)
        winner_m = stv.start()
        print('Initial winner:', winner, 'Winner after manipulation', winner_m)

    else:
        print("Manipulation is impossible")
    
    t_end = timeit.default_timer()
    print(f"Program runtime: {t_end - t_start}")
