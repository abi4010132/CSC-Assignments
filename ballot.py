import re 

# This class represents a specific voting preference + the number of voters that have it
class Ballot:
    
    def __init__(self, vote):
        count, alternatives_string = [x.strip() for x in vote.split(':')]
        self.count = int(count)
        self.ranking = []
        # Idk how to handle the tied votes (I assume?) so I just remove them for now
        alternatives = re.findall(r"\d+|{[^{}]+}", alternatives_string)
        for alternative in alternatives:
            if alternative.startswith('{') and alternative.endswith('}'):
                self.ranking.append(list(map(int, alternative.strip('{}').split(','))))
            else:
                self.ranking.append(int(alternative))

    # Eliminate the specified alternative
    def eliminate_alternative(self, alternative):
        for alt in self.ranking:
            if isinstance(alt, list):
                if alternative in alt:
                    self.ranking[self.ranking.index(alt)].remove(alternative)
            else:
                if alternative == alt:
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