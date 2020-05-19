import os
from os import path

FILE = open("encrypted_binary.txt", "r")
inputLen = int(input("ENTER NUM OF BYTES: "))

encbin = []
for x in range(0,inputLen):
    encbin.append(FILE.readline())
FILE.close()

decout = "output.txt"
if (path.isfile(decout)):
    os.remove(decout)
FILE = open(decout, "x")
FILE.close()

for seed in range(1001):

    decbin = []
    for x in range(0,inputLen):
        decbin.append("")

    FILE = open("Map_Key_s" + str(seed) + ".txt", "r")
    for x in range(0,inputLen):
        k = int(FILE.readline())
        print(str(seed) + ": " + str(encbin[x]) + str(x) + "->" + str(decbin[k]) + str(k))
        decbin[x] = encbin[k]
    FILE.close()

    dec = "decrypted_hex_s" + str(seed) + ".txt"
    if not(path.isfile(dec)):
        FILE = open(dec, "x")
        FILE.close()

#    tempstr = ""
    FILE = open(dec, "w")
    for x in range(0,inputLen):
        #tempstr += (str(decbin[x])[2:])[:-1])
        FILE.write(str(decbin[x]))
    FILE.close()

    hexstr = ""
    FILE = open(dec, "r")
    for x in range(0, inputLen):
        hexstr += (FILE.readline())[:-1]

    os.remove(dec)
    '''
    decbytestr = "decrypted_bytestr_s" + str(seed)
    if not(path.isfile(decbytestr)):
        FILE = open(decbytestr, "x")
        FILE.close()

    FILE = open(decbytestr, "w")
    FILE.write(hexstr)
    FILE.close()
    '''

    bytestr = bytes.fromhex(hexstr)

    FILE = open(decout, "a")

    try:
        bytestr.decode('utf-8')
    except:
        print("ERR: UNABLE TO CONVERT")
    else:
        FILE.write(bytestr.decode('utf-8'))
    FILE.close()

    rawout = "raw_s" + str(seed)
    if not(path.isfile(rawout)):
        FILE = open(rawout, "x")
        FILE.close()

    FILE = open(rawout, "wb")
    FILE.write(bytestr)
    FILE.close()
