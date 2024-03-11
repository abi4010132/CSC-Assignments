from ballot import Ballot
from collections import Counter
from typing import List

class STV:
    """This class represents an STV election"""

    def __init__(self, ballots: List[Ballot]):
        """Used to instantiate an STV, with a list of Ballots"""

        self.ballots = ballots
        self.update_tally()

    def update_tally(self):
        """This method updates the tally of the plurality votes each alternative gets in a Counter"""

        # Reset counter, to recount after elimination
        self.tally = Counter()
        for ballot in self.ballots:
            # Only consider ballots that don't have an empty ranking
            if ballot.get_ranking():
                for alternative in ballot.get_ranking():
                    # Initialise alternative with 0, incase alternative is never plurality winner
                    if isinstance(alternative, list): 
                        for alt in alternative:
                            if alt not in self.tally:
                                self.tally[alt] = 0
                    else: 
                        if alternative not in self.tally:
                            self.tally[alternative] = 0

                plurality = ballot.get_plurality()
                # Update tally, with plurality winner(s) and number of voters
                if isinstance(plurality, list):
                    for alternative in plurality:
                        self.tally.update({alternative: ballot.get_count()}) 
                else:
                    self.tally.update({plurality: ballot.get_count()})
    
    def eliminate_lowest_alternatives(self):
        """This method eliminates the lowest alternative(s) from the Ballots in the STV"""

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

    def round(self):
        """This method represents a round of an STV process by eliminating the lowest alternatives and then updating the tally"""

        self.eliminate_lowest_alternatives()
        self.update_tally()

    def get_tally(self):
        """Getter for the tally of the STV"""

        return self.tally
    
    def get_winner(self):
        """Getter for the current top alternative(s) of the STV"""

        # incase of ties initialise list
        if self.tally:
            highest_alternatives = []
            for alternative in self.tally.keys():
                if self.tally[alternative] == max(self.tally.values()):
                    highest_alternatives.append(alternative)
            return highest_alternatives
        else:
            return None
    
    def start(self):
        """This method is so start an STV process that calls round() until there is/are winner(s)"""

        # Loop while tally contains more than one alternative
        # and while the min and max Ballot counts of the tally are equal, incase of ties.
        while (len(self.tally) > 1) and min(self.tally.values()) != max(self.tally.values()):
            self.round()
        print(f"{self.get_winner()} is the highest ranked alternative!")
        