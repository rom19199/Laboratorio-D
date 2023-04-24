
from alph_definition import *
import string
from Operators import *
from token_object import TokenObject
    
class Reader():
    def __init__(self, path):
        self.path = path
        self.text = ""
        self.definitions = []
        self.current_char = None
        self.next_char = None
        self.actual_line = None
        self.pos = 0
        self.definitions = {}
        self.comments = []
        self.current_string = ''
        self.temp_array = []
        self.symbols = AlphabetDefinition().getSymbolDictionary()
        self.rule_stack = {}
        self.token_name = ''
        self.processing_tokens = False
        self.regex = ''
        self.valid_scapes = ['n','t','r','v','f','a','b','\\','\'','"']
        self.comment_inside = ''
        self.second_temp_array = []
        self.file_string = ''
        self.counter_increment = 0
        self.actions = {}
        self.tokens_file = []
        self.header = '' #PREGUNTA PORQUE SINO SE PASA A ARRAY
        self.trailer = ''
        self.actual_tok = None
        self.errors = []
        self.isError = False
        self.temp_name = ''

    def read_file(self):
        #read line by line
        with open(self.path, 'r') as file:
            for line in file:
                #add to the file string
                self.file_string += line
            self.process_file()
            if len(self.errors) > 0:
                for error in self.errors:
                    print((error))
                return False
            else:
                print('MEGA STRING',self.file_string)
                print('COMMENTS',self.comments)
                print('TOKENS',self.rule_stack)
                print('DEFINITION',self.definitions)
                print('ACTIONS',self.actions)
                self.header = self.comments[0]
                self.trailer = self.comments[-1]
                print('HEADER',self.header)
                print('TRAILER',self.trailer)
                return True


    '''
    Este metodo recorre el diccionario de tokens y arma el string
    '''
    def get_tokens_expression(self):
        for key in self.rule_stack:
            for i in self.rule_stack[key]:
                #if it is not the last element
                if i != self.rule_stack[key][-1]:
                    self.regex += '('+i+')' + '#'+'|'
                else:
                    self.regex += '('+i+')'+'#'
        print("FINAL REGEX: ",self.regex)
        return self.regex

    #Este metodo procesa cada linea y se verifica si es de tokens o no
    def process_file(self):
        #Recorrer string
        i = 0
        #print('LEN',len(self.file_string))
        while i < len(self.file_string):
            self.current_char = self.file_string[i]
            if self.processing_tokens:
                self.actual_tok = None
                self.process_token()
                i = self.pos
            else:
                #Caso en que se encuentre un comentario
                if self.current_char == '(' and self.get_next_char(self.file_string,self.pos) == '*':
                    self.comment()
                    self.comments.append(self.current_string)
                    self.current_string = ''
                #Caso en que se encuentre un let
                elif self.current_char == 'l' and self.get_next_char(self.file_string,self.pos) == 'e' and self.get_next_char(self.file_string,self.pos + 1) == 't' and self.get_next_char(self.file_string,self.pos + 2) == ' ':
                    self.process_definition()
                #Caso en que se encuentre un rule
                elif self.current_char == 'r' and self.get_next_char(self.file_string,self.pos) == 'u' and self.get_next_char(self.file_string,self.pos+1) == 'l' and self.get_next_char(self.file_string,self.pos+2) == 'e':
                    self.process_rule()
                    self.processing_tokens = True
                # if self.current_char == '{':
                #     self.header = self.process_action(False)
                elif self.current_char == '\n' or self.current_char == ' ' or self.current_char == '\t':
                    pass
                else:
                    self.errors.append('ERROR: Invalid syntax')
                    #ignore until the end of the line
                    while self.current_char != '\n':
                        self.current_char = self.get_next_char(self.file_string,self.pos)
                        self.pos += 1

                self.pos += 1
                i = self.pos

    '''
    Metodo que procesa al encontrar rule
    '''
    def process_rule(self):
        self.coincidir('r')
        self.coincidir('u')
        self.coincidir('l')
        self.coincidir('e')
        self.coincidir(' ')
        self.process_name()
        key = self.current_string
        self.token_name = key
        self.current_string = ''
        self.temp_array = []
        self.coincidir(' ')
        self.coincidir('=')
        self.current_char = self.get_next_char(self.file_string,self.pos)
        self.pos += 1
        self.rule_stack[key] = []

    #Se maneja la definicion let
    def process_definition(self):
        self.coincidir('l')
        self.coincidir('e')
        self.coincidir('t')
        self.coincidir(' ')
        self.process_name()
        key = self.current_string
        self.current_string = ''
        self.temp_array = []
        self.coincidir(' ')
        self.coincidir('=')
        self.coincidir(' ')
        self.process_expression()
        #print('POSICION: ',self.pos)
        if self.isError == False:
            self.definitions[key] = self.current_string
        if self.current_char == ' ':
            self.current_char = self.get_next_char(self.file_string,self.pos)
            self.pos += 1
            if self.current_char == '(' and self.get_next_char(self.file_string,self.pos) == '*':
                self.current_string = ''
                self.comment()
                self.comments.append(self.current_string)
                self.current_string = ''
        #value = self.current_string
        self.current_string = ''
        self.isError = False

    #Obtener el nombre de variable en let
    def process_name(self):
        while self.current_char != ' ':
            self.current_string += self.current_char
            self.current_char = self.get_next_char(self.file_string,self.pos)
            self.pos += 1
            self.counter_increment += 1

    '''
    Este metodo procesa las lineas que corresponden a un let la parte de definicion
    '''
    def process_expression(self):
        while self.current_char!= '\n' and self.current_char != None:
            #Caso es un charset con comillas simples
            if self.current_char == '[' and self.get_next_char(self.file_string,self.pos) == "'":
                if self.current_string != '': #Es una expresion que ya tiene algo
                    self.process_list(False)
                else: #Es una expresion que no tiene nada
                    self.process_list()
            #Caso es un comentario
            elif self.current_char == ' ' and self.get_next_char(self.file_string,self.pos) == '(' and self.get_next_char(self.file_string,self.pos + 1) == '*':
                self.comment_inside = ''
                self.comment(init=False) #No es al inicio
                self.comments.append(self.comment_inside)
                self.comment_inside= ''
            #Caso es un charset con comillas dobles
            elif self.current_char == '[' and self.get_next_char(self.file_string,self.pos) == '"':
                if self.current_string != '': #Es una expresion que ya tiene algo
                    self.process_list(False)
                else: #Es una expresion que no tiene nada
                    self.process_list()
            #Caso es un charset con negacion
            elif self.current_char == '[' and self.get_next_char(self.file_string,self.pos) == '^':
                if self.current_string != '': #Es una expresion que ya tiene algo
                    self.process_list(False)
                else: #Es una expresion que no tiene nada
                    self.process_list()
            #Caso es una expresion con comillas simples
            elif self.current_char == "'":
                self.evaluate_single()
            #Caso es una expresion con comillas dobles
            elif self.current_char == '"':
                self.evaluate_double()
            #Caso encuentra espacio vacio
            elif self.current_char == ' ':
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            #Caso es un simbolo de regex
            elif self.current_char in self.symbols.keys() and self.current_char != Concatenation().symbol:
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            #Caso es todo ascii
            elif self.current_char == '-':
                #return all ascii
                self.get_all_ascii()
            #Caso es una diferencia de charsets
            elif self.current_char == '#' and self.get_next_char(self.file_string,self.pos) == '[':
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
                self.process_list(False,True) #Es una diferencia
                #Se hace la diferencia de charsets y se coloca en el current string
                self.current_string = list(set(self.second_temp_array) - set(self.temp_array))
                temp_string = ''
                temp_string += '('
                #join all the elements in the array with | except the last one
                temp_string += '|'.join(self.current_string)
                temp_string += ')'
                self.current_string = temp_string
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            #Es una palabra
            else:
                temp_word = ''
                while self.current_char != "'" and self.current_char != '\n' and (self.current_char not in self.symbols.keys() or self.current_char == Concatenation().symbol) and self.current_char != '[' and self.current_char != '"' and self.current_char != ' '  and self.current_char != None:
                    temp_word += self.current_char
                    self.current_char = self.get_next_char(self.file_string,self.pos)
                    self.pos += 1

                #Es una palabra que se encuentra definida previamente
                if temp_word in self.definitions.keys():
                    self.current_string += self.definitions[temp_word]
                    temp_word = ''
                else:
                    #error
                    self.errors.append('Error: La palabra ' + temp_word + ' no es reconocida')
                    self.current_string += temp_word
                    temp_word = ''
                    self.isError = True



    '''
    Este metodo procesa las lineas que se encuentran dentro de rule para obtener los tokens
    '''
    def process_token(self):
        self.actual_tok = TokenObject()
        while self.current_char != '\n' and self.current_char !=None:

            #Caso en que se encuentre un comentario
            if self.current_char == ' ' and self.get_next_char(self.file_string,self.pos) == '(' and self.get_next_char(self.file_string,self.pos + 1) == '*':
                self.comment_inside = ''
                self.comment(False)
                self.comments.append(self.comment_inside)
                self.comment_inside = ''
            #Caso en que se encuentre un comentario al inicio
            elif self.current_char == '(' and self.get_next_char(self.file_string,self.pos) == '*':
                self.comment()
                self.comments.append(self.current_string)
                self.current_string = ''
            #Caso que sea charset con comilla simple
            elif self.current_char == '[' and self.get_next_char(self.file_string,self.pos) == "'":
                if self.current_string != '': #No es al inicio que lo encuentra
                    self.process_list(False)
                else: #Lo encuentra al inicio
                    self.process_list()
                self.temp_array = []
            #Caso que sea charset con comilla doble
            elif self.current_char == '[' and self.get_next_char(self.file_string,self.pos) == '"':
                if self.current_string != '': #No es al inicio que lo encuentra
                    self.process_list(False)
                else: #Lo encuentra al inicio
                    self.process_list()
                self.temp_array = []
            elif self.current_char == '{':
                if self.isError == False:
                    if self.current_string != '' and self.temp_name == '': #No es al inicio que lo encuentra
                        self.token_name_i = self.current_string
                    elif self.temp_name != '':
                        self.token_name_i = self.temp_name
                        if self.token_name_i not in self.definitions.keys() and self.temp_name == '':
                            self.actual_tok.token = self.token_name_i
                            self.actual_tok.value = self.token_name_i
                        elif self.temp_name != '':
                            self.actual_tok.token = self.token_name_i
                            self.actual_tok.value = self.current_string

                    self.actual_tok.definition = self.process_action()
                    #print('procese acction')
                    # else:
                    #     self.trailer = self.process_action(False)
                else:
                    self.process_action(isValid=False)

            #Caso que sea charset con negacion
            elif self.current_char == '[' and self.get_next_char(self.file_string,self.pos) == '^':
                if self.current_string != '': #No es al inicio que lo encuentra
                    self.process_list(False)
                else: #Lo encuentra al inicio
                    self.process_list()
            #Caso encuentra regex con comilla simple
            elif self.current_char == "'":
                self.evaluate_single()
            #Caso encuentra regex con comilla doble
            elif self.current_char == '"':
                self.evaluate_double()
            #Caso encuentra espacio vacio
            elif self.current_char == ' ':
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            #Caso encuentra todo ascii
            elif self.current_char == '-':
                self.get_all_ascii()
            #Caso encuentra un | seguido de vacio
            elif self.current_char == '|' and self.get_next_char(self.file_string,self.pos) == ' ':
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            #Caso encuentra un simbolo de regex
            elif self.current_char in self.symbols.keys() and self.current_char != Concatenation().symbol:
                self.current_string += self.current_char
                if self.temp_name != '':
                    self.temp_name += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            #Caso encuentra una diferencia de charsets
            elif self.current_char == '#' and self.get_next_char(self.file_string,self.pos) == '[':
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
                self.process_list(False,True) #No es al inicio que lo encuentra y es una diferencia
                self.current_string = list(set(self.second_temp_array) - set(self.temp_array))
                temp_string = ''
                temp_string += '('
                #join all the elements in the array with | except the last one
                temp_string += '|'.join(self.current_string)
                temp_string += ')'
                self.current_string = temp_string
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            elif self.current_char == '\t':
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            #Es una variable
            else:
                temp_word = ''
                while self.current_char != "'" and (self.current_char not in self.symbols.keys() or self.current_char != Concatenation().symbol) and self.current_char != '[' and self.current_char != '"' and self.current_char != ' ' and self.current_char != '\n':
                    if self.current_char not in self.symbols.keys():
                        temp_word += self.current_char
                        self.current_char = self.get_next_char(self.file_string,self.pos)
                        self.pos += 1
                if temp_word in self.definitions.keys(): #Es una variable definida previamente
                    #print('es una variable')
                    if self.current_char == ' ' or self.current_char == '\n':
                        self.actual_tok.token = temp_word
                        self.current_string += self.definitions[temp_word]
                        self.actual_tok.value = self.current_string
                        self.rule_stack[self.token_name].append(self.current_string)
                        self.token_name_i = temp_word
                        temp_word = ''
                        self.current_string = ''
                        self.isError = False
                    elif self.current_char != ' ':
                        self.temp_name = temp_word
                        self.current_string += self.definitions[temp_word]


                    # self.current_char = self.get_next_char(self.file_string,self.pos)
                    # self.pos += 1
                else: #Es una variable no definida
                    #string with the variable not defined
                    self.errors.append('Error: variable {} no definida'.format(temp_word))
                    temp_word = ''
                    self.current_string = ''
                    self.isError = True
        if self.current_string != '' and self.temp_name == '':
            if self.actual_tok.definition is None:
                self.actual_tok.token = self.current_string
                self.actual_tok.value = self.current_string
            elif self.actual_tok.token is None and self.actual_tok.definition is not None:
                self.actual_tok.token = self.current_string
                self.actual_tok.value = self.current_string
            self.tokens_file.append(self.actual_tok)
            self.rule_stack[self.token_name].append(self.current_string)

            self.current_string = ''
        elif self.temp_name != '':
            self.actual_tok.token = self.temp_name
            self.actual_tok.value = self.current_string
            self.tokens_file.append(self.actual_tok)
            self.rule_stack[self.token_name].append(self.current_string)
            self.current_string = ''
            self.temp_name = ''
        elif self.current_string == '' and self.actual_tok.token is not None:
            self.tokens_file.append(self.actual_tok)
            self.pos += 1
        else:
            self.pos += 1


    def process_action(self,is_action=True,isValid = True):
        self.coincidir('{')
        temp_action_string = ''

        while self.current_char != '}':
                temp_action_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1

        self.coincidir('}')
        if is_action and isValid:
            #print('token name',self.token_name_i)
            self.actions[self.token_name_i] = {}
            #print('ACTI',self.actions)
            self.actions[self.token_name_i] = temp_action_string
            #print('ACTI2',self.actions)
            return temp_action_string
        elif is_action == False and isValid:
            return temp_action_string
        else:
            return None

    #Metodo para obtener todo ascii printeable
    def get_all_ascii(self):
        self.coincidir('-')
        for char in string.printable:
            if len(str(ord(char))) == 1:
                self.temp_array.append('00' + str(ord(char)))
            elif len(str(ord(char))) == 2:
                self.temp_array.append('0' + str(ord(char)))
            else:
                self.temp_array.append(str(ord(char)))
        temp_string = ''
        temp_string += '('
        #join all the elements in the array with | except the last one
        temp_string += '|'.join(self.temp_array)
        temp_string += ')'
        self.current_string += temp_string
        self.temp_array = []

    #Metodo para procesar un charset
    def process_list(self,initial_exp = True, isDifference = False):
        negative = False
        self.coincidir('[')
        while self.current_char != "]":
            if self.current_char == "'":
                self.evaluate_single(True)
            elif self.current_char == '-':
                self.evaluate_range()
            elif self.current_char == '"':
                self.evaluate_double(True)
            elif self.current_char == '^':
                negative = True #Si es una negacion se debe restar de todo el ascii
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            else:
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1

        self.coincidir(']')

        if negative:
            all_ascii = []
            for char in string.printable:
                if len(str(ord(char))) == 1:
                    char_ascii = '00' + str(ord(char))
                elif len(str(ord(char))) == 2:
                    char_ascii = '0' + str(ord(char))
                else:
                    char_ascii = str(ord(char))
                if char_ascii in self.temp_array:
                    continue
                else:
                    all_ascii.append(char_ascii)
            self.temp_array = all_ascii
        temp_string = ''
        temp_string += '('
        #separate all elements in the array with | except the last one
        temp_string += '|'.join(self.temp_array)
        temp_string += ')'

        if initial_exp:
            self.current_string = temp_string.strip()
        else:
            self.current_string += temp_string.strip()

        if self.current_char != '#' and isDifference: #Si se debe hacer diferencia no se vacia el temp array
            pass
        elif self.current_char == '#':
            self.second_temp_array = self.temp_array
            self.temp_array = []
        else:
            self.temp_array = []

    #Metodo para evaluar una expresion con comillas dobles
    def evaluate_double(self,inside_list = False):
        self.coincidir('"')
        self.temp_array = []
        text = ''
        while self.current_char != '"':
            if self.current_char == '\\' and self.get_next_char(self.file_string,self.pos) in self.valid_scapes:
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
                if self.current_char in self.valid_scapes:
                    if self.current_char == 'n':
                        text = '\n'
                    elif self.current_char == 't':
                        text = '\t'
                    elif self.current_char == 'r':
                        text = '\r'
                    elif self.current_char == 'v':
                        text = '\v'
                    elif self.current_char == 'b':
                        text = '\b'
                    elif self.current_char == 'f':
                        text = '\f'
                    elif self.current_char == 'a':
                        text = '\a'
                    elif self.current_char == '\\':
                        text = '\\'
                    #print('TEXT here',text, ord(text))
                    if len(str(ord(text))) ==1:
                        text = '00'+str(ord(text))
                    elif len(str(ord(text))) == 2:
                        text = '0'+str(ord(text))
                    else:
                        text = str(ord(text))
                self.temp_array.append(text)
                text = ''
                #self.current_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            elif self.current_char == '\\' and self.get_next_char(self.file_string,self.pos) not in self.valid_scapes:
                string_concat = ''
                text = self.current_char
                if len(str(ord(text))) ==1:
                    text = '00'+str(ord(text))
                elif len(str(ord(text))) == 2:
                    text = '0'+str(ord(text))
                else:
                    text = str(ord(text))
                string_concat += '('+text + ')'
                text = ''
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
                text = self.current_char
                if len(str(ord(text))) ==1:
                    text = '00'+str(ord(text))
                elif len(str(ord(text))) == 2:
                    text = '0'+str(ord(text))
                else:
                    text = str(ord(text))
                string_concat += '('+text+')'
                self.temp_array.append(string_concat)
                text = ''
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1

            else:
                text += self.current_char
                #print('TEXT',text)
                if len(str(ord(text))) ==1:
                    text = '00'+str(ord(text))
                elif len(str(ord(text))) == 2:
                    text = '0'+str(ord(text))
                else:
                    text = str(ord(text))
                self.temp_array.append(text)
                text = ''
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
        if inside_list:
            self.current_string += text #vacio porque esta en temp array
            #print("INSIDE LIST DOUBLE",self.current_string)
        else:
            temp_string = ''
            #separate the each element with ()
            for element in self.temp_array:
                temp_string += '(' + element + ')'
            self.current_string += temp_string.strip()
        self.coincidir('"')

    #Metodo que evalua un rango
    def evaluate_range(self):
        #self.current_string += self.current_char
        self.coincidir('-')
        #print('CURRENT STRING -',self.current_string)
        self.evaluate_single(True)
        self.expand_range()

    #Metodo para expandir un rango
    def expand_range(self):
        #get the ascii value of the first char and the last char and then expand the range
        #print('EXPANDING RANGE')
        #pop the last element
        last = self.temp_array.pop()
        #pop the first element
        first = self.temp_array.pop()
        #print('FIRST',chr(int(first)))
        #print('LAST',chr(int(last)))
        for i in range(int(first),int(last) + 1):
            if len(str(i)) ==1:
                i = '00'+str(i)
            elif len(str(i))==2:
                i = '0'+str(i)
            else:
                i = str(i)
            self.temp_array.append(i)
        #print('TEMP ARRAY EXPAND',self.temp_array)

    #Metodo para evaluar una expresion con comillas simples
    def evaluate_single(self,inside_list = False):
        self.coincidir("'")
        #get one char
        text = ''
        while self.current_char != "'":
            if self.current_char == '\\' and self.get_next_char(self.file_string,self.pos) in self.valid_scapes:
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
                if self.current_char == 'n':
                    text = '\n'
                elif self.current_char == 't':
                    text = '\t'
                elif self.current_char == 'r':
                    text = '\r'
                elif self.current_char == 'v':
                    text = '\v'
                elif self.current_char == 'b':
                    text = '\b'
                elif self.current_char == 'f':
                    text = '\f'
                elif self.current_char == 'a':
                    text = '\a'
                elif self.current_char == '\\':
                    text = '\\'
                #print('TEXT here',text)
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
            elif self.current_char == '\\' and self.get_next_char(self.file_string,self.pos) not in self.valid_scapes:
                pass

            else:
                text += self.current_char
                #print('TEXT',text)

                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
        #print('SALI DE EVALUAR SINGLE',text,ord(text))
        if len(text) >1:
                #add error
                self.errors.append('Error: Invalid single')
                self.isError = True
        if self.isError == False:
            if len(str(ord(text))) ==1:
                text = '00'+str(ord(text))
            elif len(str(ord(text))) == 2:
                #print('SOY LEN 2')
                text = '0'+str(ord(text))
            else:
                text = str(ord(text))

            if inside_list:
                self.temp_array.append(text)
            else:
                self.current_string += '('+text+')'
            #self.current_string += text
        self.coincidir("'")

    #Metodo para evaluar comentario
    def comment(self, init=True):
        if init:
            #self.current_string += self.current_char
            self.coincidir('(')
            #self.current_string += self.current_char
            self.coincidir('*')
            while self.current_char != '*' or self.get_next_char(self.file_string,self.pos) != ')':
                #print('CURRENT',self.current_char,self.pos,self.get_next_char(self.actual_line,self.pos))
                self.current_string += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1
                #print('SELF CURRENT',self.current_char,self.get_next_char(self.actual_line,self.pos))

            #print('SALIR')
            #self.current_string += self.current_char
            self.coincidir('*')
            #self.current_string += self.current_char
            self.coincidir(')')
        else:
            self.current_char = self.get_next_char(self.file_string,self.pos)
            self.pos += 1
            self.comment_inside += self.current_char
            self.coincidir('(')
            self.comment_inside += self.current_char
            self.coincidir('*')
            while self.current_char != '*' or self.get_next_char(self.file_string,self.pos) != ')':
                self.comment_inside += self.current_char
                self.current_char = self.get_next_char(self.file_string,self.pos)
                self.pos += 1

            self.comment_inside += self.current_char
            self.coincidir('*')
            self.comment_inside += self.current_char
            self.coincidir(')')

    def coincidir(self,terminal):
        if self.current_char == terminal:
            self.current_char = self.get_next_char(self.file_string,self.pos)
            self.pos += 1
            self.counter_increment += 1
        elif self.current_char == None:
            pass
        else:
            print('Error')

    def get_next_char(self, string, pos = None):
        index = pos
        if index + 1 < len(string):
            return string[index + 1]
        else:
            return None
