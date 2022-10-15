import os
import shutil
import sys 
import time
import pyfiglet
import paramiko
import requests
from zipfile import ZipFile, BadZipFile
import pyminizip
from pathlib import Path


class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'


homePath = Path.home()


if os.geteuid() != 0:
   sys.exit(color.BOLD + color.RED + 'Must have root priv to run this script.' + color.END)

def getSourceCode():
	try:
		print(f'''

		----- Link Examples -----

		https://testing.com
		http://testing.com


			''')
		while True:
			print("Enter the url.")
			linkURL = input("> ")
			print("Enter the filename to save it to your current working directory.")
			fileName = input("> ")
			r = requests.get(linkURL)

			if r.status_code == 200:
				with open(str(fileName), "a+") as f:
					f.write(r.text)
					print(color.BOLD + color.GREEN + f"Source Code has been downloaded to {fileName}" + color.END)
			else:
				print(color.BOLD + color.RED + "Failed to upload downloaded code" + color.END)
	except KeyboardInterrupt:
		downloadFiles()



def downloadImages():
	try:
		print(f'''


		---- Example of Image URL ----

		SCHEMAS: 

		http://
		https://

			''')

		while True:
			print("Enter the url.")
			linkURL = input("> ")
			print("Enter the filename to save it as.")
			fileName = input("> ")
			r = requests.get(linkURL, stream = True)
			break

		if r.status_code == 200:
			with open(str(fileName), "wb") as z:
				shutil.copyfileobj(r.raw, z)
				print("Image File Successfully Downloaded")
		else:
			print("Image File Failed Download")
	except KeyboardInterrupt:
		downloadFiles()


def moveMultipleFiles():
	global homePath

	filess = ''
	fileList = []
	try:
		print(f'''

		----- Move Multiple Files -----

		Example of Folder Path = home/user/folder

		Note - Do CTRL-C to go back to the menu at any time.

			''')
		while True:
			folderPath = input("Enter path to folder -->  ")
			fileAmount = input(f"How many files would you like to transfer at once to {folderPath}: ")
			if int(fileAmount) < 0:
				break
				print("Enter a valid number")
				manageFiles()
			for i in range(int(fileAmount)):
				filess = input("Enter File Path>")
				fileList.append(filess)

			for files in fileList:
				shutil.move(files, folderPath)

			break
		print(color.BOLD + color.GREEN + f"Transfer of {fileAmount} files has been sent to {folderPath}" + color.END)
		manageFiles()
	except KeyboardInterrupt:
		mainMenu()

def createZIP():
	fileList = []
	fileQuotes = []

	print(f'''

	----- Password Protected ZIP Creator -----

	Example of ZIP name - test.zip
	
	----- Note -----

	The files you want to zip must be in your current working directory.


		''')
	print("Name of zip file to be created?")
	zipFileName = input("> ")
	print("Name of password for your zip file?")
	passwordFile = input("> ")
	FilesToBeTransfered = input(f"Amount of files to transfer to {zipFileName}:")

	if int(FilesToBeTransfered.strip()) == 1:
		print("Enter the file path.")
		OneFilePath = input("> ")
		pyminizip.compress(OneFilePath, None, zipFileName, passwordFile, 5)
		print(color.BOLD + color.GREEN + f"ZIP File has been succesfully created." + color.END)
		createZIP()
	else:
		for fileNames in range(int(FilesToBeTransfered)):
			files = input(f"FILE NAME-{fileNames}>")
			fileList.append(files)

		for quotes in range(int(FilesToBeTransfered)):
			fileQuotes.append("")

		
		print(color.BOLD + color.GREEN + "Created Zip. Now sending files." + color.END)


		pyminizip.compress_multiple(fileList, fileQuotes, zipFileName, passwordFile, 5)
		print(color.BOLD + color.GREEN + "File Transfer Completed. ZIP has been created." + color.END)


