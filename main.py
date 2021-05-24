import numpy as np
import time
import keyboard
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import os.path
import pickle

arrX = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
arrY = np.array([])


def learningParams(X, Y, n):
    m = []
    for i in range(n-1):
        print("Enter key phrase as usual")
        while True:
            a = keyboard.read_event()     #Reading the key
            if a.name == "enter":
                a = keyboard.read_event()
                break      #Loop will break on pressing esc, you can remove that
            elif a.event_type == "down":  #If any button is pressed (Not talking about released) then wait for it to be released
                t = time.time()           #Getting time in sec
                b = keyboard.read_event()
                while not b.event_type == "up":  #Loop till the key event doesn't matches the old one
                    b = keyboard.read_event()
                m.append(time.time() - t)
        X = np.append(X, [m], axis=0)
        Y = np.append(Y, 1)
        m.clear()
        print("Enter key phrase and put your hands up high or very closely to keyboard")
        while True:
            c = keyboard.read_event()     #Reading the key
            if c.name == "enter":
                c = keyboard.read_event()
                break      #Loop will break on pressing esc, you can remove that
            elif c.event_type == "down":  #If any button is pressed (Not talking about released) then wait for it to be released
                t = time.time()           #Getting time in sec
                d = keyboard.read_event()
                while not d.event_type == "up" and d.name == c.name:  #Loop till the key event doesn't matches the old one
                    d = keyboard.read_event()
                m.append(time.time() - t)
        X = np.append(X, [m], axis=0)
        Y = np.append(Y, 0)
        m.clear()
        i += 1
    return X, Y


print("1 - Learning")
print("2 - Authentication")
opt = input("Choose one from the options above: ")
if opt == "1":
    n = int(input("Enter number of repetitions: "))
    arrX, arrY = learningParams(arrX, arrY, n)
    arrX = np.delete(arrX, (0), axis=0)
    if os.path.isfile('model.pkl'):
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Model score: {}".format(model.score(arrX, arrY)))
        print("Confusion matrix: ")
        print(confusion_matrix(arrY, model.predict(arrX)))
        print(classification_report(arrY, model.predict(arrX)))
    else:
        model = LogisticRegression(solver='liblinear', random_state=0, warm_start=True)
    model = model.fit(arrX, arrY)
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
if opt == "2":
    if os.path.isfile('model.pkl'):
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Enter your password: ")
        z = np.empty((1, 10))
        while True:
            a = keyboard.read_event()     #Reading the key
            if a.name == "enter":
                a = keyboard.read_event()
                break      #Loop will break on pressing esc, you can remove that
            elif a.event_type == "down":  #If any button is pressed (Not talking about released) then wait for it to be released
                t = time.time()           #Getting time in sec
                b = keyboard.read_event()
                while not b.event_type == "up" and b.name == a.name:  #Loop till the key event doesn't matches the old one
                    b = keyboard.read_event()
                np.append(z, time.time() - t)
        if model.predict(z)[0]:
            print("Successfully authenticated!")
        else:
            print("You are not authenticated. If you are eligible, try one more time")
            exit()
    else:
        print("Any model has ben trained. Choose learning option first")

