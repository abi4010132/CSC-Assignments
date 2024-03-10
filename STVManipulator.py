import copy
from collections import Counter
import itertools
import random

from STV import STV

N_ALTERNATIVES = 11 #TODO change this to not be hardcoded

class STVManipulator():

    def __init__(self, votes) -> None:
        stv_election = STV(votes)
        self.all_ballots = copy.deepcopy(stv_election.ballots)
        self.init_winner = stv_election.start()
    

    def find_manipulation(self):
        for alt in range(1, N_ALTERNATIVES + 1):
            suitable_ballots = self.remove_opposition_voters(alt)
            self.elect_alternative(suitable_ballots, alt)


    # find the smallest set of voters which can manipulate the results to get the given alternative,
    # assuming they prefer the alternative to the current winner
    # TODO: implement this
    def elect_alternative(self, suitable_ballots, alternative):
        return None
    

    # find the list of ballots which prefer the given alternative to the current winner
    def remove_opposition_voters(self, alternative):
        suitable_ballots = []
        for ballot in self.strat_ballots:
            if alternative == ballot.compare_alternatives(alternative, self.init_winner):
                suitable_ballots.append(ballot)

        return suitable_ballots



    
    def elect_alternative_bottomup(self, suitable_ballots, alternative):
        opposition_ballots = list((Counter(self.all_ballots)-Counter(suitable_ballots)).elements())
    
        # Start recursion
        manipulation_ballot = self.get_initial_manipulation_ballot(alternative)
        manipulation_ballot_options = list(itertools.permutations(list(range(1, N_ALTERNATIVES+1))))
        manipulators, manipulation_ballot = self.minimize_manipulators(alternative, suitable_ballots, opposition_ballots, manipulation_ballot, 1, manipulation_ballot_options)
        if manipulators == []: # Manipulation is impossible for this alternative
            return len(suitable_ballots)+1
        else: # Return the minimum needed number of manipulators and their corresponding ballot
            return len(manipulators), manipulation_ballot

    # Build a profile from three subsets: 1) opposition ballots 2) suitable but preserved ballots 3) manipulated ballots
    def get_profile(self, opposition_ballots, manipulators, manipulation_ballot):
        preserved_suitable_ballots = list((Counter(self.suitable_ballots)-Counter(manipulators)).elements())
        return opposition_ballots+preserved_suitable_ballots+[manipulation_ballot]*len(manipulators)
    
    # Recursive function to find the minimum number of manipulators for an alternative
    def minimize_manipulators(self, alt, suitable_ballots, opposition_ballots, manipulation_ballot, num_manipulators, manipulation_ballot_options):
        # Stop if manipulation is impossible for this alternative
        if num_manipulators > len(suitable_ballots): return [], []
    
        # Loop over all subsets of manipulators with size=num_manipulators
        for manipulators in itertools.permutations(suitable_ballots, r=num_manipulators):
            while manipulation_ballot != None: # None if there is no ballot that is better than those already tried
                # See if this subset and manipulation ballot wins
                profile = get_profile(opposition_ballots, manipulators, manipulation_ballot)
                stv = STV(profile)
                win, tally_before_end = self.stv_until_loss(alt, stv)
                if win: # Return the solution if it wins
                    return manipulators, manipulation_ballot
                else: # Otherwise, try to improve (somehow?) the manipulation ballot
                    manipulation_ballot_options.remove(manipulation_ballot)
                    manipulation_ballot = improve_manipulation_ballot(alt, tally_before_end, manipulation_ballot, manipulation_ballot_options)
    
        # 2. Try to increase manipulator set size and reset manipulation_ballot_options
        manipulation_ballot = self.get_initial_manipulation_ballot(alt)
        manipulation_ballot_options = list(itertools.permutations(list(range(1, N_ALTERNATIVES+1))))
        return minimize_manipulators(alt, suitable_ballots, opposition_ballots, manipulation_ballot, num_manipulators+1, manipulation_ballot_options)
    
    # Run the stv competition until a certain alternative is eliminated or wins, and return the tally from the round before that
    def stv_until_loss(alt, stv):
        while (len(stv.tally) > 1) and min(stv.tally.values()) != max(stv.tally.values()):
            if stv.tally[alt] == min(stv.tally.values()):
                return False, stv.tally
            else:
                stv.eliminate_lowest_alternatives()
                stv.update_tally()
        return True, stv.tally
    
    def improve_manipulation_ballot(alt, tally_before_end, manipulation_ballot, manipulation_ballot_options):
        if manipulation_ballot_options == []:
            return None
        else:
            # Just picks a random one for now
            return random.choice(manipulation_ballot_options)
    
    # Create an initial manipulation ballot guess
    def get_initial_manipulation_ballot(alt):
        manipulation_ballot = list(range(1, N_ALTERNATIVES+1))
        del manipulation_ballot[alt-1]
        del manipulation_ballot[self.init_winner-1]
        manipulation_ballot = [alt]+manipulation_ballot+[self.init_winner]
