from graphviz import Digraph
#uuid
import uuid

class Tree():
    #class to visualize the tree making postorder traversal
    def __init__(self, root):
        self.root = root
        self.dot = Digraph('tree',format='pdf')

        #make postorder traversal
        #add the root node
        self.dot.node(str(self.root.id), self.root.value)

        #add the rest of the nodes
        self.make_postorder(self.root)

    def make_postorder(self, node):
        if node.left != None:
            self.dot.node(str(node.left.id), node.left.value)
            self.dot.edge(str(node.id), str(node.left.id))
            self.make_postorder(node.left)

        if node.right != None:
            self.dot.node(str(node.right.id), node.right.value)
            self.dot.edge(str(node.id), str(node.right.id))
            self.make_postorder(node.right)
