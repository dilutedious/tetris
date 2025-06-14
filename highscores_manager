from settings import *

class HighScoreManager:
    def __init__(self):
        self.filepath = HIGHSCORES
        self.scores = self.load_scores()
    
    def load_scores(self):
        try:
            with open(self.filepath, 'r') as f:
                scores = []
                for line in f:
                    try:
                        name, score = line.strip().split(',')
                        scores.append((int(score), name))
                    except ValueError:
                        continue # skip any error lines...
                scores.sort(key=lambda x: x[0], reverse=True) # sort by scores, highest score comes first
                return scores[:20] # return top 20
        except FileNotFoundError:
            return []
    
    def save_scores(self):
        with open(self.filepath, 'w') as f:
            for score, name in self.scores:
                f.write(f"{name},{score}\n")

    def add_score(self, name, score):
        self.scores.append((score, name))
        self.scores.sort(key=lambda x: x[0], reverse=True)
        self.scores = self.scores[:20]
        self.save_scores()

    def ishighscore(self, score):
        if len(self.scores) < 20: # if fewer than 20 scores, any score qualifies as highscore.
            return True
        return score > self.scores[-1][0] # checks highest score
                        