import copy

from STV import STV

class STVManipulator():

    def __init__(self, votes) -> None:
        stv_election = STV(votes)
        self.all_ballots = copy.deepcopy(stv_election.ballots)
        self.init_winner = stv_election.start()

        self.strat_ballots = self.identify_suitable_voters()


    # only voters who do not already win the election would want to manipulate the results
    def identify_suitable_voters(self):
        suitable_ballots = []
        for ballot in self.all_ballots:
            if ballot.get_plurality() != self.init_winner:
                suitable_ballots.append(ballot)

        return suitable_ballots
