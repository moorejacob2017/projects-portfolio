from neural_network import *
import random
import curses

#REQUIRED MODULES: random,curses,neural_network.py
#
#NOTES: This driver is used as a simple showcase of the classes and functions contained in my accompanied neural_network.py file.
#       This diver randomly generates a number between 00 and 99 inclusivly that is then passed to a Neural Network with an input
#       layer of 20 neuron nodes, 10 nodes for the ten's place values of 0-9 and 10 nodes for the one's place values of 0-9.
#       The Neural Network must then reproduce the aformentioned value based on the given value's ten's place and one's place by sending
#       the proper signals to the output layer, which contains 100 output neuron nodes, 1 node for each possible outcome for the
#       values of 00-99. Once the Neural Network has produced a response the driver then determines if the response is correct.
#       The Neural Network then modifies it's weights and biases accordingly, via backpropogation, to increase it's answering accuracy.
#
#RUNNING IN CMD PROMPT:
#       python neural_network_driver.py
#
#USER DIRECTIONS:
#       Press Up Arrow Key(^) to pause
#       Press Left Arrow Key(<) to slow down or continue
#       Press Right Arrow Key(>) to speed up or continue
#       Press Down Arrow Key(v) to exit
#
#       Author: Jacob Benjamin Tyler Moore

s = curses.initscr()
curses.curs_set(0)
sht, swt = s.getmaxyx()
sh = int (sht)
sw = int (swt)

screen = curses.newwin(sh, sw)
screen.keypad(1)
screen.timeout(1)

j = 100
p = 0
right = 0
wrong = 0

screen.addstr(0,0, "Press Up Arrow Key(^) to pause")
screen.addstr(1,0, "Press Left Arrow Key(<) to slow down or continue")
screen.addstr(2,0, "Press Right Arrow Key(>) to speed up or continue")
screen.addstr(3,0, "Press Downs Arrow Key(v) to exit")


test_net = NeuralNetwork().add_layer(20).add_layer(j)

key = curses.KEY_RIGHT

while key != curses.KEY_DOWN:

    if key == curses.KEY_LEFT:
        curses.napms(1000)

    while key == curses.KEY_UP:
        curses.napms(100)
        next_key = screen.getch()
        key = key if next_key == -1 else next_key

    screen.addstr(5,0,"GENERATION :\t" + str(p))
    p+=1
    next_key = screen.getch()
    key = key if next_key == -1 else next_key

    answer = random.randint(0,j-1)
    screen.addstr(7,0, "ANSWER :\t" + str(answer))

    for x in range(0, 10):
        if int(answer / 10) == x:
            test_net.set_input_neuron(x, 1)
        else:
            test_net.set_input_neuron(x, 0)

    for x in range(10, 20):
        if answer % 10 == x-10:
            test_net.set_input_neuron(x, 1)
        else:
            test_net.set_input_neuron(x, 0)

    test_net.impulse()

    outs = []
    for x in range(0, j):
        outs.append(test_net.neurons[1][x].value)

    guess = outs.index(max(outs))
    for x in range(0, j):
        if guess == x:
            screen.addstr(6,0, "GUESS  :\t" + str(x))

            if x == answer:
                right += 1
                screen.addstr(9, 0, "# OF RIGHT   :\t" + str(right))
            else:
                wrong += 1
                screen.addstr(10, 0, "# OF WRONG   :\t" + str(wrong))

            screen.addstr(11, 0, "RUN ACCURACY :\t%" + str((right/(wrong+right))*100)[:5])

    correct = [[]]
    for x in range(0, j):
        if x == answer:
            correct[0].append(1)
        else:
            correct[0].append(0)

    test_net.adjustment(correct)

curses.endwin()
#test_net.print_network_map()
