import os.path
import pickle


def getUsers():
    f = open(r'D:\passfile', 'rb')
    usersList = []
    while True:
        try:
            usersList.append(pickle.load(f))
        except EOFError:
            break
    f.close()
    result = []
    for u in usersList:
        result.append([u[0], u[1], u[3], u[4]])
    return result


def addUser(usr):
    f = open(r'D:\passfile', 'ab')
    pickle.dump(usr, f)
    f.close()


def blockUser(name):
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
            u[3] = True
            break
    x = open(r'D:\passfile', 'wb')
    for u in usersList:
        pickle.dump(u, x)
    x.close()


def addLimit(name):
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
            u[4] = True
            break
    x = open(r'D:\passfile', 'wb')
    for u in usersList:
        pickle.dump(u, x)
    x.close()


def removeLimit(name):
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
            u[4] = False
            break
    x = open(r'D:\passfile', 'wb')
    for u in usersList:
        pickle.dump(u, x)
    x.close()

