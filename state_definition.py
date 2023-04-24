class State():
    counter = 0
    def __init__(self, is_initial=False, is_final=False):
        self.name = str(State.counter)
        State.counter += 1

        self.is_initial = is_initial
        self.is_final = is_final
        self.leaf_id = None
        self.mark_dfa = False
        self.list = []

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.name