import re 

# This class represents a specific voting preference + the number of voters that have it
class Ballot:
    
    def __init__(self, vote):
        count, alternatives_string = [x.strip() for x in vote.split(':')]
        self.count = int(count)
        self.ranking = []
        # Idk how to handle the tied votes (I assume?) so I just remove them for now
        alternatives = re.findall(r"\d+|{[^{}]+}", alternatives_string)
        self.ranking_map = {}

        for idx, alternative in enumerate(alternatives):
            if alternative.startswith('{') and alternative.endswith('}'):
                alts = list(map(int, alternative.strip('{}').split(',')))
                self.ranking.append(alts)
                self.ranking_map[alts[0]] = idx
                self.ranking_map[alts[1]] = idx
            else:
                self.ranking.append(int(alternative))
                self.ranking_map[int(alternative)] = idx

    # Eliminate the specified alternative
    def eliminate_alternative(self, alternative):
        for alt in self.ranking:
            if isinstance(alt, list):
                if alternative in alt:
                    self.ranking[self.ranking.index(alt)].remove(alternative)
            else:
                if alternative == alt:
                    self.ranking.remove(alternative)
                    # make sure it is the lowest ranked in the order
                    self.ranking_map[alternative] = len(self.ranking)
            
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
        if self.ranking_map[alt1] < self.ranking_map[alt2]:
            return alt1
        elif self.ranking_map[alt2] < self.ranking_map[alt1]:
            return alt2
        return None