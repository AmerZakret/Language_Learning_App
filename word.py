
class Word:

    #Initialize the User object.
    def __init__(self, word, meaning):
        self.word = word
        self.meaning = meaning

    #Convert the User object to a dictionary.
    def to_dict(self):
        return {
            "word": self.word,
            "meaning": self.meaning
        }
