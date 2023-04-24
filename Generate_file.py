#write a python file to simulate and read the pickle file of dfa
class GeneratingScanner():
    def __init__(self,header = None,trailer=None):
        self.header = header
        self.trailer = trailer
        self.name_file = 'generated_scanner.py'

    def build_scanner(self):
        with open(self.name_file,'w') as f:
            if self.header is not None:
                f.write(self.header.strip())
            f.write('''
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
''')
            if self.trailer is not None:
                f.write(
self.trailer.strip()
                )