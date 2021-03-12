import sys

def encryption(msg, key):
    tMsg = ""
    for Msg in msg:
        tempMsg = ""
        key = key.replace(" ","")
        spaceCount = 0
        for index in range(0,len(Msg)):
            if ord(Msg[index]) < 91 and ord(Msg[index]) > 64:
                tempMsg += chr((ord(Msg[index])%65 + ord(key[(spaceCount+index)%len(key)])%65)%26+65)
            elif ord(Msg[index]) < 123 and ord(Msg[index]) > 96:
                tempMsg += chr((ord(Msg[index])%97 + ord(key[(spaceCount+index)%len(key)])%65)%26+97)
            else:
                tempMsg += Msg[index]
                spaceCount -= 1
        tMsg += tempMsg
    return tMsg

def decryption(msg, key):
    tMsg = ""
    for Msg in msg:
        tempMsg = ""
        key = key.replace(" ","")
        spaceCount = 0
        for index in range(0,len(Msg)):
            if ord(Msg[index]) < 91 and ord(Msg[index]) > 64:
                tempMsg += chr((26 + ord(Msg[index])%65 - ord(key[(spaceCount+index)%len(key)])%65)%26+65)
            elif ord(Msg[index]) < 123 and ord(Msg[index]) > 96:
                tempMsg += chr((26 + ord(Msg[index])%97 - ord(key[(spaceCount+index)%len(key)])%65)%26+97)
            else:
                tempMsg += Msg[index]
                spaceCount -= 1
        tMsg += tempMsg
    return tMsg

if(len(sys.argv) <3):
    print("Please provide required arguements for encryption/decryption")
    exit(0)
elif(sys.argv[1] != "-e" and sys.argv[1] != "-d"):
    print("Please mention correct mode. -e for Encryption and -d for Decryption")
    exit(0)
msg = sys.stdin.readlines()
if(sys.argv[1] == "-e"):
    sys.stdout.write(encryption(msg, sys.argv[2].upper()))
    
elif(sys.argv[1] == "-d"):
    sys.stdout.write(decryption(msg, sys.argv[2].upper()))
