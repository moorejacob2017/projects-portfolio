import math
import random

#NOTES: While this module provides structure for a Neural Network, it does not format how the Neural Network takes in information.
#       The input design msut still be maticulously created in order to achieve proper results.
#       Please see neural_network_driver.py for examples of how this module operates.
#       It is hightly recommended that whoever uses this module has an understanding of how Neural Networks operate and learn.
#
#       Author: Jacob Benjamin Tyler Moore

def sigmoid(input):
    #BASIC SIGMOID FUNCTION
    return (1 / (1 + (math.e**(-input))))

class NeuralLink:
    #MEMBER VARIABLES:
    #dest - Location in NeuralNetwork for recieving neuron, First is layer, Second is Neuron
    #weight - Weight of link

    #MEMBER FUNCTIONS:
    #__init__(self, y, x) - initialization of instance of NeuralLink
        #y - Destination layer
        #x - Destination Neuron in layer y

    def __init__(self, y, x):
        self.dest = [y, x]
        self.weight = random.randint(0,1) - random.random()

class Neuron:
    #MEMBER VARIABLES:
    #value - Activation value to be sent to recieving neuron via link
    #bias - Activation bias added to previous layers forwarding weighted sum before sigmoid
    #link_list - List of NeuralLinks to recieving neurons, Replaces weight matrix

    #MEMBER FUNCTIONS:
    #__init__(self) - Initialization of instance of Neuron

    def __init__(self):
        self.value = 0
        self.bias = random.randint(0,1)- random.random()
        self.link_list = []

