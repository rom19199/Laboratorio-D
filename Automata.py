from graphviz import Digraph
class Automata():
    def __init__(self, states, alphabet, transitions, initial, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

    #visualize the automata with graphviz
    def visualize(self):
        graph_dot = Digraph('automata1',format='pdf')
        graph_dot.attr(rankdir='LR')
        for state in self.states:
            if state.is_initial and state.is_final==False: #CORRECCION EPSILON
                graph_dot.node(state.name, state.name, shape='circle')
            elif state.is_final:
                graph_dot.node(state.name, state.name, shape='doublecircle')

        for transition in self.transitions:
            for symbol in self.transitions[transition]:

                for transition_final in self.transitions[transition][symbol]:
                    #print('trans',transition_final)
                    graph_dot.edge(transition.__str__(),transition_final.__str__(),label=str(symbol))

        graph_dot.render(directory='test-output',view=True)