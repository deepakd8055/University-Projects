import sys
import ftplib

def decode(dirList):
    data = ""
    #if Method is 7-bit discard files if first 3 bits are set and
    #remove first 3 bits of file permissions. Else take 10bits from each list element
    if METHOD == '7-bit' :                
        for line in dirList:
            if(line[0:3] == "---"):
                data += line[3:10]
    elif METHOD == '10-bit' :
        data = ""
        for line in dirList:
            data += line[0:10]        
    stringMessage = ""
    # replace d,l,r,w,x with 1 and - with 0
    data = data.replace('-','0').replace('d','1').replace('l','1').replace('r','1').replace('w','1').replace('x','1')
    #convert 7 bit binary value to character
    for index in range(0, len(data),7):
        if index+7 < len(data):
            temp = data[index:index+7]
        else:
            temp = data[index:]
        temp = int(temp,2)
        if temp == 8:
            stringMessage = stringMessage[:-1]
        else:
            stringMessage += chr(temp)
    return stringMessage

try:
    cwd = "cd FILES"
    METHOD ="10-bit" #change to 10-bit for 10-bit decoding
    if len(sys.argv) == 3:
        if sys.argv[1]!= '7-bit' and sys.argv[1]!= '10-bit':
            print("Please pass either 7-bit or 10bit as first arguement for decoding")
            exit(0)
        METHOD = sys.argv[1]
        cwd = sys.argv[2]
    ipAddr = '138.47.99.163'
    port = 8008
    username = 'valkyrie'
    password = 'readytoride'
    USE_PASSIVE = True
    ftp = ftplib.FTP()
    ftp.connect(ipAddr, port)
    ftp.login(username, password)
    ftp.set_pasv(USE_PASSIVE)
    ftp.cwd(cwd)
    dirList = []
    ftp.dir(dirList.append) #get file attributes of given directory files and append into list
    print(decode(dirList))
    ftp.quit()
except ftplib.all_errors as e:
    print(e)  #handle wrong directory exception here
 