class NeuralNetwork:
    #MEMBER VARIABLES:
    #neurons - Double array of neurons neuron[y] specifies the layer, neuron[y][x] specifies the neuron in layer y

    #MEMEBER FUNCTIONS:
    #__init__(self) - Initialization of instance of NeuralNetwork
    #num_layers(self) - Number of layers in NeuralNetwork
    #num_neurons_in(self, layer) - Number of Neurons in specified layer
        #layer - Chosen layer for number of Neurons
    #num_neurons(self) - Total number of Neurons in NeuralNetwork
    #print_network_map(self) - prints map of NeuralNetwork
    #add_layer(self, num_neurons) - Appends an additional layer to NeuralNetwork, automatically points previous layer Neurons to all Neurons in new layer
        #num_neurons - Number of Neurons to add to new layer
        #return self
    #set_input_neuron(self, pos, val) - Sets the desired neuron in the import layer,
        #pos - the position in the input layer ie. pos = 5 -> neurons[0][5]
        #val - value to set input neuron to. !!!WARNING!!! vall must be run through a sigmoid before being passed to function
    #impulse(self) - Activates a the chain reaction amoungst Neuron values, starts at layer 0 and propogates to last layer
    #adjustment(self, correct) - Adjust weights and baises through back propogations
        #correct - an array with size equal to that of number of layers and the size of each respective layer, it is filled with 1 and 0 based on which forwarding neuron was correct, 1 if correct, 0 if wrong. ie correct[y][x]

    def __init__(self):
        self.neurons = []

    def num_layers(self):
        return len(self.neurons)

    def num_neurons_in(self, layer):
        return len(self.neurons[layer])

    def num_neurons(self):
        count = 0
        for x in range(0, self.num_layers()):
            count += self.num_neurons_in(x)
        return count

    def print_network_map(self):
        print("=============================================================")
        print("# LAYERS  : " + str(self.num_layers()))
        print("# NEURONS : " + str(self.num_neurons()))
        j = 0

        #PRINT LAYER
        for y in self.neurons:
            print("=============================================================")
            i = 0
            print("# NEURONS IN LAYER " + str(j) + ": " + str(self.num_neurons_in(j)))
            print("-------------------------")
            #PRINT NEURON IN LAYER
            for x in y:
                #print("[" + str(j) + ", " + str(i) + "]|" + str(x.bias) + "|: "+ str(x.value), end=" v\n")
                print("[" + str(j) + ", " + str(i) + "]|" + str(x.bias) + "|: ", end="\n")
                i +=1
                for z in x.link_list:
                    print("\t\t" + str(z.weight) + "\t-> " +str(z.dest))
            j += 1
        print("=============================================================")

    def add_layer(self, num_neurons):
        #=======================================================================
        self.neurons.append([])

        #CHECK IF FIRST LAYER
        if (self.num_layers() != 1):
            for x in range(0, num_neurons):
                self.neurons[self.num_layers() - 1].append(Neuron())
                for y in range(0, self.num_neurons_in(self.num_layers() - 2)):
                    self.neurons[self.num_layers() - 2][y].link_list.append(NeuralLink(self.num_layers() - 1, x))
        else:
            for x in range(0, num_neurons):
                self.neurons[0].append(Neuron())

        return self
        #=======================================================================

    def set_input_neuron(self, pos, val):
        #=======================================================================
        self.neurons[0][pos].value = val
        #=======================================================================

    def impulse(self):
        #SENDING PROPOGATION
        #=======================================================================
        #LAYER
        for y in range(0, self.num_layers()-1):
            #LINKS/OUTPUT NEURONS
            for z in range(0, self.num_neurons_in(y+1)):
                val = 0.0 #put in z?
                #INPUT NEURON
                for x in range(0, self.num_neurons_in(y)):
                    val += self.neurons[y][x].value * self.neurons[y][x].link_list[z].weight
                self.neurons[y+1][z].value = sigmoid(val + self.neurons[y+1][z].bias)
        #=======================================================================

    def adjustment(self, correct):
        #BACKPROPOGATION

        #GET WEIGHT ADJUSTMENTS
        #=======================================================================
        weight_adjustment_matrix = []
        for y in range(-(self.num_layers()-2), 1):
            weight_adjustment_matrix.append([])

        #ACTIVE ALTERATION LAYER (SENDING)
        for y in range(-(self.num_layers()-2), 1):
            #ACTIVE ALTERATION NEURON (SENDING)
            for x in range(0, self.num_neurons_in(-y)):
                #ACTIVE ALTERATION LINK WEIGHT (SENDING)
                weight_adjustment_matrix[-y].append([])
                for z in range(0, len(self.neurons[-y][x].link_list)):
                    val = 0.0

                    #OVER ALL INPUTS
                    for i in range(0, self.num_neurons_in(-y)):
                        val += self.neurons[-y][i].value * self.neurons[-y][i].link_list[z].weight
                    val += self.neurons[-y+1][z].bias

                    e_val = (math.e**(-val))
                    dest_val = self.neurons[self.neurons[-y][x].link_list[z].dest[0]][self.neurons[-y][x].link_list[z].dest[1]].value

                    weight_adjustment_matrix[-y][x].append( - 2*(dest_val - correct[-y][z]) * dest_val * e_val * self.neurons[-y][x].value)
                    del val
        #=======================================================================

        #GET BIAS ADJUSTMENTS
        #=======================================================================
        bias_adjustment_matrix = []
        for y in range(-(self.num_layers()-2), 1):
            bias_adjustment_matrix.append([])

        #ACTIVE SENDING LAYER (ACTIVE ALTERATION LAYER IS -y+1)
        for y in range(-(self.num_layers()-2), 1):
            #ACTIVE RECEIVEING NEURON BIAS
            for x in range(0, self.num_neurons_in(-y+1)):
                val = 0.0
                for i in range(0, self.num_neurons_in(-y)):
                    val += self.neurons[-y][i].value * self.neurons[-y][i].link_list[x].weight
                val += self.neurons[-y+1][x].bias

                e_val = (math.e**(-val))
                dest_val = self.neurons[-y+1][x].value
                bias_adjustment_matrix[-y].append( -2*(dest_val - correct[-y][x]) * dest_val * e_val)

                del val
        #=======================================================================

        #ALTER WEIGHTS
        #=======================================================================
        for y in range(-(self.num_layers()-2), 1):
            for x in range(0, self.num_neurons_in(-y)):
                for z in range(0, len(self.neurons[-y][x].link_list)):
                    self.neurons[-y][x].link_list[z].weight += weight_adjustment_matrix[-y][x][z]
        #=======================================================================

        #ALTER BIASES
        #=======================================================================
        for y in range(-(self.num_layers()-2), 1):
            for x in range(0, self.num_neurons_in(-y+1)):
                self.neurons[-y+1][x].bias += bias_adjustment_matrix[-y][x]
        #=======================================================================
