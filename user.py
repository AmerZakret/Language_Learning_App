class User:

    #Initialize the User object.
    def __init__(self, name, password):
        self.name = name
        self.password = password

    #Convert the User object to a dictionary.
    def to_dict(self):
        return {
            "name": self.name,
            "password": self.password
        }
