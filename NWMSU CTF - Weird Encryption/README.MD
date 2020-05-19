Northwest Missouri State University has a dedicated server for a CTF that is run by the Cyber Defense Club(CDC).
The challenge was that a given application used an unknown encryption to encrypt the file that contained the flag.
From the application they gave us, I was able to reverse-engineer it to determine that the encryption used a seed between
0 and 1000 to switch the bytes of the flag file. Accordingly, I created 2 Python script thats would first, map the movement
of swapped bytes over all seeds and second, to attempt to decrypt the encrypted file over all maps. The encrypted file 
was a .zip file containing a .txt that held the flag and used the 420th seed to encrypt the file.
