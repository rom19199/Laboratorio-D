from alph_definition import AlphabetDefinition
from Operators import *
from nodes import Node
from validate_exp import Clear
from token_symbol import Symbol
class PostfixConverter:
    def __init__(self, expression, augmented_value=None, tokens_file=None):
        new_expression = []
        self.expression = expression
        self.alphabet = AlphabetDefinition()
        self.symbols = self.alphabet.getSymbolDictionary()
        self.stack_operators = []
        self.postfix_stack = []
        self.nodes_stack = []
        self.tokens_file = tokens_file
        temp_number = ''
        print('INGRESIING TO CONVERTER',self.expression, len(self.expression))
        for i in range(len(self.expression)):
            if self.expression[i] not in self.symbols and self.expression[i] != Symbol('#').name:
                temp_number += self.expression[i]
            elif self.expression[i] in self.symbols and temp_number != '':
                new_expression.append(temp_number)
                new_expression.append(self.expression[i])
                temp_number = ''
            else:
                new_expression.append(self.expression[i])

        if augmented_value is None:
             self.expression = new_expression
        else:
            print('Adding')
            self.expression = '('+expression+')' + augmented_value
            new_expression = []
            temp_number = ''
            for i in range(len(self.expression)):
                if self.expression[i] == '#':
                    new_expression.append(augmented_value)
                elif self.expression[i] not in self.symbols and self.expression[i] != Symbol('ε').name and len(temp_number) <3:
                    temp_number += self.expression[i]
                elif self.expression[i] in self.symbols and temp_number != '' and len(temp_number) == 3:
                    new_expression.append(temp_number)
                    new_expression.append(self.expression[i])
                    temp_number = ''
                elif self.expression[i] not in self.symbols and self.expression[i] != Symbol('ε').name and len(temp_number) == 3:
                    new_expression.append(temp_number)
                    temp_number = ''
                    temp_number += self.expression[i]
                else:
                    new_expression.append(self.expression[i])
            self.expression = new_expression



    def build_Alphabet(self):
        for i in self.expression:
            if i not in self.symbols and i != Symbol('ε').name and i !='#':
                self.alphabet.addSymbol(Symbol(i, True))
            else:
                if i == '#':
                    self.alphabet.addSymbol(Symbol(i))
        return self.alphabet


    def convertToPostfix(self,validate):
    
        self.expression = Clear(self.expression,self.symbols).preprocess()
        #print('PREPROCESSED',self.expression)
        arr_preprocessed = self.expression
        #Iterate through the expression
        print(''.join(self.expression))
        print('LENGTH',len(self.expression))
        for i in arr_preprocessed:
            #print('ENTRY',i,self.stack_operators)
            #check if it is an alphabet symbol
            if i not in self.symbols:
                #print('IM HERE APPENDING STACK',i)
                self.postfix_stack.append(i)
                #print('STACK',self.postfix_stack)
            #Check if the character is an operator
            elif i in self.symbols:
                #print('OPERATOR',i)
                if len(self.stack_operators) == 0:
                    #print('STACK OPERATORS EMPTY',self.stack_operators)
                    self.stack_operators.append(i)
                    #print('STACK OPERATORS',self.stack_operators)
                #check if it is (
                elif i == LeftParenthesis().symbol:
                    self.stack_operators.append(i)
                #check if it is ) and empty the stack until (
                elif i == RightParenthesis().symbol:
                    #print('RIGHT PARENTHESIS',self.stack_operators)
                    while self.stack_operators[-1] != LeftParenthesis().symbol:
                        self.postfix_stack.append(self.stack_operators.pop())
                    self.stack_operators.pop()
                else:
                    #while the precedence is less or equal

                    while len(self.stack_operators) != 0 and self.symbols[i].precedence <= self.symbols[self.stack_operators[-1]].precedence:
                        self.postfix_stack.append(self.stack_operators.pop())
                    self.stack_operators.append(i)
            #print("SALIR DEL FOR")
        #Empty the stack
        while len(self.stack_operators) != 0:

            self.postfix_stack.append(self.stack_operators.pop())
        validate = True
        #postfix = (''.join(self.postfix_stack))
        postfix = self.postfix_stack
        return (postfix, validate)

    def make_nodes(self,expression):
        for i in range(len(expression)):
            i = expression[i]
            #check if it is an alphabet symbol
            if i not in self.symbols:

                self.nodes_stack.append(Node(i))
            else:
                    #check if it is a *
                    if i == KleeneStar().symbol:
                        node = Node(i)
                        node.left = self.nodes_stack.pop()
                        self.nodes_stack.append(node)
                    #check if it is a |
                    elif i == Union().symbol:
                        node = Node(i)
                        node.right = self.nodes_stack.pop()
                        node.left = self.nodes_stack.pop()
                        self.nodes_stack.append(node)
                    #check if it is a .
                    elif i == Concatenation().symbol:
                        node = Node(i)
                        node.right = self.nodes_stack.pop()
                        node.left = self.nodes_stack.pop()
                        self.nodes_stack.append(node)
                    #check if it is a ?
                    elif i == QuestionMark().symbol:
                        node = Node(i)
                        node.left = self.nodes_stack.pop()
                        self.nodes_stack.append(node)
                    #check if it is a +
                    elif i == PositiveClosure().symbol:
                        node = Node(i)
                        node.left = self.nodes_stack.pop()
                        self.nodes_stack.append(node)

        root = self.nodes_stack.pop()
        Node.tokens_list = self.tokens_file
        return root