def sftpClient():
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	cmd = ['ls', 'chdir', 'pwd', 'get', 'put']

	current_directory = "/"

	print(f'''

		COMMANDS 

		ls - List Files
		chdir - Change Directory
		pwd - Get current working directory
		get - Get a file from your remote machine
		put - Transfer a file from your local machine the remote machine

		''')
	ip = input("Specify the IP address: ")
	user = input("Enter the user: ")
	passwd = input("Enter the password: ")
	portnumber = input("Enter the port: ")
	ssh.connect(hostname=ip, username=user, password=passwd, port=portnumber)
	print(f"Succesfully Connected To {color.BOLD + ip + color.END}")
	sftp_client = ssh.open_sftp()
	sftp_client.chdir(current_directory)


	while True:
		commandline = input(f"{color.BOLD + ip + color.END}>")
		for commands in cmd:
			if commandline in commands:
				if commandline == "ls":
					print(sftp_client.listdir())
				elif commandline == "chdir":
					change_directory = input(f"{color.BOLD + 'chdir>' + color.END}")
					try:
						sftp_client.chdir(change_directory)
					except:
						print("No such directory found")
				elif commandline == "pwd":
					print(sftp_client.getcwd())
				elif commandline == "get":
					print("Make sure to enter the full path of")
					get_file = input(f"{color.BOLD + 'get>' + color.END}")
					try:
						sftp_client.get(get_file, get_file)
					except:
						print("File does not exist.")
				elif commandline == "put":
					print("Enter full path to file if its not in your current working directory")
					print("All transfered files go to the /tmp directory")
					put_file = input(f"{color.BOLD + 'put>' + color.END}")
					sftp_client.put(put_file, f"/tmp/{put_file}")
				else:
					print("Invalid Command")
		
	

def smbClient():
	print(f'''
		{color.BOLD + color.GREEN + "SOON COMING..." + color.END}
		''')
	remoteFileManagement()


def downloadFiles():
	print(f'''

	---- DOWNLOAD FILES ----


	1. Get source code of any website
	2. Download Images



		''')
	while True:
		choice = input("Choose your number:")
		if choice.strip() == "1":
			getSourceCode()
		elif choice.strip() == "2":
			downloadImages()
		else:
			print("Invalid Number Chosen")


def manageFiles():
	print(f'''

	----- Manage Files -----

	1. Move Multipile Files
	2. Create Pass Protected ZIP Files


		''')
	while True:
		manageFileOption = input("Choose your number: ")
		if manageFileOption == "1":
			moveMultipleFiles()
		elif manageFileOption == "2":
			createZIP()
		else:
			print("Invalid Number Chosen")


def remoteFileManagement():
	print(f'''

	----- Remote File Management -----
	

	1. SMB (SOON COMING...)
	2. SFTP


		''')
	while True:
		choiceR = input("Choose a Number: ")

		if choiceR.strip() == "1":
			smbClient()
		elif choiceR.strip() == "2":
			sftpClient()
		else:
			print("Invalid Numbers")


def mainMenu():
	try:
		print(f'''

{colored(pyfiglet.figlet_format('EasyFile', font='slant'), 'green', attrs=['bold'])}

----------------------------------------------------------------------------------------------------------------------------------------

	1. {color.BOLD + 'Remote File Management' + color.END}
	2. {color.BOLD + 'Manage Files' + color.END}
	3. {color.BOLD + 'Download Files From The Internet' + color.END}


-----------------------------------------------------------------------------------------------------------------------------------------
CTRL-C To Go Back Anytime.
			''')
		while True:
			choice = input("Choose a Number: ")

			if choice.strip() == "1":
				remoteFileManagement()
			elif choice.strip() == "2":
				manageFiles()
			elif choice.strip() == "3":
				downloadFiles()
			else:
				print("Invalid Choice")
	except KeyboardInterrupt:
		sys.exit("\n Exiting Program...")



def main():
	dot = "."
	checkSystem = "Checking your system before starting EasyFile Management System."

	for i in range(3):
		os.system("clear")
		print(checkSystem)
		time.sleep(0.5)
		os.system("clear")
		checkSystem = checkSystem + dot
		checkSystem.replace(checkSystem, checkSystem)


	if sys.platform != "win32" or "win64":
		print(color.BOLD + color.GREEN + "\t Linux Detected" + color.END)
		time.sleep(0.1)
		os.system("clear")
		mainMenu()
	else:
		print(color.BOLD + color.RED + "EasyFile Management System only supports Linux Machines" + color.END)
		sys.exit()

if __name__ == "__main__":
	main()
	









