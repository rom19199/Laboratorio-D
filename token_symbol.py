class Symbol():
    counter_id = 0
    def __init__(self, name, isAcii=False,var_ascii=None):

        #save the ascii value
        if isAcii==False:
            self.name = name
            self.ascii_repr = ord(name)
        else:
            self.name = str(name)
            Symbol.counter_id += 1
            self.ascii_repr = int(name)
