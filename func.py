import os.path
import pickle
import string
from Crypto.Cipher import ARC4
from Crypto.Hash import MD2
import adminfunc


def createPassFile():
    if not os.path.isfile(r'D:\passfile'):
        f = open(r'D:\passfile', 'wb')
        #('id, usrname, passwd, isblocked, islimited')
        users = [0, 'ADMIN', '', False, False]
        pickle.dump(users, f)
        f.close()


def changePassword(name, newpass):
    f = open(r'D:\passfile', 'rb')
    usersList = []
    while True:
        try:
            usersList.append(pickle.load(f))
        except EOFError:
            break
    f.close()
    for u in usersList:
        if u[1] == name:
            u[2] = newpass
            break
    x = open(r'D:\passfile', 'wb')
    for u in usersList:
        pickle.dump(u, x)
    x.close()


def verifyPassword(password):
    if len(set(string.ascii_lowercase).intersection(password)) == 0:
        print("Your password must contain lowercase letter")
        return 0
    elif len(set(string.ascii_uppercase).intersection(password)) == 0:
        print("Your password must contain uppercase letter")
        return 0
    elif len(set(string.digits).intersection(password)) == 0:
        print("Your password must contain number")
        return 0
    else:
        return 1


def encrypt(filename):
    key = input("Enter secret phrase: ")
    f = open(filename, 'rb')
    tempkey = MD2.new(data=key.encode()).digest()
    cipher = ARC4.new(tempkey)
    enc = cipher.encrypt(f.read())
    f.close()
    f = open(filename, 'wb')
    f.write(enc)


def decrypt(filename):
    key = input("Enter secret phrase: ")
    f = open(filename, 'rb')
    tempkey = MD2.new(data=key.encode()).digest()
    cipher = ARC4.new(tempkey)
    plaintext = cipher.decrypt(f.read())
    f.close()
    f = open(filename, 'wb')
    f.write(plaintext)

