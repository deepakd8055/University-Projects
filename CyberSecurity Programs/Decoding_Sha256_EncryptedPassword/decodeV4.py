import sqlite3
import hashlib
conn = sqlite3.connect('users.db')


c = conn.cursor()


x=c. execute("SELECT name FROM sqlite_master WHERE type='table';")

lis = []
for y in x.fetchall():
    c1 = conn.cursor()
    cmd = "SELECT * FROM " + str(y[0])
    c1.execute(cmd)
    lis.append(c1.fetchall())
lis1 = []
for i in range(len(lis[0])):
    lis1.append(lis[0][i][0])
lis5 = []
for k in range(len(lis1)):
    a = lis1[k]
    b = []
    c=""
    d=a
    for j in range(len(d)):
        if ord(d[j]) > 96 and ord(d[j]) < 123:
            c+= chr(((ord(d[j])+24-96)%26)+97)
        elif ord(d[j]) > 64 and ord(d[j]) < 91:
            c+= chr(((ord(d[j])+24-64)%26)+65)

        else:
            c+= d[j]
    lis5.append(c)


lis2 = []
lis3 = []
for i in range(len(lis[0])):
    lis2.append(lis[0][i][1])
    lis3.append(lis[0][i][2])

pep = "I really love this stuff!"
result = hashlib.sha256(pep.encode())
p = result.hexdigest()
lis4 = []
for j in range(len(lis2)):
    pwd = lis2[j]
    salt = lis3[j]
    f = open("dictionary.txt", "r")
    for x in f:
        #print(x)

        bi=""
        for i in range(0,len(salt),2):
            bi += format(int(str(salt[i:i+2]),16),'08b')
        bi2=""
        for i in range(0,len(x[:-1])):
            bi2 += format(ord(x[i]),'08b')

        bi3=""
        for i in range(0,len(p)):
            bi3 += format(ord(p[i]),'08b')

    
        d2 = bi+bi2+bi3

        d3 = int(d2,2).to_bytes((len(d2)+7)//8,byteorder='big')
        pas1 = hashlib.sha256(d3).hexdigest()


        if pwd == pas1:
            lis4.append(lis5[j]+" > "+x)
print("USERNAME > PASSWORD")
for j in lis4:
    print(j)

