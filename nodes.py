#Node for the automata
from state_definition import State
from afn import AFN_automata
from dfa import DFA_automata
from alph_definition import AlphabetDefinition
from Operators import *
import uuid
from token_symbol import Symbol

class Node():
    leaf_node = []
    counter_leaf = 0
    tokens_list = None
    counter_hash = 0
    def __init__(self, value):
        self.value = value
        self.id = uuid.uuid4().hex
        self.left = None
        self.right = None
        self.automata = []
        self.symbols = AlphabetDefinition().getSymbolDictionary()
        self.label_leaf = None
        self.null_node = None
        self.follow = dict()
        self.counter_hash = 0


    def make_alphabetic_automata(self,node):
        #make automata for an alphabet symbol
        state1 = State(True,False)
        state2 = State(False,True)
        transition = dict()
        #automata = AFN_automata([state1,state2],[Symbol(node.value).ascii_repr],[transition],state1,state2)
        automata = AFN_automata([state1,state2],[Symbol(node.value).name],[transition],state1,state2)

        #automata.make_movement(Symbol(node.value).ascii_repr, state1, state2)
        automata.make_movement(Symbol(node.value).name, state1, state2)

        return automata

    def make_or_automata(self,a1,a2):
        #make automata for or operator
        state1 = State(True,False)
        state2 = State(False,True)
        #epsilon = Symbol('ε').ascii_repr
        epsilon = Symbol('ε').name
        automatas = [a1,a2]
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)

        automata.make_movement(epsilon,state1, a1.initial)
        a1.make_movement(epsilon,a1.finals, state2)

        automata.make_movement(epsilon,state1, a2.initial)
        a2.make_movement(epsilon,a2.finals, state2)

        for i in range(len(automatas)):
            i = automatas[i]
            i.finals.is_final=False

            #add transition from automata i to the automata
            for j in i.transitions:
                transition_dict = i.transitions[j]
                for symbol in transition_dict:
                    symbol_dict = transition_dict[symbol]
                    for state in symbol_dict:
                        automata.make_movement(symbol,j, state)
        return automata

    def make_kleene_automata(self,a1):
        #make automata for kleene star operator
        state1 = State(True,False)
        state2 = State(False,True)
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)
        #epsilon = Symbol('ε').ascii_repr
        epsilon = Symbol('ε').name
        automata.make_movement(epsilon,state1, a1.initial)
        automata.make_movement(epsilon,state1, state2)
        a1.make_movement(epsilon,a1.finals, state2)
        a1.make_movement(epsilon,a1.finals, a1.initial)

        a1.finals.is_final=False

        #add transition from automata i to the automata
        for j in a1.transitions:
            transition_dict = a1.transitions[j]
            for symbol in transition_dict:
                symbol_dict = transition_dict[symbol]
                for state in symbol_dict:
                    automata.make_movement(symbol,j, state)
        return automata

    def make_concatenation_automata(self,a2,a1):
        #make automata for concatenation operator
        automatas = [a1,a2]
        state1 = a1.initial
        state2 = a2.finals
        transition = dict()
        automata = AFN_automata([state1,state2],[],[transition],state1,state2)

        state_join = None
        #add transition from automata i to the automata
        for iterator in range(len(automatas)):
            if iterator == 0:
                state_join = a1.finals
                a1.finals.is_final=False
                state_join.is_final=False
            i = automatas[iterator]
            states_count = 0
            for j in i.transitions:

                transition_dict = i.transitions[j]
                for symbol in transition_dict:

                    symbol_dict = transition_dict[symbol]

                    for state in symbol_dict:
                        if iterator==1 and states_count==0:
                            automata.make_movement(symbol,state_join, state)
                        else:
                            automata.make_movement(symbol,j, state)
                    states_count+=1
        return automata


    #Postorder traversal
    def make_postorder(self):
        #make postorder and save it in array
        postorder = []
        if self.left:
            postorder = self.left.make_postorder()
        if self.right:
            postorder = postorder + self.right.make_postorder()

        postorder.append(self)
        return postorder

    def label_leafs(self):
        postorder = []

        if self.left:
            postorder = self.left.label_leafs()
        if self.right:
            postorder = postorder + self.right.label_leafs()

        if self.left == None and self.right == None:
            #evaluate if it is epsilon
            if self.value == Symbol('ε').name:
                 #Node.leaf_node.append(self)  #PREGUNTAR!!!!!
                 pass
            else:
                self.label_leaf = Node.counter_leaf
                if self.value == Symbol('#').name:
                    print(
                     'counter_tokens: ',Node.counter_hash,
                     "tokens list: ",Node.tokens_list[Node.counter_hash].token,
                    )
                    Node.tokens_list[Node.counter_hash].id_leaf = self.label_leaf
                    Node.counter_hash+=1
                Node.counter_leaf+=1
                Node.leaf_node.append(self)

        postorder.append(self)
        return postorder


    def make_rules(self,nodes_labeled):
        #calculate nullable
        #fill followpos dictionary with empty sets of leafs
        for i in Node.leaf_node:
            self.follow[i.label_leaf]  = set()

        for i in range(len(nodes_labeled)):
            i = nodes_labeled[i]
            i.null_node = self.nullable(i)
            i.firstpos = self.firstpos(i)
            i.lastpos = self.lastpos(i)
            if i.value == KleeneStar().symbol:
                for j in i.lastpos:
                    self.follow[j] = self.follow[j].union(i.firstpos)
            if i.value == Concatenation().symbol:
                for j in i.left.lastpos:
                    self.follow[j] = self.follow[j].union(i.right.firstpos)


    def lastpos(self,node):
        if node.value == Symbol('ε').name:
            return set()
        if node.label_leaf != None:
            return set([node.label_leaf])
        if node.value == Union().symbol:
            return self.lastpos(node.left).union(self.lastpos(node.right))
        if node.value == Concatenation().symbol:
            if self.nullable(node.right):
                return self.lastpos(node.left).union(self.lastpos(node.right))
            else:
                return self.lastpos(node.right)
        if node.value == KleeneStar().symbol:
            return self.lastpos(node.left)

    def firstpos(self,node):
        if node.value == Symbol('ε').name:
            return set()
        if node.label_leaf != None:
            return set([node.label_leaf])
        if node.value == Union().symbol:
            return self.firstpos(node.left).union(self.firstpos(node.right))
        if node.value == Concatenation().symbol:
            if self.nullable(node.left):
                return self.firstpos(node.left).union(self.firstpos(node.right))
            else:
                return self.firstpos(node.left)
        if node.value == KleeneStar().symbol:
            return self.firstpos(node.left)

    def nullable(self, node):
        if node.value == Symbol('ε').name:
            return True
        if node.label_leaf != None:
            return False
        if node.value == Union().symbol:
            return self.nullable(node.left) or self.nullable(node.right)
        if node.value == Concatenation().symbol:
            return self.nullable(node.left) and self.nullable(node.right)
        if node.value == KleeneStar().symbol:
            return True

    #Read each node
    def make_automata(self,nodes_postorder):
        for i in range(len(nodes_postorder)):
            i = nodes_postorder[i]
            #check if it is an alphabet symbol
            if i.value not in self.symbols:

                self.automata.append(self.make_alphabetic_automata(i))
            if i.value == Union().symbol:
                automata1 = self.automata.pop()
                automata2 = self.automata.pop()

                self.automata.append(self.make_or_automata(automata1,automata2))
            if i.value == KleeneStar().symbol:

                automata1 = self.automata.pop()
                self.automata.append(self.make_kleene_automata(automata1))
            if i.value == Concatenation().symbol:

                automata1 = self.automata.pop()
                automata2 = self.automata.pop()
                self.automata.append(self.make_concatenation_automata(automata1,automata2))
        return self.automata.pop()


    def make_dfa_direct(self,alfabeto):
        d_states = []
        state = State()
        state.is_initial = True
        d_tran = dict()
        state.list = self.firstpos
        d_states.append(state)
        #while there is unmarked states in d_states
        while len([state for state in d_states if state.mark_dfa == False])>0:
            for state in [state for state in d_states if state.mark_dfa == False]:
                if state.mark_dfa == False:
                    state.mark_dfa = True

                    #for each symbol
                    for symbol in alfabeto:
                        #print(alfabeto)
                        if symbol != Symbol('#').name:

                            #get the set of states that can be reached from state with symbol
                            u = set()
                            for i in state.list:
                                #verify if i is equal to symbol
                                if self.leaf_node[i].value == symbol:
                                    u = u.union(self.follow[i])
                            #if u is not empty
                            if len(u)>0:

                                for statei in d_states:
                                    flag = False
                                    if statei.list == u:
                                        #add transition to state
                                        if state in d_tran:
                                            d_tran[state][symbol] = [statei]
                                        else:
                                            d_tran[state] = {symbol:[statei]}
                                        break
                                    else:
                                        flag = True
                                if flag:
                                    #create a new state
                                    new_state = State()
                                    new_state.list = u
                                    d_states.append(new_state)
                                    #make dictionary
                                    if state in d_tran:
                                        d_tran[state][symbol] = [new_state]
                                    else:
                                        d_tran[state] = {symbol:[new_state]}


                                    '''#if u is not in d_states
                                    if u not in [state.list for statei in d_states]:
                                        #create a new state
                                        new_state = State()
                                        new_state.list = u
                                        d_states.append(new_state)
                                        #make dictionary
                                        if state in d_tran:
                                            d_tran[state][symbol] = [new_state]
                                        else:
                                            d_tran[state] = {symbol:[new_state]}
                                    #if u is in d_states
                                    else:
                                        #add transition to state
                                        if state in d_tran:
                                            d_tran[state][symbol] = statei
                                        else:
                                            d_tran[state] = {symbol:i}'''

        #print('DTRAN DFA',d_tran)
        #print('DSTATES DFA',d_states)

        #get final states
        final_states = []
        #evaluate if there is # symbol
        # print('NODEEE')
        # for i in Node.leaf_node:
        #     print('NODEEE',i.value)

        #print('DSTATES AA')
        # for state in d_states:
        #     print(state.name)
        for state in d_states:
            #print('STATE LIST AAAAA',state.list)
            for i in state.list:
                #print('IIII',i,self.leaf_node[i].value)
                if Node.leaf_node[i].value == Symbol('#').name:
                    #print('FINAL',state, self.leaf_node[i].value)
                    state.is_final = True
                    state.leaf_id = i
                    #print('STATE ID',state.leaf_id)
                    final_states.append(state)
                    break


        #create dfa
        dfa = DFA_automata(d_states,alfabeto,[d_tran],d_states[0],final_states,Node.tokens_list)
        return dfa






