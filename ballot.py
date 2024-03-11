import re 

class Ballot:
    """Represents a specific voting preference + the number of voters that have it """

    def __init__(self, vote):
        """Used to instantiate a Ballot and takes in a str/tuple/list"""
        if type(vote) == str:
            # split the line of the dataset into a tuple, with the number of voters and ranking
            count, alternatives = [x.strip() for x in vote.split(':')]
            self.count = int(count)
            # remove tied votes
            alternatives = alternatives.replace('{', '').replace('}', '')
            self.ranking = list(map(int, alternatives.split(',')))
        elif type(vote) in [list, tuple]:
            self.count = 1
            self.ranking = list(vote)

    def eliminate_alternative(self, alternative):
        """Removes a specified alternative from Ballot's ranking."""
        if alternative in self.ranking:
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
        
    def compare_alternatives(self, alt1, alt2):
        """Method to compare two alternatives and return the more preferred one for this Ballot"""
        # Check if both alternatives are in Ballot ranking
        if alt1 in self.ranking:
            if alt2 in self.ranking:
                # Compare preference by comparing index
                if self.ranking.index(alt1) < self.ranking.index(alt2):
                    return alt1
                elif self.ranking.index(alt2) < self.ranking.index(alt1):
                    return alt2
            # return 1 since 2 not in Ballot but 2 is
            else: return alt1
        # Return 2 since 1 not in Ballot but 2 is
        elif alt2 in self.ranking: return alt2
        # return None since 1 and 2 not in Ballot
        else: return None
        
    def __eq__(self, other): 
        """This method compares the rankings of Ballots"""
        if not isinstance(other, Ballot):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.ranking == other.ranking

    def __hash__(self):
        """Converts the Ballot's ranking and number of voters to a hash"""
        return hash((self.count, tuple(self.ranking)))