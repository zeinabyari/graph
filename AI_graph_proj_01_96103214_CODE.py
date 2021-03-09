import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib.widgets import Button
from matplotlib.widgets import AxesWidget
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import TextBox
#from matplotlib.widgets import Slider

   
################ Drawing the Graph, options as radio buttons and etc. ################

#Define the graph along with its nodes and their positions ;
X = nx.Graph()
for i in range (1,6) :
    for j in range (0, i + 6):
        k = i * 7 + j - 6
        if (k < 36):
            X.add_node(k, pos = (j, i - 1))

pos=nx.get_node_attributes(X,'pos')

#Making a list of 58 random numbers from 1 to 100 as the weights of the graph's edges ;
my_randoms = random.sample(range(1,101), 100)
del my_randoms[58:100]

#Setting edges of the graph and assigning weights to each one ;
i = 0
for j in range (1, 35) :
    if j % 7 != 0 :
        X.add_edge(j, j + 1, weight = my_randoms[i])
        i = i + 1
    if j < 29:
        X.add_edge(j, j + 7, weight = my_randoms[i])
        i = i + 1

labels = nx.get_edge_attributes(X,'weight')

#Determine the location of the graph in the plot ;
x_place = plt.axes([0.12,  0.01, 0.87, 0.88])

#Drawing the graph
nx.draw_networkx_nodes(X,pos,node_size=600, node_color='g', alpha=0.4, node_shape='s')
nx.draw_networkx_labels(X, pos, font_size = 8, font_weight = 'heavy')

nx.draw_networkx_edges(X, pos, width = 1.5, edg_color = 'r', style = 'dotted', alpha = 0.3)
nx.draw_networkx_edge_labels(X, pos, edge_labels = labels, font_size = 7)

#A class to make radio buttons display horizontally
class MyRadioButtons(RadioButtons):

    def __init__(self, ax, labels, active=0, activecolor='blue', size=49,
                 orientation="vertical", **kwargs):
        
        AxesWidget.__init__(self, ax)
        self.activecolor = activecolor
        axcolor = ax.get_facecolor()
        self.value_selected = None

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_navigate(False)

        circles = []
        for i, label in enumerate(labels):
            if i == active:
                self.value_selected = label
                facecolor = activecolor
            else:
                facecolor = axcolor
            p = ax.scatter([],[], s=size, marker="o", edgecolor='black',
                           facecolor=facecolor)
            circles.append(p)
        if orientation == "horizontal":
            kwargs.update(ncol=len(labels), mode="expand")
        kwargs.setdefault("frameon", False)    
        self.box = ax.legend(circles, labels, loc="center", **kwargs)
        self.labels = self.box.texts
        self.circles = self.box.legendHandles
        for c in self.circles:
            c.set_picker(5)
        self.cnt = 0
        self.observers = {}

        self.connect_event('pick_event', self._clicked)

    def _clicked(self, event):
        if (self.ignore(event) or event.mouseevent.button != 1 or
            event.mouseevent.inaxes != self.ax):
            return
        if event.artist in self.circles:
            self.set_active(self.circles.index(event.artist))

#Initializing "start node" and "goal node" as their default values + receiving values entered by the user ;
start_node = 1
def submit_start(submit):
    global start_node
    start_node = submit

goal_node = 35
def submit_goal(submit):
    global goal_node
    goal_node = submit

preferred_depth = 2
def submit_depth(submit):
    global preferred_depth
    preferred_depth = submit

#Setting the default method of search + setting it according to what user has chosen ;
search_method = 1

def methodFunc(lable):
    global search_method
    if lable == 'Breadth-First Search' :
        search_method = 1
    if lable == 'Depth-First Search' :
        search_method = 2
    elif lable == 'Uniform Cost Search' :
        search_method = 3
    elif lable == 'Iterative Deepening Depth-First Search' :
        search_method = 4

#Setting search method options as radio buttons by determining their place on the plot and setting their texts ;    
plt.subplots_adjust(left=0.2)
radios_place = plt.axes([0.12,0.9,0.87,0.05])
#plt.text(- 0.068, - 0.05, "Choose a method :\n")
radio_buttons =  MyRadioButtons(radios_place ,['Breadth-First Search','Depth-First Search','Uniform Cost Search', 'Iterative Deepening Depth-First Search'], active=0, activecolor='black',
                        orientation="horizontal")
radio_buttons.on_clicked(methodFunc)

#Defining a text-box for inputting start node by the user (sends input data to "submit_start" function (line 96))
startbox_place = plt.axes([0.07, 0.8, 0.03, 0.05])
text_box1 = TextBox(startbox_place,'', initial = '1')
plt.text(-1.7, 1.0, "Start :\n")
text_box1.on_submit(submit_start)

