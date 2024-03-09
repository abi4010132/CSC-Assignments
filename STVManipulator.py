import copy

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