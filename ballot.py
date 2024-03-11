import re 

class Ballot:
    """Represents a specific voting preference + the number of voters that have it """

    def __init__(self, vote):
        """Used to instantiate a Ballot and takes a str as input"""

         # split the line of the dataset into a tuple, with the number of voters and ranking
        count, alternatives_string = [x.strip() for x in vote.split(':')]
        self.count = int(count)
        self.ranking = []
        # Regex to find tied votes in the str
        alternatives = re.findall(r"\d+|{[^{}]+}", alternatives_string)
        for alternative in alternatives:
            # if tied votes, join the alternatives in a list
            if alternative.startswith('{') and alternative.endswith('}'):
                self.ranking.append(list(map(int, alternative.strip('{}').split(','))))
            else:
                self.ranking.append(int(alternative))

    def eliminate_alternative(self, alternative):
        """Removes a specified alternative from Ballot's ranking."""

        for alt in self.ranking:
            # if alternative is in a tied vote list
            if isinstance(alt, list):
                if alternative in alt:
                    self.ranking[self.ranking.index(alt)].remove(alternative)
            else:
                if alternative == alt:
                    self.ranking.remove(alternative)
            
    def get_ranking(self):
        """Getter for the Ballot's ranking."""
        return self.ranking
    
    def get_count(self):
        """Getter for the Ballot's number of voters."""

        return self.count
    
    def get_plurality(self):
        """Getter for the Ballot's top ranked alternative."""
        
        if self.ranking:
            return self.ranking[0]
        else:
            return None