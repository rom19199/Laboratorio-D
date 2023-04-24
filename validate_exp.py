from Operators import *
from token_symbol import Symbol
class Clear():
    def __init__(self, expression,symbols):
        self.expression = expression
        self.symbols = symbols

    #Validar que la cantidad de parentesis este balanceada
    def validate_expression_parenthesis(self):
        opening_parenthesis = [LeftParenthesis().symbol]
        closing_parenthesis = [RightParenthesis().symbol]
        counter_parenthesis = 0
        positions_opening = []
        positions_closing = []

        for i in range(len(self.expression)):
            if self.expression[i] in opening_parenthesis:
                counter_parenthesis += 1
                positions_opening.append(i)
            elif self.expression[i] in closing_parenthesis:
                counter_parenthesis -= 1
                if positions_opening != []:
                    positions_opening.pop()
                else:
                    positions_closing.append(i) #hay mas derechos que izquierdos
        if counter_parenthesis != 0:

            if positions_opening != []:

                return False, "Error: Missing closing parenthesis of parenthesis in position " + ','.join(map(str, positions_opening))
            elif positions_closing != []:
                return False, "Error: Missing opening parenthesis of parenthesis in position " + ','.join(map(str, positions_closing))
        else:
            return True, ""

        #validate if inside parentheses there is a symbol
    def validate_expression_inside_parenthesis(self,alphabet):
        flag_parenthesis = True
        if alphabet == []:
             flag_parenthesis = False
        else:
            inside = []
            new_expression = list(self.expression)

            while len(new_expression) > 0 :

                value = new_expression[-1]

                if value == RightParenthesis().symbol:
                    counter_R = 0 #Count if there are more than one parenthesis
                    counter_L = 0
                    new_expression.pop()

                    #iterate until you find the left parenthesis
                    while len(new_expression) > 0:
                        value = new_expression[-1]
                        if value != LeftParenthesis().symbol and value != RightParenthesis().symbol:
                            inside.append(new_expression.pop())
                        elif value == LeftParenthesis().symbol and counter_R == counter_L:
                            new_expression.pop()
                            break
                        elif value == LeftParenthesis().symbol and counter_R != counter_L:
                            counter_L += 1
                            inside = inside[::-1] #reverse the list

                            if inside[0] == RightParenthesis().symbol:
                                inside = []
                                break
                            else:
                                inside.append(new_expression.pop())
                        else:
                            counter_R += 1
                            inside.append(new_expression.pop())

                    if inside == []:
                        flag_parenthesis = False
                        break
                    else:
                        flag_parenthesis = True
                    inside = []

                if flag_parenthesis == False:
                    break
                elif flag_parenthesis == True and len(new_expression) > 0:
                    new_expression.pop()
        if flag_parenthesis == False:
            return flag_parenthesis, "Error: Empty parenthesis"
        else:
         return flag_parenthesis, ""

    #Valida las necesidades de cada operador
    def validate_expression_operators(self):
        operators = [KleeneStar().symbol, Concatenation().symbol, Union().symbol, QuestionMark().symbol, PositiveClosure().symbol]
        flag_operator = True
        error = ""
        for i in range(len(self.expression)):
            if self.expression[i] in operators and flag_operator ==True:
                if self.expression[i] == Union().symbol:

                    #check if has a symbol before and after
                    flag_operator,error = Union().valid_operation(self.expression,self.symbols)
                elif self.expression[i] == KleeneStar().symbol:

                    flag_operator,error = KleeneStar().valid_operation(self.expression)

                elif self.expression[i] == QuestionMark().symbol:
                    flag_operator,error = QuestionMark().valid_operation(self.expression)
                elif self.expression[i] == PositiveClosure().symbol:

                    flag_operator,error = PositiveClosure().valid_operation(self.expression)
            elif flag_operator == False:
                break
            else:
                pass
        return flag_operator,error



    #Realiza la transformacion dependiendo del symbol
    def clean_special_operators(self,symbol, new_expression):
        #pop the symbol
        new_expression.pop()
        a = []
        inside = []
        external_letters = []

        while len(new_expression) > 0 :
            value = new_expression[-1]
            #evaluate value not in symbols
            if value != RightParenthesis().symbol:
                if inside != []: #demas letras
                    external_letters.append(new_expression.pop())
                #evaluate if the value is not a symbol
                elif value not in self.symbols:

                    a.append(new_expression.pop())
                    break
                else:
                    a.append(new_expression.pop())

            elif value == RightParenthesis().symbol:
                counter_R = 0 #Count if there are more than one parenthesis
                counter_L = 0
                new_expression.pop()

                #iterate until you find the left parenthesis
                while len(new_expression) > 0:
                    value = new_expression[-1]
                    if value != LeftParenthesis().symbol and value != RightParenthesis().symbol:
                        inside.append(new_expression.pop())
                    elif value == LeftParenthesis().symbol and counter_R == counter_L:
                        new_expression.pop()
                        break
                    elif value == LeftParenthesis().symbol and counter_R != counter_L:
                        counter_L += 1
                        inside.append(new_expression.pop())
                    else:
                        counter_R += 1
                        inside.append(new_expression.pop())
                inside = list((symbol.get_representation(''.join(reversed(inside)))))
                new_expression = new_expression + inside
                break
            else:
                pass
        if a != []:
            #make conversion
            conversion = list((symbol.get_representation(''.join(reversed(a)))))
            new_expression = new_expression + conversion

        #print('CLEANING SPECIAL OPERATOR ENDING',new_expression)
        return new_expression


    #Realiza la transformacion de los simbolos especiales
    def make_changes_operators(self):
        new_expression = []

        for i in range(len(self.expression)):
            new_expression.append(self.expression[i])
            if self.expression[i] == QuestionMark().symbol:
                #print('ENTRE QUESTION')
                new_expression = self.clean_special_operators(QuestionMark(), new_expression)
            elif self.expression[i] == PositiveClosure().symbol:
                new_expression = self.clean_special_operators(PositiveClosure(), new_expression)


        return new_expression

    #add the concatenation operator after the kleene star
    def preprocess(self):
        new_expression = []
        flag = False
        temp_number = ''
        #print('PREPOOOO',self.expression)
        #ITERATE THE EXPRESSION and find number count 2 more and create a symbol
        for i in range(len(self.expression)):
                if self.expression[i] == '#':
                    new_expression.append(self.expression[i])
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

        #print('ARRAY OF EXPRESSION: ',new_expression)
        self.expression = new_expression
        self.expression = self.make_changes_operators()

        #print('AFTER CLEANING OPERATORS: ',self.expression)
        new_expression = self.expression
        #self.expression = ''.join(self.expression)
        #print('NEWW2',self.expression)
        new_expression = []
        temp_number = ''
        #ITERATE THE EXPRESSION and find number count 2 more and create a symbol
        for i in range(len(self.expression)):
                if self.expression[i] == '#':
                    new_expression.append(self.expression[i])
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

        #print('NEWW3',new_expression)

        other = []
        other = new_expression
        new_expression = []

        for i in range(len(other)):
            #print('FOR',other[i])
            new_expression.append(other[i])

            if i < len(other) -1:
                #REVISAR CAMBIO
                if other[i] == KleeneStar().symbol or other[i]==PositiveClosure().symbol or other[i]==QuestionMark().symbol or other[i] == RightParenthesis().symbol or other[i] == Epsilon().symbol :
                    if other[i+1] != RightParenthesis().symbol and other[i+1] not in self.symbols:

                        new_expression.append(Concatenation().symbol)
                    elif other[i+1] == LeftParenthesis().symbol:

                        new_expression.append(Concatenation().symbol)
                #add concatenation operator between two alphabet symbols
                elif other[i] not in self.symbols:
                    if other[i+1] not in self.symbols and other[i+1] != RightParenthesis().symbol:

                        new_expression.append(Concatenation().symbol)
                    #add concatenation between alphabet and left parenthesis
                    elif other[i+1] == LeftParenthesis().symbol:
                        new_expression.append(Concatenation().symbol)

        return new_expression