from collections import Counter
from ballot import Ballot
from STV import STV
from STVManipulator import STVManipulator
import random
import copy

random.seed(4)

# convert .txt file to a list of Ballot objects.
def read_votes(file_path):
    with open(file_path, 'r') as file: 
        lines = [line.strip() for line in file if not line.startswith('#')]
        votes = [Ballot(line) for line in lines]
    return votes

def reduce_votes(votes, alts, n):
    remove_alts = [x for x in list(range(1, 11 + 1)) if x not in alts]
    new_votes = []
    count = 0
    random.shuffle(votes)
    for ballot in votes:
        for alt in remove_alts:
            ballot.eliminate_alternative(alt)
        if ballot.ranking != []:
            # new_votes.append(ballot)
            count += ballot.count
            if count > n:
                ballot.count -= count - n
            ballot_count_copy = ballot.count
            ballot.count = 1
            new_votes.extend([copy.deepcopy(ballot) for _ in range(ballot_count_copy)])
            if count >= n:
                return new_votes


if __name__ == '__main__':
    votes = read_votes('data.txt')
    alts = [8,2,3,4]
    votes = reduce_votes(votes, alts, 20)
    # votes = reduce_votes(votes, alts, 4)
    for ballot in votes:
        print(ballot.ranking, ballot.count)
    # stv = STV(votes)
    # print(stv.get_tally())
    # winner = stv.start()
    # print(f"{winner} is the highest ranked alternative!")
    manip = STVManipulator(votes, alts)
    alt, s, manip_ballot, manipulators = manip.find_manipulation()
    if s != 9999:
        print('alt =', alt, 'min size =', s, ':', [x.ranking for x in manipulators], 'to', manip_ballot.ranking)
        # confirm
        stv = STV(votes)
        winner = stv.start()

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
        print('unmanipulated winner:', winner, 'manipulated winner', winner_m)
    else:
        print("Manipulation is impossible")