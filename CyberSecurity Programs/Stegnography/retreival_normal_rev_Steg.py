import sys
import os
import shutil 

def stegging(fileName):
    file = open(fileName,'wb')
    file.close()
    file = open(fileName,'ab')
    for x in offsetList:
        for y in intervalList:
            offset = x
            interval = y        
            if storeType == "s":
                if mode =="B":
                    for i in range(0,len(hData)):
                        # Replacing values at index offset with hidden file index data
                        wData[offset] = hData[i]
                        offset += interval
                    for i in range(0,len(senti)):
                        # Replacing values at index offset with senti index data
                        wData[offset] = senti[i]
                        offset += interval
                    file.write(wData)
                elif mode =="b":
                    for i in range(0,len(hData)):
                        for j in range(0,8):
                            # Replacing the least significant bit of wrapper file with offset with hidden file index bit
                            wData[offset] &= 254
                            wData[offset] |= ((hData[i] & 128) >> 7)
                            hData[i] = (hData[i] << 1)& (2**8 - 1)
                            offset += interval
                    for i in range(0,len(senti)):
                        for j in range(0,8):
                            # Replacing the least significant bit of wrapper file with offset with senti index bit
                            wData[offset] &= 254
                            wData[offset] |= ((senti[i] & 128) >> 7)
                            senti[i] = (senti[i] << 1)& (2**8 - 1)
                            offset += interval
                    file.write(wData)
                    
            elif storeType == "r":
                if mode =="B":
                    count = 0
                    while(count!=6 and offset<len(wData)):
                        if wData[offset] != senti[count]:
                            #checking with senti data, if equals increments the count value and breaks the loop if it matches all senti values
                            for i in range(0,count):
                                file.write(bytes([senti[i]]))
                            file.write(bytes([wData[offset]]))
                            offset += interval
                            count = 0
                        else:
                            count+= 1
                            offset += interval
                            
                elif mode =="b":
                    count = 0
                    while(count!=6 and ((offset+8*interval)<len(wData))):
                        data = 0
                        for j in range(0,8):
                            #taking the last bit from wrapper file after offset and constructing the byte
                            data |= (wData[offset] & 1)
                            if j < 7:
                                data = (data << 1)
                                offset += interval
                        if data != senti[count]:
                            for i in range(0,count):
                                #checking with senti data, if equals increments the count value and breaks the loop if it matches all senti values
                                file.write(bytes([senti[i]]))
                            file.write(bytes([data]))
                            offset += interval
                            count = 0
                        else:
                            count+= 1
                            offset += interval
                        #print(offset)
                        
            else:
                print("Please provide type (-s or -r)")
    file.close()
    
# Command line arguements
if len(sys.argv) >1:    
    storeType = "r"
    mode = sys.argv[1][1:]
    wFile = "tararipaparipaapaj.mp3"
    wData = bytearray(open(wFile,"rb").read())

    hFile = ""
    hData = ""
    
#stegging from left to right    
if mode == "B":
    offsetList = [2**12]
    intervalList = [8]
else:
    offsetList = [2**12]
    intervalList = [1]

senti = bytearray(b'\0\xff\0\0\xff\0')

stegging("leftToRightSteg.gif")

#stegging from right to left            
if mode == "B":
    offsetList = [2**10]
    intervalList = [-8]
else:
    offsetList = [2**10]
    intervalList = [-1]        


stegging("rightToLeftSteg.txt")
