import copy
from collections import Counter
import itertools
import random
from ballot import Ballot

from STV import STV

class STVManipulator():

    def __init__(self, votes, alts) -> None:
        self.alts = alts
        stv_election = STV(votes)
        self.all_ballots = copy.deepcopy(stv_election.ballots)
        self.init_winner = stv_election.start()[0]
    

    def find_manipulation(self):
        s = 9999
        manip_ballot = None
        manipulators = None
        for alt in [x for x in self.alts if x != self.init_winner]:
            print("trying alternative", alt)
            suitable_ballots = self.remove_opposition_voters(alt)
            new_s, new_manip_ballot, new_manipulators = self.elect_alternative_bottomup(suitable_ballots, alt)
            if new_s < s:
                s = new_s
                manipulators = new_manipulators
                manip_ballot = new_manip_ballot
        return alt, s, manip_ballot, manipulators


    # find the list of ballots which prefer the given alternative to the current winner
    def remove_opposition_voters(self, alt):
        suitable_ballots = []
        for ballot in self.all_ballots:
            if alt == ballot.compare_alternatives(alt, self.init_winner):
                suitable_ballots.append(ballot)

        return suitable_ballots

    
    def elect_alternative_bottomup(self, suitable_ballots, alternative):
        opposition_ballots = list((Counter(self.all_ballots)-Counter(suitable_ballots)).elements())
    
        # Start recursion
        manipulation_ballot = self.get_initial_manipulation_ballot(alternative)
        manipulation_ballot_options = [Ballot(x) for x in itertools.permutations(self.alts)]
        manipulators, manipulation_ballot = self.minimize_manipulators(alternative, suitable_ballots, opposition_ballots, manipulation_ballot, 1, manipulation_ballot_options)
        if manipulators == []: # Manipulation is impossible for this alternative
            return 9999, None, []
        else: # Return the minimum needed number of manipulators and their corresponding ballot
            return len(manipulators), manipulation_ballot, manipulators

    # Build a profile from three subsets: 1) opposition ballots 2) suitable but preserved ballots 3) manipulated ballots
    def get_profile(self, suitable_ballots, opposition_ballots, manipulators, manipulation_ballot):
        preserved_suitable_ballots = list((Counter(suitable_ballots)-Counter(manipulators)).elements())
        manipulation_ballot.count = len(manipulators)
        return opposition_ballots+preserved_suitable_ballots+[copy.deepcopy(manipulation_ballot)]
    
    # Recursive function to find the minimum number of manipulators for an alternative
    def minimize_manipulators(self, alt, suitable_ballots, opposition_ballots, manipulation_ballot, num_manipulators, manipulation_ballot_options):
        # Stop if manipulation is impossible for this alternative
        if num_manipulators > len(suitable_ballots): return [], None

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
    
        # 2. Try to increase manipulator set size and reset manipulation_ballot_options
        manipulation_ballot = self.get_initial_manipulation_ballot(alt)
        manipulation_ballot_options = [Ballot(x) for x in itertools.permutations(self.alts)]
        return self.minimize_manipulators(alt, suitable_ballots, opposition_ballots, manipulation_ballot, num_manipulators+1, manipulation_ballot_options)
    
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
