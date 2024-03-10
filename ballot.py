import re 

# This class represents a specific voting preference + the number of voters that have it
class Ballot:
    
    def __init__(self, vote):
        if type(vote) == str:
            count, alternatives = [x.strip() for x in vote.split(':')]
            self.count = int(count)
            # Idk how to handle the tied votes (I assume?) so I just remove them for now
            alternatives = alternatives.replace('{', '').replace('}', '')
            self.ranking = list(map(int, alternatives.split(',')))
        elif type(vote) in [list, tuple]:
            self.count = 1
            self.ranking = list(vote)

    # Eliminate the specified alternative
    def eliminate_alternative(self, alternative):
        if alternative in self.ranking:
            self.ranking.remove(alternative)
            
    # Getter for voting preference
    def get_ranking(self):
        return self.ranking
    
    # Getter for number of voters
    def get_count(self):
        return self.count
    
    # Getter for plurality winner of ballot
    def get_plurality(self):
        if self.ranking:
            return self.ranking[0]
        else:
            return None
        
    # out of two alternatives, pick the more preferred one according to this ballot
    def compare_alternatives(self, alt1, alt2):
        if alt1 in self.ranking:
            if alt2 in self.ranking:
                if self.ranking.index(alt1) < self.ranking.index(alt2):
                    return alt1
                elif self.ranking.index(alt2) < self.ranking.index(alt1):
                    return alt2
            else: return alt1
        elif alt2 in self.ranking: return alt2
        else: return None
        
    def __eq__(self, other): 
        if not isinstance(other, Ballot):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.ranking == other.ranking

    def __hash__(self):
        return hash((self.count, tuple(self.ranking)))