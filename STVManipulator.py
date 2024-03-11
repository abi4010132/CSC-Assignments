import copy
from collections import Counter
import itertools
import random
from ballot import Ballot
import math

from STV import STV

class STVManipulator():

    def __init__(self, votes, alts) -> None:
        self.alts = alts
        stv_election = STV(votes)
        self.all_ballots = copy.deepcopy(stv_election.ballots)
        self.init_winner = stv_election.start()
    

    def find_manipulation(self):
        s = 9999
        manip_ballot = None
        manipulators = None
        manip_alt = None

        # Loop over all alternatives in order of Borda score
        alts = [x for x in self.alts if x != self.init_winner]
        alts = self.sort_by_borda_scores(self.all_ballots, alts)
        for alt in alts:
            print("trying alternative", alt)
            suitable_ballots = self.remove_opposition_voters(alt)
            new_s, new_manip_ballot, new_manipulators = self.elect_alternative_bottomup(suitable_ballots, alt, s)
            if new_s < s: # A new minimum manipulation set is found
                s = new_s
                manipulators = new_manipulators
                manip_ballot = new_manip_ballot
                manip_alt = alt
            if s == 1: break # A single voter could manipulate the election so that is the solution
        return manip_alt, s, manip_ballot, manipulators


    # find the list of ballots which prefer the given alternative to the current winner
    def remove_opposition_voters(self, alt):
        suitable_ballots = []
        for ballot in self.all_ballots:
            if alt == ballot.compare_alternatives(alt, self.init_winner):
                suitable_ballots.append(ballot)

        return suitable_ballots

    # Find the minimum set of voters and manipulation ballot that can manipulate the election to result in the given alternative
    def elect_alternative_bottomup(self, suitable_ballots, alt, min_of_other_alts):
        opposition_ballots = list((Counter(self.all_ballots)-Counter(suitable_ballots)).elements())
        max_manipulators = min(len(suitable_ballots), min_of_other_alts) # The maximum possible number of manipulators that could be a solution
        s = max_manipulators # The set size that will be tried next
        min_manipulators = 1  # The minimum possible number of manipulators that could be a solution

        # Variables to store the best found solution
        best_manipulators_len = 9999
        best_manipulators = []
        best_manipulation_ballot = []

        # Decrease set size with binary search
        while s > 0 and max_manipulators != min_manipulators: # Stop when the number of manipulators is known
            if s < min_manipulators: # Don't try set sizes when larger set sizes didn't create a solution
                s += math.ceil((max_manipulators-s)/2)
                continue

            # Try to find manipulators and a manipulation ballot for a set size of s
            manipulation_ballot = self.get_initial_manipulation_ballot(alt)
            manipulation_ballot_options = [Ballot(x) for x in itertools.permutations(self.alts)]
            manipulators, manipulation_ballot = self.try_manipulate(alt, suitable_ballots, opposition_ballots, manipulation_ballot, s, manipulation_ballot_options)

            if manipulators == []: # No manipulation possible
                if s == max_manipulators: break
                min_manipulators = s+1 
                s += math.ceil((max_manipulators-s)/2) # Binary search upwards
            else:
                if s < best_manipulators_len: # Manipulation possible
                    best_manipulators = manipulators
                    best_manipulation_ballot = manipulation_ballot
                    best_manipulators_len = s
                max_manipulators = s
                s = max_manipulators//2 # Binary search downwards

        return best_manipulators_len, best_manipulation_ballot, best_manipulators

    # Build a profile from three subsets: 1) opposition ballots 2) suitable but preserved ballots 3) manipulated ballots
    def get_profile(self, suitable_ballots, opposition_ballots, manipulators, manipulation_ballot):
        preserved_suitable_ballots = list((Counter(suitable_ballots)-Counter(manipulators)).elements())
        manipulation_ballot.count = len(manipulators)
        return opposition_ballots+preserved_suitable_ballots+[copy.deepcopy(manipulation_ballot)]
    
    # Try to find manipulators and a manipulation ballot for a specific manipulator set size
    def try_manipulate(self, alt, suitable_ballots, opposition_ballots, manipulation_ballot, num_manipulators, manipulation_ballot_options):
        print("trying size", num_manipulators)
    
        # Loop over all subsets of manipulators with size=num_manipulators
        for manipulators in itertools.permutations(suitable_ballots, r=num_manipulators):
            while not manipulation_ballot is None: # None if there is no ballot that is better than those already tried
                # See if this subset and manipulation ballot wins
                profile = self.get_profile(suitable_ballots, opposition_ballots, manipulators, manipulation_ballot)
                stv = STV(profile)
                win, tally_before_end = self.stv_until_loss(alt, stv)
                if win: # Return the solution if it wins
                    return manipulators, manipulation_ballot
                else: # Otherwise, try to improve (somehow?) the manipulation ballot
                    manipulation_ballot_options.remove(manipulation_ballot)
                    manipulation_ballot = self.improve_manipulation_ballot(alt, tally_before_end, manipulation_ballot, manipulation_ballot_options)
            
        return [], None
    
    # Run the stv competition until a certain alternative is eliminated or wins, and return the tally from the round before that
    def stv_until_loss(self, alt, stv):
        while (len(stv.tally) > 1) and min(stv.tally.values()) != max(stv.tally.values()):
            if stv.tally[alt] == min(stv.tally.values()):
                return False, stv.tally
            else:
                stv.eliminate_lowest_alternatives()
                stv.update_tally()
        return True, stv.tally
    
    def improve_manipulation_ballot(self, alt, tally_before_end, manipulation_ballot, manipulation_ballot_options):
        if manipulation_ballot_options == []:
            return None
        else:
            # Just picks a random one for now
            return random.choice(manipulation_ballot_options)
    
    # Create an initial manipulation ballot string guess
    def get_initial_manipulation_ballot(self, alt):
        manipulation_ballot = self.alts.copy()
        manipulation_ballot.remove(alt)
        manipulation_ballot.remove(self.init_winner)
        manipulation_ballot = [alt]+manipulation_ballot+[self.init_winner]
        return Ballot(manipulation_ballot)

    # Sort alternatives by their Borda scores
    def sort_by_borda_scores(self, votes, alts):
        borda_scores = [0]*len(alts)
        for ballot in votes:
            for i, r in enumerate(ballot.ranking):
                if r in alts:
                    borda_scores[alts.index(r)] += len(alts) - (i + 1)
        alts2 = []
        while borda_scores:
            idx_max = max(range(len(borda_scores)), key=borda_scores.__getitem__)
            del borda_scores[idx_max]
            alts2.append(alts[idx_max])
            del alts[idx_max]
        return alts2