#Defining a text-box for inputting goal node by the user (sends input data to "submit_goal" function (line 101))
goalbox_place = plt.axes([0.07, 0.7, 0.03, 0.05])
text_box2 = TextBox(goalbox_place,'', initial = '35')
plt.text(-1.7, 1.0, "Goal :\n")
text_box2.on_submit(submit_goal)

#Defining a text-box for inputting depth limit by the user (sends input data to "preferred_depth" function (line 106))
preferredDepthBox_place = plt.axes([0.07, 0.6, 0.03, 0.05])
text_box3 = TextBox(preferredDepthBox_place,'')#, initial = '2')
plt.text(-1.7, 1.0, "Depth limit :\n")
text_box3.on_submit(submit_depth)

#Defining a button for searching proccess to start whenever user clicked it ;
searchButton_place = plt.axes([0.04, 0.5, 0.06, 0.05])
searchButton = Button(searchButton_place, 'Search', color = 'pink', hovercolor = 'grey')

#######################################################################

################ Define required functions and classes ################

#Tree Class ;

class Tree(object) :
    def __init__(self, lable, parent) :
        self.lable = lable
        self.children = []
        self.parent = parent
        self.depth = 0

        if self.parent == None :
            self.depth = 0
        else :
            self.depth = parent.depth + 1

    def addChildren(self) :
        neighbors_list = list(X.neighbors(self.lable))
        if self.parent == None :
            self.children = []
            for f in range(len(neighbors_list)) :
                aChild = Tree(neighbors_list[f], self)
                self.children.append(aChild)

        else :
            self.children = []
            for f in range(len(neighbors_list)) :
                if neighbors_list[f] != self.parent.lable :
                    aChild = Tree(neighbors_list[f], self)
                    self.children.append(aChild)
    def getCost(self) :
        sample_node = self
        sample_node_cost = 0
        while sample_node.parent != None :
            weightDic = X.get_edge_data(sample_node.lable, sample_node.parent.lable)
            sample_node_cost = sample_node_cost + int(weightDic['weight'])
            sample_node = sample_node.parent
        return sample_node_cost


#Depth Class ;

class Depth(object) :
    def __init__(self, level) :
        self.level = level
        self.members = []

    def addMember(self, node) :
        self.members.append(node)

#Breadth-First search function ;
def breadthFirst_search(startNode, goalNode) :
    
    found = 'no'
    
    current_searchin_node = Tree(int(startNode), None)
    
    current_searchin_depth = Depth(0)
    current_searchin_depth.addMember(current_searchin_node)
    next_searchin_depth = Depth(1)

    while found == 'no' :
        current_searchin_node.addChildren()
        for m in range(len(current_searchin_node.children)):
            next_searchin_depth.addMember(current_searchin_node.children[m])
            if int(goalNode) == current_searchin_node.children[m].lable :
                    found = 'yes'
                    break
        if found == 'yes' :
            break
        else :
            if current_searchin_node == current_searchin_depth.members[len(current_searchin_depth.members) - 1] :
                current_searchin_node = next_searchin_depth.members[0]
                del(current_searchin_depth)
                current_searchin_depth = next_searchin_depth
                next_searchin_depth = Depth(current_searchin_node.depth + 1)

            else :
                for h in range(len(next_searchin_depth.members)):
                    if current_searchin_node == current_searchin_depth.members[h] :
                        current_searchin_node = current_searchin_depth.members[h + 1]
                        break

    ansList = []        
    if found == 'yes' :
        ansList.append(int(goalNode))
        while current_searchin_node != None:
            ansList.append(current_searchin_node.lable)
            current_searchin_node = current_searchin_node.parent
    return ansList


#Depth-First search function ;  
def depthFirst_search(startNode, goalNode) :
    
    found = 'no'

    current_searchin_node = Tree(int(startNode), None)
    current_searchin_node.addChildren()

    while found == 'no' :
        while len(current_searchin_node.children) != 0:
            for m in range(len(current_searchin_node.children)):
                if int(goalNode) == current_searchin_node.children[m].lable :
                    found = 'yes'
                    break
            if found == 'yes' :
                break
            else :
                current_searchin_node = current_searchin_node.children[0]
                current_searchin_node.addChildren()

        if found == 'yes' :
                break
        if len(current_searchin_node.children) == 0 :
            goodOne = 0
            while goodOne == 0 :
                for h in range(len(current_searchin_node.parent.children)):
                    if current_searchin_node == current_searchin_node.parent.children[h] :
                        if h + 1 < len(current_searchin_node.parent.children) :
                            current_searchin_node = current_searchin_node.parent.children[h + 1]
                            current_searchin_node.addChildren()
                            goodOne = 1
                            break
                    if h == len(current_searchin_node.parent.children) - 1 :
                        current_searchin_node = current_searchin_node.parent

    ansList = []
    if found == 'yes' :
        ansList.append(int(goalNode))
        while current_searchin_node != None:
            ansList.append(current_searchin_node.lable)
            current_searchin_node = current_searchin_node.parent
    return ansList


