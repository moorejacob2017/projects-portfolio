import os
from os import path

plainArray = []
inputLen = int(input("ENTER NUM OF BYTES: "))

for x in range(0,inputLen):
    plainArray.append('a')

for x in range(1001):
    if path.isfile("Map_Key_s" + str(x) + ".txt"):
        FILE = open("Map_Key_s" + str(x) + ".txt", "w")
        FILE.write("")
        FILE.close()

for seed in range(1001):
    for x in range(0,inputLen):

        plainArray[x] = 'A'

        FILE = open("ptArray", "w")
        for y in range(0,inputLen):
            FILE.write(plainArray[y])
        FILE.close

        FILE = open("ptArray", "r")
        FILE2 = open("etArray", "w")

        print("S" + str(seed) + "- I" + str(x+1))
        cmd = "./weird-encrypt-x64 " + str(seed) + " ptArray etArray"
        os.system(cmd)
        os.system("echo \n")

        FILE2.close()
        FILE.close()

        FILE = open("etArray", "r")
        encryptedArray = FILE.read()
        FILE.close()

        mks = "Map_Key_s" + str(seed) + ".txt"

        if not(path.isfile(mks)):
            FILE = open("Map_Key_s" + str(seed) + ".txt", "x")
            FILE.close()

        FILE = open("Map_Key_s" + str(seed) + ".txt", "a")
        for y in range(0,inputLen):
            if encryptedArray[y] == 'A':
                FILE.write(str(y) + "\n")
                break
        FILE.close()

        plainArray[x] = 'a'
