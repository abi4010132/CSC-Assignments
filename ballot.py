# This class represents a specific voting preference + the number of voters that have it
class Ballot:
    
    def __init__(self, vote):
        count, alternatives = [x.strip() for x in vote.split(':')]
        self.count = int(count)
        # Idk how to handle the tied votes (I assume?) so I just remove them for now
        alternatives = alternatives.replace('{', '').replace('}', '')
        self.ranking = list(map(int, alternatives.split(',')))

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