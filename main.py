import os
import shutil
import getpass
import psutil
from win32api import GetSystemMetrics, GetComputerName
import wmi
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


def set_reg(name, value):
	try:
		winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
		winreg.SetValueEx(registry_key, name, 0, winreg.REG_NONE, value)
		winreg.CloseKey(registry_key)
		return True
	except WindowsError:
		return False


if __name__ == '__main__':
	while True:
		directory = input("Choose directory to write program code: ")
		if os.path.isdir(directory):
			shutil.copy(r"C:\Users\Professional\PycharmProjects\lab1\adminfunc.py", directory)
			shutil.copy(r"C:\Users\Professional\PycharmProjects\lab1\func.py", directory)
			shutil.copy(r"C:\Users\Professional\PycharmProjects\lab1\main.py", directory)
			break
		else:
			print("No such directory")
	login = getpass.getuser()
	hostname = GetComputerName()
	winpath = os.environ['WINDIR']
	sysfilespath = os.environ['WINDIR'] + "\\System32\\"
	width = GetSystemMetrics(0)
	size, device = get_drive_details(directory)
	keyboard_type = get_keyboard_details()
	info = "Login {}, Hostname {}, Winpath {}, Sysfilespath {}, Monitorwidth {}, Drivesize {}, Drivedevices {}, Keyboardtype {}".format(login, hostname, winpath, sysfilespath, width, size, device, keyboard_type)
	key = RSA.generate(1024, os.urandom)
	hash_info = SHA256.new(data=info.encode())
	signature = pkcs1_15.new(key).sign(hash_info)
	pubkey = key.publickey()
	f = open('{}mykey.pem'.format(directory), 'wb')
	f.write(pubkey.export_key('PEM'))
	f.close()
	print(set_reg('Signature', signature))

