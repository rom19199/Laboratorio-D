from Automata import Automata
from token_symbol import Symbol
import copy
from state_definition import State

class DFA_automata(Automata):
    def __init__(self, states, alphabet, transitions, initial, finals,tokens_list=None):
        super().__init__(states, alphabet, transitions, initial, finals)
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions[0]
        self.initial = initial
        self.finals = finals
        self.tokens_list = tokens_list
        self.identified_tokens = []


    def move(self, state, symbol):
        #print('TRANS',self.transitions)
        #print('STATE',state)
        #print('SYMBOL',symbol)
        if state in self.transitions:
            if symbol in self.transitions[state]:
                 #print('TRANSICION STATES',self.transitions[state][symbol])
                 return self.transitions[state][symbol][0]
            else:
                return None
        else:
            return None
    def simulate_dfa(self,word):
        s0 = self.initial
        last_acceptance_state = None
        counter_symbol = 0
        last_index_acceptance = 0
        while counter_symbol < len(word):
            symbol = word[counter_symbol]
            if len(str(ord(symbol))) == 1:
                symbol = ('00' + str(ord(symbol)))
            elif len(str(ord(symbol))) == 2:
                symbol = ('0' + str(ord(symbol)))
            else:
                symbol = str(ord(symbol))
            s0 = self.move(s0, symbol)
            if s0 != None:
                #print('HAY  TRANSICION')
                if s0 in self.finals:

                    last_acceptance_state = s0
                    counter_symbol += 1
                    last_index_acceptance = counter_symbol
                else:
                    counter_symbol += 1
            elif s0 == None and last_acceptance_state != None:
                #print('NO',last_acceptance_state)
                #print('LEAF LAST',last_acceptance_state.leaf_id)
                self.search_idx(last_acceptance_state.leaf_id)
                #reinicio el automata
                s0 = self.initial
                last_acceptance_state = None
                counter_symbol = last_index_acceptance
            else:
                error= 'NO VALID STRING '+chr(int(symbol))
                self.identified_tokens.append(error)
                counter_symbol += 1
                s0 = self.initial

        #check the last acceptance state if it is not empty
        if last_acceptance_state != None:
            #print('LEAF LAST',last_acceptance_state.leaf_id)
            self.search_idx(last_acceptance_state.leaf_id)

    def search_idx(self,leaf_id):
        for i in self.tokens_list:
            if i.id_leaf == leaf_id:
                #print('TOKEN',i.token)
                #print(i.definition.strip())
                #print('a=4\nprint(a)'==i.definition.strip())
                self.identified_tokens.append(i)

    def get_identified(self):
        return self.identified_tokens

    def get_list_tokens(self):
        #get the values of the tokens
        list_tokens = []
        for i in self.tokens_list:
            list_tokens.append(i.token)
        return list_tokens