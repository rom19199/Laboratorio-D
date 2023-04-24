from token_definitions import *
import pickle
#read the dfa
with open('dfa', 'rb') as handle:
    dfa = pickle.load(handle)
#read the file to simulate from console
input_file = input('Ingresar archivo de entrada: ')
with open(input_file, 'r') as f:
    # Read the contents of the file
    text = f.read()
#simulate the dfa
dfa.simulate_dfa(text)
tokens  = dfa.get_identified()
yal_tokens = dfa.get_list_tokens()
for i in tokens:
    if type(i) == str:
        print(i)
    else:
        if i.definition != None:
            exec(i.definition.strip())
        else:
            print('NO DEFINITION',i.token)
print("fin del archivo")