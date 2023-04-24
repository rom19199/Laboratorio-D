class Operator():
    def __init__(self, symbol, precedence, associativity):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity

#Make kleene star operator
class KleeneStar(Operator):
    def __init__(self):
        super().__init__('*', 3, 'right')

    def valid_operation(self,expression):
        flag = True
        counter = 0
        expression_len = len(expression)
        flag = True
        counter = 0
        err_msg = ''
        expression = list(expression)
        expression_len = len(expression)
        index = expression.index(self.symbol)

        while flag and expression_len>0:
            if counter == 0 and expression[counter] == self.symbol:
                flag = False
                err_msg = "Error: Expected one symbol before the kleene star operator at position "+str(index)
            elif expression[counter] == self.symbol:
                if expression[:index][-1] == Union().symbol:
                    err_msg = "Error: Invalid expression at position "+str(index)
                    flag = False
            counter += 1
            expression_len -= 1

        return flag,err_msg

#Make concatenation operator
class Concatenation(Operator):
    def __init__(self):
        super().__init__('.', 2, 'left')

#Make union operator
class Union(Operator):
    def __init__(self):
        super().__init__('|', 1, 'left')

    def valid_operation(self,expression,alphabet):
        flag = True
        counter = 0
        expression = list(expression)
        error_msg = ''
        expression_len = len(expression)
        index = expression.index(self.symbol)

        while flag and expression_len>0:
            if counter == 0 and expression[counter] == self.symbol:
                flag = False
                error_msg ="Error: Expected one symbol before the union operator at position "+str(index)
            elif expression[counter] == self.symbol and expression_len == 1:
                flag = False
                error_msg ="Error: Expected one symbol after the union operator at position "+str(index)
            elif expression[counter] == self.symbol:
                index = counter
                if expression[:index][-1] == self.symbol:
                    error_msg = "Error: Invalid expression at position "+str(index)
                    flag = False
                elif expression[index+1:][0] == self.symbol or (expression[index+1:][0] != (LeftParenthesis().symbol) and expression[index+1:][0] in alphabet):
                    error_msg = "Error: Invalid expression at position "+str(index+1)
                    flag = False
            counter += 1
            expression_len -= 1

        return flag,error_msg

#Make left parenthesis operator
class LeftParenthesis(Operator):
    def __init__(self):
        super().__init__('(', 0, None)

#Make right parenthesis operator
class RightParenthesis(Operator):
    def __init__(self):
        super().__init__(')', 0, None)

#Make question mark operator
class QuestionMark(Operator):
    def __init__(self):
        super().__init__('?', 3, 'right')

    def get_representation(self, symbol):
        #return (a|ε)
        if len(symbol) == 1:
            return '('+symbol+Union().symbol+Epsilon().symbol+')'
        else:
            return '('+'('+symbol+')'+Union().symbol+Epsilon().symbol + ')'

    def valid_operation(self,expression):
        flag = True
        counter = 0
        expression_len = len(expression)
        flag = True
        counter = 0
        expression = list(expression)
        expression_len = len(expression)
        index = expression.index(self.symbol)
        err_msg = ''

        while flag and expression_len>0:
            if counter == 0 and expression[counter] == self.symbol:
                flag = False
                err_msg = "Error: Expected one symbol before the question mark operator at position "+str(index)
            elif expression[counter] == self.symbol:
                if expression[:index][-1] == Union().symbol:
                    err_msg = "Error: Invalid expression at position "+str(index)
                    flag = False
            counter += 1
            expression_len -= 1

        return flag,err_msg


#Positive closure operator
class PositiveClosure(Operator):
    def __init__(self):
        super().__init__('+', 3, 'right')

    def get_representation(self, symbol):
        if len(symbol) == 1:
            return '('+symbol+symbol+KleeneStar().symbol+')'
        else:
            return '('+'('+symbol+')'+'('+symbol+')'+KleeneStar().symbol+')'

    def valid_operation(self,expression):
        flag = True
        counter = 0
        expression_len = len(expression)
        flag = True
        counter = 0
        err_msg = ''
        expression = list(expression)
        expression_len = len(expression)
        index = expression.index(self.symbol)
        while flag and expression_len>0:
            if counter == 0 and expression[counter] == self.symbol:
                flag = False
                err_msg = "Error: Expected one symbol before the positive closure operator at position "+str(index)
            elif expression[counter] == self.symbol:
                if expression[:index][-1] == Union().symbol:
                    err_msg = "Error: Invalid expression at position "+str(index)
                    flag = False
            counter += 1
            expression_len -= 1

        return flag,err_msg

#Make epsilon operator
class Epsilon(Operator):
    def __init__(self):
        super().__init__('ε', 0, None)
