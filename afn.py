from Automata import Automata
from token_symbol import Symbol
from state_definition import State
from dfa import DFA_automata
class AFN_automata(Automata):
    def __init__(self, states, alphabet, transitions, initial, finals):
        super().__init__(states, alphabet, transitions, initial, finals)
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions[0]
        self.initial = initial
        self.finals = finals

    #Se realiza la creacion de las transiciones
    def make_movement(self, symbol, state1, state2):
        #Verificar que el simbolo este en el alfabeto si no esta se agrega
        if symbol not in self.alphabet:
            self.alphabet.append(symbol)
        #Verificar los estados
        if state1 not in self.states:
            self.states.append(state1)

        if state2 not in self.states:
            self.states.append(state2)
        #verificar que el primer estado este en el diccionario
        if state1 in self.transitions:
            #verificar que el simbolo este en el diccionario
            if symbol in self.transitions[state1]:
                #agregar el segundo estado al diccionario
                self.transitions[state1][symbol].append(state2)
            else:
                #agregar el simbolo al diccionario
                self.transitions[state1][symbol] = [state2]
        else:
            #agregar el primer estado al diccionario
            self.transitions[state1] = {symbol:[state2]}
        #print(self.transitions)


    #se construye los subconjuntos para DFA
    def make_dfa(self):
        d_states = []
        state = State()
        state.is_initial = True
        d_tran = dict()
        #Se maneja como una lista dentro de un estado los epsilon closure
        state.list = self.epsilon_closure(self.initial) #Closure del estado inicial
        d_states.append(state)

        #while there is unmarked states in d_states
        while len([state for state in d_states if state.mark_dfa == False]) > 0:

            for state in [state for state in d_states if state.mark_dfa == False]:
                if state.mark_dfa == False:
                    state.mark_dfa = True
                    #for each symbol in the alphabet except epsilon
                    for symbol in self.alphabet:
                        if symbol == Symbol('ε').name: #CAMBIAR A  ASCII
                            pass
                        else:
                            U = self.epsilon_closure(self.move_dfa(state, symbol)) #devuelve lista de estados con epsilon

                            for i in d_states:
                                flag = False
                                if U == i.list: #esto es para comprobar si ya esta en d_states
                                    #make dictionary
                                    if state in d_tran:
                                        d_tran[state][symbol] = [i]
                                    else:
                                        d_tran[state] = {symbol:[i]}
                                    break
                                elif U == []:
                                    pass
                                else:
                                    flag = True
                            if flag == True: #si no esta se crea un nuevo estado
                                    new_state = State()
                                    new_state.list = U
                                    d_states.append(new_state)
                                    #make dictionary
                                    if state in d_tran:
                                        d_tran[state][symbol] = [new_state]
                                    else:
                                        d_tran[state] = {symbol:[new_state]}

        final_states = []
        #if a state in state.list has a final state of NFA
        for state in d_states:
            for state_final in state.list:
                if state_final.is_final:
                    state.is_final = True
                    final_states.append(state)

        dfa = DFA_automata(d_states, self.alphabet, [d_tran], d_states[0], final_states)
        return dfa


    def verify_epsilon_transition(self, state):
        movements_epsilon = []
        for transition in self.transitions:
            if state == transition:
                for symbol in self.transitions[state]:
                    if symbol == Symbol('ε').name: #CAMBIAR A ASCII
                        for transition_final in self.transitions[state][symbol]:
                            movements_epsilon.append(transition_final)

        return movements_epsilon

    def epsilon_closure(self, state):
        #make an stak to store the states
        stack = []
        if type(state)==State:
            iterate = set([state])
        else:
            iterate = set(state)
        e_closure = []
        for i in iterate:
            stack.append(i)
            #initialize the e_closure with the state
            e_closure.append(i)

        while len(stack) > 0:
            t = stack.pop()
            for u in self.verify_epsilon_transition(t):
                if u not in e_closure:
                    e_closure.append(u)
                    stack.append(u)

        return e_closure

    def move_dfa(self, state, symbol):
        #See with symbol can be reached from state
        movements = []
        #check every list of the state
        for state in state.list:
            for transition in self.transitions:
                if state == transition:
                    for symbol_transition in self.transitions[state]:
                        if symbol_transition == symbol:
                            for transition_final in self.transitions[state][symbol_transition]:
                                movements.append(transition_final)
        return movements

    def simulate_nfa(self, word):
        #make the epsilon closure of the initial state
        current_state = self.epsilon_closure(self.initial)
        #for each symbol in the word
        for symbol in word:
            #make the move
            state = State()
            state.list = current_state
            current_state = self.move_dfa(state, symbol)

            #make the epsilon closure
            current_state = self.epsilon_closure(current_state)
        #if the current state is a final state
        for state in current_state:
            if state.is_final:
                return True
        return False


