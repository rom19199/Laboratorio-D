from postfix import PostfixConverter
from state_definition import State
from binary_tree import Tree
from YALex import Reader
import pickle
from Generate_file import GeneratingScanner
#initialize alphabet
validate =False
State.counter = 0

#read file
yal_file = input('Ingresar el archivo .yal: ')
reader = Reader(yal_file)
flag  = reader.read_file()

if flag == False:
    print('Error al leer archivo')
    exit()
expression = reader.get_tokens_expression()

#a = input("Enter to continue...") #solo para la siguiente
print('----------------------------------------')

print('DFA DIRECTO')
print('EXPRESSION DFA: ',expression)
#direct dfa
expression_postfix = PostfixConverter(expression, tokens_file = reader.tokens_file) #Se aumenta la expresion

postfix,validate= expression_postfix.convertToPostfix(validate)
alfabeto = expression_postfix.build_Alphabet()
print('ALF',alfabeto.getAlphabetNames())

node_root = expression_postfix.make_nodes(postfix)#nodo root


postorder_labeled= node_root.label_leafs() #se enumeran las hojas
for i in reader.tokens_file:
    print(i.token,i.value,i.definition,i.id_leaf)
node_root.make_rules(postorder_labeled) #se hacen las reglas


dfa_direct = node_root.make_dfa_direct(alfabeto.getAlphabetNames())

print('----------------------------------------')

print('SIMULACION DFA DIRECTO')

#make the dfa pickle
with open('dfa', 'wb') as handle:
    pickle.dump(dfa_direct, handle, protocol=pickle.HIGHEST_PROTOCOL)

#create the scanner
header = reader.header
trailer = reader.trailer
scanner = GeneratingScanner(header,trailer)
scanner.build_scanner()
print('----------------------------------------')

