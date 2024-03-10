from ballot import Ballot
from collections import Counter
from typing import List
import copy

# This class just represents the whole multiround STV process
class STV:

    # Take a list of Ballots as initial input
    def __init__(self, ballots: List[Ballot]):
        self.ballots = copy.deepcopy(ballots)
        self.update_tally()

    # Update the tally
    def update_tally(self):
        # Reset counter, to recount after elimination
        self.tally = Counter()
        for ballot in self.ballots:
            # If there are still alternatives present in a ballot
            if ballot.get_ranking():
                for alternative in ballot.get_ranking():
                    # Initialise alternative with 0, incase alternative is never plurality winner
                    if alternative not in self.tally:
                        self.tally[alternative] = 0
                # Update tally, with plurality winner and number of voters
                self.tally.update({ballot.get_plurality(): ballot.get_count()})

    # Eliminate lowest alternative(s) from tally and votes
    def eliminate_lowest_alternatives(self):
        # List in case multiple tied lowest alternatives
        lowest_alternatives = []
        # If lowest and highest alternative count are the same stop elimination
        if min(self.tally.values()) == max(self.tally.values()):
            return

        # Add alternatives that have the lowest count to the list
        for alternative in self.tally.keys():
            if self.tally[alternative] == min(self.tally.values()):
                lowest_alternatives.append(alternative)

        # Eliminate alternative(s) from the ballot and from the tally
        for alternative in lowest_alternatives:
            for ballot in self.ballots:
                ballot.eliminate_alternative(alternative)
            del self.tally[alternative]
            # print(f"{alternative} is eliminated!")

    # One round of STV
    def round(self):
        self.eliminate_lowest_alternatives()
        self.update_tally()
        # print(self.get_tally())

    # Getter for tally
    def get_tally(self):
        return self.tally

    # Get 
    def get_winner(self):
        # incase of ties
        if self.tally:
            highest_alternatives = []
            for alternative in self.tally.keys():
                if self.tally[alternative] == max(self.tally.values()):
                    highest_alternatives.append(alternative)
            return highest_alternatives
        else:
            return None

    def start(self):
        while (len(self.tally) > 1) and min(self.tally.values()) != max(self.tally.values()):
            self.round()
        return self.get_winner()
        
        