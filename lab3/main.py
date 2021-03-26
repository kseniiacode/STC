import func
import pickle
import os
import psutil
import getpass
import wmi
from win32api import GetSystemMetrics, GetComputerName
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import winreg
REG_PATH = r"Software\Zakhariiash"


def get_drive_details(directory):
    size = 0
    device = ""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if str(partition.mountpoint) == directory[:3]:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            size = partition_usage.total
            device += partition.device
    return size, device


def get_keyboard_details():
    keyboard_type = ""
    obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)
    keyboard = [x for x in obj if 'Keyboard' in str(x)]
    for item in keyboard:
        keyboard_type = item.Description
    return keyboard_type


def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


def main():
    # curr_path = os.path.abspath('main.py')[:-7]
    # login = getpass.getuser()
    # hostname = GetComputerName()
    # winpath = os.environ['WINDIR']
    # sysfilespath = os.environ['WINDIR'] + "\\System32\\"
    # width = GetSystemMetrics(0)
    # size, device = get_drive_details(curr_path)
    # keyboard_type = get_keyboard_details()
    # info = "Login {}, Hostname {}, Winpath {}, Sysfilespath {}, Monitorwidth {}, Drivesize {}, Drivedevices {}, Keyboardtype {}".format(login, hostname, winpath, sysfilespath, width, size, device, keyboard_type)
    # hash_info = SHA256.new(data=info.encode())
    # f = open('{}mykey.pem'.format(curr_path), 'rb')
    # pubkey = RSA.import_key(f.read())
    # signature = get_reg('Signature')
    # try:
    #     pkcs1_15.new(pubkey).verify(hash_info, signature)
    # except ValueError:
    #     print("Signature wasn't verified")
    #     exit()
    # print("Success")
    func.createPassFile()
    func.decrypt(r'D:\passfile')
    while True:
        print("1 - SignIn")
        print("2 - SignIn as ADMIN")
        print("3 - Info")
        print("4 - Exit")
        answ = 0
        answ = int(input())
        if answ == 1:
            flag = 1
            login = str(input("Type your login: "))
            f = open(r'D:\passfile', 'rb')
            usersList = []
            while True:
                try:
                    usersList.append(pickle.load(f))
                except EOFError:
                    break
            f.close()
            while True:
                for u in usersList:
                    flag = 0
                    if u[1] == login:
                        if u[3] == 1:
                            print("Your account is blocked")
                            flag = -1
                            break
                        else:
                            flag = 1
                            break
                if flag == 0:
                    print("No such username")
                    print("Enter 0 to exit")
                    login = input("Type your login: ")
                    if login == "0":
                        break
                else:
                    break
            if flag <= 0:
                break
            attempts = 1
            while True:
                if attempts > 3:
                    break
                elif 4 > attempts > 0:
                    password = input("Type your password: ")
                    for u in usersList:
                        if u[1] == login:
                            if password == u[2]:
                                attempts = 0
                            else:
                                print("Incorrect password")
                                print("You have {} more attempts".format(3 - attempts))
                                attempts += 1
                                continue
                elif attempts == 0:
                    break
            if attempts < 4:
                print("1 - Change password")
                print("2 - Exit")
                answ2 = 0
                answ2 = int(input())
                if answ2 == 1:
                    password = input("Type your current password: ")
                    for u in usersList:
                        if u[1] == login:
                            if password == u[2]:
                                while True:
                                    password = input("Type new password: ")
                                    if password == "0":
                                        break
                                    if u[4]:
                                        if func.verifyPassword(password):
                                            password2 = input("Retype your new password: ")
                                            if password2 == password:
                                                func.changePassword(login, password)
                                                print("Password has changed")
                                                break
                                            else:
                                                print("Password wasn't confirmed")
                                                break
                                        else:
                                            print("Enter 0 to exit")
                                            continue
                                    else:
                                        password2 = input("Retype your new password: ")
                                        if password2 == password:
                                            func.changePassword(login, password)
                                            print("Password has changed")
                                            break
                                        else:
                                            print("Password wasn't confirmed")
                                            break
                            else:
                                print("Incorrect password")
                                break
                elif answ2 == 2:
                    break
                else:
                    print("You haven`t chosen any option")
                    break
            else:
                break
            break
        if answ == 2:
            flag = 1
            login = input("Type your login: ")
            f = open(r'D:\passfile', 'rb')
            usersList = []
            while True:
                try:
                    usersList.append(pickle.load(f))
                except EOFError:
                    break
            f.close()
            while True:
                if login != "ADMIN":
                    print("Only for admin")
                    print("Enter 0 to exit")
                    login = input("Type your login: ")
                    if login == "0":
                        flag = 0
                        break
                else:
                    break
            if flag == 0:
                break
            attempts = 1
            while True:
                if 4 > attempts:
                    password = input("Type your password: ")
                    if password == usersList[0][2]:
                        break
                    else:
                        print("Incorrect password")
                        print("You have {} more attempts".format(3 - attempts))
                        attempts += 1
                        continue
                else:
                    flag = 0
                    break
            if flag == 0:
                break
            while True:
                print("1 - Change password")
                print("2 - List of users")
                print("3 - New user")
                print("4 - Block user")
                print("5 - Limit/unlimit user`s password")
                print("6 - Exit")
                answ3 = int(input())
                if answ3 == 1:
                    password = input("Type your current password: ")
                    if usersList[0][2] == password:
                        password = input("Type your new password: ")
                        if usersList[0][4]:
                            if func.verifyPassword(password):
                                password2 = input("Retype your new password: ")
                                if password == password2:
                                    func.changePassword('ADMIN', password)
                                    print("Password has changed")
                                    break
                                else:
                                    print("Password wasn't confirmed")
                                    break
                            else:
                                break
                        else:
                            password2 = input("Retype your new password: ")
                            if password == password2:
                                func.changePassword('ADMIN', password)
                                print("Password has changed")
                                break
                            else:
                                print("Password wasn't confirmed")
                                break
                if answ3 == 1:
                    password = input("Type your current password: ")
                elif answ3 == 2:
                    usersList = func.adminfunc.getUsers()
                    print(usersList)
                    continue
                elif answ3 == 3:
                    id = input("Enter id: ")
                    username = input("Enter username: ")
                    isblocked = input("Enter 1 if blocked, 0 if not: ")
                    islimited = input("Enter 1 if password is limited, 0 if not: ")
                    usr = [id, username, '', isblocked, islimited]
                    func.adminfunc.addUser(usr)
                    continue
                elif answ3 == 4:
                    username = input("Enter username: ")
                    func.adminfunc.blockUser(username)
                    continue
                elif answ3 == 5:
                    option = input("If you want to set the limit, enter 1, enter 0 if not: ")
                    username = input("Enter username: ")
                    if option == 1:
                        func.adminfunc.addLimit(username)
                    else:
                        func.adminfunc.removeLimit(username)
                    continue
                elif answ3 == 6:
                    break
                else:
                    print("Chose one option")
            break
        elif answ == 3:
            print("Zakhariash Kseniia")
            print("Upper and lowercase letters and numbers")
            continue
        elif answ == 4:
            break
        else:
            print("Chose one option")
        break
    func.encrypt(r'D:\passfile')


if __name__ == '__main__':
    main()