#Uniform cost search function ;  
def uniformCost_search(startNode, goalNode) :

    found = 'no'
    
    current_searchin_node = Tree(int(startNode), None)
    
    notSearchedNodes_List = []
    sample_node = current_searchin_node

    while found == 'no' :
        current_searchin_node.addChildren()
        for m in range(len(current_searchin_node.children)):
            if int(goalNode) == current_searchin_node.children[m].lable :
                found = 'yes'
                break
            notSearchedNodes_List.append(current_searchin_node.children[m])
            current_searchin_node.children[m].parent = sample_node
            sample_node.children.append(current_searchin_node.children[m])
        if found == 'yes' :
            break

        indx = 0
        leastCost = notSearchedNodes_List[0].getCost()
        for f in range(len(notSearchedNodes_List)) :
            sample_cost = notSearchedNodes_List[f].getCost()
            if sample_cost < leastCost :
                leastCost = sample_cost
                indx = f
        current_searchin_node = notSearchedNodes_List[indx]
        sample_node = current_searchin_node
        for l in range(len(current_searchin_node.parent.children)) :
            if current_searchin_node.parent.children[l] == current_searchin_node :
                current_searchin_node.parent.children[l] = sample_node
                break

        del notSearchedNodes_List[indx]

    ansList = []
    if found == 'yes' :
        ansList.append(int(goalNode))
        while current_searchin_node != None:
            ansList.append(current_searchin_node.lable)
            current_searchin_node = current_searchin_node.parent
    return ansList


#Iterative deepening depth-first search function ;  
def IterativeDeepeningDF_search(startNode, goalNode, preferredDepth) :
    
    found = 'no'

    current_searchin_node = Tree(int(startNode), None)
    current_searchin_node.addChildren()

    while found == 'no' :
        while len(current_searchin_node.children) != 0:
            if current_searchin_node.depth == int(preferredDepth) :
                current_searchin_node.children = []
                break
            for m in range(len(current_searchin_node.children)):
                if int(goalNode) == current_searchin_node.children[m].lable :
                    found = 'yes'
                    break
            if found == 'yes' :
                break
            else :
                current_searchin_node = current_searchin_node.children[0]
                current_searchin_node.addChildren()

        if found == 'yes' :
                break
        if len(current_searchin_node.children) == 0 :
            goodOne = 0
            while goodOne == 0 :
                if current_searchin_node.parent != None :
                    for h in range(len(current_searchin_node.parent.children)):
                        if current_searchin_node == current_searchin_node.parent.children[h] :
                            if h + 1 < len(current_searchin_node.parent.children) :
                                current_searchin_node = current_searchin_node.parent.children[h + 1]
                                current_searchin_node.addChildren()
                                goodOne = 1
                                break
                        if h == len(current_searchin_node.parent.children) - 1 :
                            current_searchin_node = current_searchin_node.parent

    ansList = []
    if found == 'yes' :
        ansList.append(int(goalNode))
        while current_searchin_node != None:
            ansList.append(current_searchin_node.lable)
            current_searchin_node = current_searchin_node.parent
    return ansList


def on_button_clicked(event):
    #clears the axes where the graph is placed
    plt.axes([0.12,  0.01, 0.87, 0.88])
    plt.cla()

    #draws the graph again    
    nx.draw_networkx_nodes(X,pos,node_size=600, node_color='g', alpha=0.4, node_shape='s')
    nx.draw_networkx_labels(X, pos, font_size = 8, font_weight = 'heavy')

    nx.draw_networkx_edges(X, pos, width = 1.5, edg_color = 'r', style = 'dotted', alpha = 0.3)
    nx.draw_networkx_edge_labels(X, pos, edge_labels = labels, font_size = 7)
    
    ans_list = []

    if start_node == goal_node:
        ans_list.append(int(start_node))

    elif search_method == 1 :
        ans_list = breadthFirst_search(start_node, goal_node)

    elif search_method == 2 :
        ans_list = depthFirst_search(start_node, goal_node)

    elif search_method == 3 :
        ans_list = uniformCost_search(start_node, goal_node)
     
    elif search_method == 4 :
        global preferred_depth
        ans_list = IterativeDeepeningDF_search(start_node, goal_node, preferred_depth)

    #colors the navigated nodes
    plt.axes([0.12,  0.01, 0.87, 0.88])
    nx.draw_networkx_nodes(X, pos, node_size=600, nodelist = ans_list, node_color = '#84D7F5', node_shape='s')

def main() :
    searchButton.on_clicked(on_button_clicked)

if __name__ == "__main__":
    main()

plt.show()