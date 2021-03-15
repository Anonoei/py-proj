#######################################################################################
#                                                                                     #
#      MM   M   MMMM   MMMMM         MMM    MMM     MMM     MMMMM                     #
#      M M  M   M        M           M  M   M  M   M   M      M         MM   M M      #
#      M  M M   MMM      M     MMM   MMM    MMM    M   M      M         M M  M M      #
#      M   MM   M        M           M      M M    M   M   M  M         MM    M       #
#      M    M   MMMM     M           M      M  M    MMM     MM      X   M     M       #
#                                                                                     #
#######################################################################################
#------------------------------------  Ver 0.2.1  ------------------------------------#
#######################################################################################
#!/usr/bin/python3
# Author: Devon Adams (https://github.com/devonadams)
# License: GPLv3
######################################
#
## net-proj.py
#
# This script serves as a cheat sheat for networking
#    Subnetting w/ CIDR / mask
#    CIDR to NM / NM to CIDR Conversion
#    Network Summarization / Reverse Summarization
#    # Finding all IPs in network range
#    # Finding all UNUSED IPs in network
#    Mapping networks
## 
from os import system, name
from time import sleep
import re
#from graphics import *
import tkinter as tk
from tkinter import filedialog

iCIDR = 0

def clear():
	if name == "nt":
		_ = system("cls")
	else:
		_ = system("clear")

def pause():
	if name == "nt":
		_ = system("pause")
	else:
		input("Press any key to continue...")


#====------------------------------------------------------------------====
#=                        Begin Menu Functions
#====------------------------------------------------------------------====

def MainMenu():
	sErrMsg = ""
	while(True):
		clear()
		print("\n\t" + sErrMsg)
		print("\t =========================================================")
		print("\t =                M A I N   M E N U                      =")
		print("\t =========================================================")
		print("\t = 1) Subnetting                                         =")
		print("\t = 2) CIDR to Network Mask / Network Mask to CIDR        =")
		print("\t = 3) Network Summarization / Reverse Summarization      =")
		print("\t = 4) Automatic Network Mapping                          =")
		print("\t =                                                       =")
		print("\t =                                                       =")
		print("\t =                                                       =")
		print("\t =========================================================")
		sUsrInput = input("\t => What would you like to do? > ")
		if (sUsrInput.lower() == "exit"):
			print("\t See ya!")
			exit()
		elif (sUsrInput == "1"):
			mSubnetting()
		elif (sUsrInput == "2"):
			mCIDR_NM()
		elif (sUsrInput == "3"):
			mSummarization()
		elif (sUsrInput == "4"):
			mNetworkMapping()
		else:
			sErrMsg = ("That's not a valid option!")
			continue
		sErrMsg = ""
		
def mSubnetting():
	sErrMsg = ""
	while (True):
		clear()
		sNetwork = ""	#	Network String
		NetCIDR = ""		#	Stores Network CIDR
		NetFirst = ""		#	Stores First Network
		NetLast = ""		#	Stores Last Network
		NetBroadcast = ""	#	Stores Network Broadcast
		NetNext = ""		#	Stores Next Network
		NetHosts = ""		#	Stores Total Hosts
		NetNetworks = ""	#	Stores Total Networks
		NetSM = ""			#	Stores Network Subnet Mask
		print("\n\t" + sErrMsg)
		print("\t =========================================================")
		print("\t =                 S U B N E T T I N G                   =")
		print("\t =========================================================")
		print("\t =  Examples:  192.168.0.1/24                            =")
		print("\t =      Or 192.168.0.1 255.255.255.0                     =")
		print("\t =========================================================")
		sUsrInput = input("\t = Enter a Network > ")
		if (sUsrInput.lower() == "exit"):
			return
		elif (re.search("^(\d{1,3}\.){3}\d{1,3}/\d{1,2}", sUsrInput)): # IP and CIDR
			print("IP with CIDR")
			NetCheck = re.split("/|\.",sUsrInput)
			for item in NetCheck:
				if (int(item) > 255):
					sErrMsg = ("\t ERR: Invalid Network! \"" + sUsrInput + "\".")
					break
			if (int(NetCheck[4]) > 32):
				sErrMsg = ("\t ERR: Invalid CIDR! \"/" + str(NetCheck[4]) + "\".")
				break
			sNetwork = sUsrInput
			NetSM = CIDRtoNM(int(NetCheck[4]))
			NetCIDR = (int(NetCheck[4]))
		elif (re.search("^(\d{1,3}\.){3}\d{1,3} (\d{1,3}\.){3}\d{1,3}$", sUsrInput)): # IP and SM
			print("IP with NM")
			NetCheck = re.split("\s|\.", sUsrInput)
			for item in NetCheck:
				if (int(item) > 255):
					sErrMsg = ("\t ERR: Invalid Network! \"" + sUsrInput + "\".")
					break
			Networks = sUsrInput.split(" ")
			NetSM = Networks[1]
			NetCIDR = NMtoCIDR(NetSM)
			sNetwork = str(Networks[0]) + "/" + str(NetCIDR)
		else:
			sErrMsg = ("\t ERR: Invalid Input! \"" + sUsrInput + "\".")
			continue
		lNetwork = Subnet(sNetwork)
		NetID = lNetwork[0]			#
		NetFirst = lNetwork[1]		#
		NetLast = lNetwork[2]		#
		NetBroadcast = lNetwork[3]	#
		NetNext = lNetwork[4]		#
		NetHosts = lNetwork[5]		#
		NetNetworks = lNetwork[6]	#
		NetBV = lNetwork[7]			#
		NetOctInt = lNetwork[8]		#
		print("\n\n\t =========================================================")
		print("\t = > Network:" + str(sNetwork) + "\tBV: " + str(NetBV) + "\tOct: " + str(NetOctInt))
		print("\t ===========================================")
		print("\t = > Network ID:    N : \"" + str(NetID) + "/" + str(NetCIDR) + "\"")
		print("\t = > First Network: F : \"" + str(NetFirst) + "\"")
		print("\t = > Last Network:  L : \"" + str(NetLast) + "\"")
		print("\t = > Broadcast:     B : \"" + str(NetBroadcast) + "\"")
		print("\t = > Next Network:  X : \"" + str(NetNext) + "/" + str(NetCIDR) + "\"")
		print("\t =----------")
		print("\t = > Total Hosts:    \"" + str(NetHosts) + "\"")
		print("\t = > Total Networks: \"" + str(NetNetworks) + "\"")
		print("\t = > Subnet Mask:    \"" + str(NetSM) + "\"")
		print("\t ===============================\n\n")
		pause()
		sErrMsg = ""
	
def mCIDR_NM():
	sErrMsg = ""
	while (True):
		clear()
		iNetMask = ""
		print("\n\t" + sErrMsg)
		print("\t =========================================================")
		print("\t =              CIDR to NM // NM to CIDR                 =")
		print("\t =========================================================")
		print("\t =  Examples:   /24                                      =")
		print("\t =      Or 255.255.255.0                                 =")
		print("\t =========================================================")
		sUsrInput = input("\t = Enter a Value > ")
		if (sUsrInput.lower() == "exit"):
			return
		elif (re.search("^/\d{1,2}$", sUsrInput)):	#	 Usr Inputted CIDR Value
			sUsrInput = int((sUsrInput[1:]))
			if ((sUsrInput <= 32) and (sUsrInput >= 0)):
				iCIDR = sUsrInput
				iNetMask = CIDRtoNM(sUsrInput)
			else:
				sErrMsg = ("\t ERR: Invalid CIDR value! \"" + sUsrInput[1] + "\".")
				continue
		elif (re.search("^(\d{1,3}\.){3}\d{1,3}$", sUsrInput)):	#	Usr Inputted Subnet Mask 
			sUsrInput.split(".")
			iNM = []
			for item in sUsrInput:
					if (item == "."):
						iNM.append(item)
					elif (int(item) <= 255 ):
						iNM.append(item)
					else:
						sErrMsg = ("\t ERR: Invalid Subnetmask! \"" + sUsrInput[item] + "\".")
						continue
			for item in iNM:
				iNetMask += item
			iCIDR = NMtoCIDR(iNetMask)
		else:
			sErrMsg = ("\t ERR: That's not a valid input! \"" + sUsrInput + "\".")
			continue
		print("\n\n\t =========================================================")
		print("\t = > CIDR:    : /" + str(iCIDR))
		print("\t = > Netmask: : " + str(iNetMask))
		print("\t ==========\n\n")
		pause()
		sErrMsg = ""
	
	
def mSummarization():
	sErrMsg = ""
	while (True):
		sNetwork1 = ""	#	Stores Network 1 / Summarized Network
		sNetwork2 = ""	#	Storres Network 2
		clear()
		print("\n\t" + sErrMsg)
		print("\t =========================================================")
		print("\t =               S U M M A R I Z A T I O N               =")
		print("\t =========================================================")
		print("\t =  Examples:   128.16.0.0/12 (reverse)                  =")
		print("\t =   Or 128.21.21.34 128.29.2.3 (lowest / highest)       =")
		print("\t =========================================================")
		sUsrInput = input("\t = Enter a Value > ")
		if (sUsrInput.lower() == "exit"):
			return
		elif (re.search("^(\d{1,3}\.){3}\d{1,3} (\d{1,3}\.){3}\d{1,3}$", sUsrInput)): # Usr wants summarization
			sString = re.split("\s|\.", sUsrInput)
			for item in sString:
				if (item == " "):
					continue
				elif (item == "."):
					continue
				elif (int(item) > 255 ):
					sErrMsg = ("\t ERR: Invalid Network! \"" + str(item) + "\".")
					break
			SummarizedNetwork = Summarize(sUsrInput)
			for item in SummarizedNetwork:
				sNetwork1 += str(item)
			print("\n\n\t =========================================================")
			print("\t = > Summarized Network:\t " + str(sNetwork1))
			print("\t ==========\n\n")
			pause()
		elif (re.search("^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$", sUsrInput)):
			sString = re.split("\.|/", sUsrInput)
			print("sString: \"" + str(sString) + "\".")
			for item in sString:
				if (int(item) > 255):
					sErrMsg = ("\t ERR: Invalid Network! \"" + str(item) + "\".")
					break
			if (int(sString[4]) > 32):
				sErrMsg = ("\t ERR: Invalid CIDR! \"/" + str(sString[4]) + "\".")
				break
			rSummarizedNetworks = rSummarize(sUsrInput)
			sNetwork1 = rSummarizedNetworks[0]
			sNetwork2 = rSummarizedNetworks[1]
			print("\n\n\t =========================================================")
			print("\t = > Minimum Net:\t " + str(sNetwork1))
			print("\t = > Maximum Net:\t " + str(sNetwork2))
			print("\t ==========\n\n")
			pause()
		else:
			sErrMsg = ("\t ERR: That's not a valid input! \"" + sUsrInput + "\".")
	
def mNetworkMapping():
	sErrMsg = ""
	NetWin = GraphWin("Mapped Network", 1200, 800)	#	Create graphics.py instance
	NetWin.setBackground("white")
	while (True):
		clear()
		print("\n\t" + sErrMsg)
		print("\t =========================================================")
		print("\t =           N E T W O R K   M A P P I N G               =")
		print("\t =========================================================")
		print("\t =  Examples: Type 'load' to load file                   =")
		print("\t =   Or Enter router config line by line                 =")
		print("\t =========================================================")
		sUsrInput = input("\t = Enter an input > ")
		if (sUsrInput.lower() == "exit"):
			NetWin.close()
			return
		elif (sUsrInput.find("load") != -1):
			print("User is loading file")
			FilePath = filedialog.askopenfilename()
			MapNetwork(NetWin, FilePath, True)
			pause()
		else: # User is inputting config
			MapNetwork(NetWin, sUsrInput, False)
			print("mNM MyRouterInfo: " + str(MyRouterInfo))
			
	
	
	
#====------------------------------------------------------------------====
#=                        Begin Back-end Functions
#====------------------------------------------------------------------====
	
	
#=---------------------=
#=-   Map Network
#=---------------------=
def MapNetwork(NetWin, command, rType):
	print("Mapping network!")
	lCommand = ""
	lConfig = []
	iConfigSize = 0
	lineNum = 0		#	Stores Current Line Number
	pCommandUnk = False
	MyRouterInfo = ["Cisco RTR", "Non-Modular"]
	MyRouterInterfaces = []
	lInterfaceNumber = [0, 0]
	# Default Width: 1200 / Default Height: 800
	WinWidth = NetWin.getWidth()
	WinHeight = NetWin.getHeight()
	DefaultRouterWidth = 200
	DefaultRouterHeight = 200
	MyRouterWidth = 250
	MyRouterHeight = 100
	MyRouterIsModular = False
	MyRouter = Rectangle(Point(WinWidth/2, WinHeight/2), Point(WinWidth/2, WinHeight/2))
	MyRouterText = Text(Point((WinWidth/2), (WinHeight/2)), str(MyRouterInfo[0]))
	MyRouterInt = Rectangle(Point(0,0), Point(0,0))
	MyRouterIntText = Text(Point(0,0), "")
	
	lMyRouterIntSize = [50, 20, 5]
	while (True):
		if (rType == True):
			if (lineNum == 0):
				print("Attempting to load file!")
				ConfFile = open(command, 'r')
				lConfig = ConfFile.readlines()
				command = lConfig[0]
				iConfigSize = len(lConfig)
				print("ConfigSize: " + str(iConfigSize) + "\t LineNum: " + str(lineNum))
			else:
				if (iConfigSize == lineNum):
					print("Finished Reading File!")
					
					pause()
					return
				else:
					command = lConfig[lineNum]
		elif (rType == False):
			if (lineNum != 0):
				command = input("\tEnter an input > ")
				if (command.lower == "exit"):
					return
		
		elif (NetWin.isClosed()):
			return
		if (pCommandUnk == False):
			for item in NetWin.items[:]:
				item.undraw()
			NetWin.update()
		pCommandUnk = False
		lineNum += 1
		sStr = ""
		if (command.find("service") != -1):
			print("Found service!")
			continue
		elif (command.find("version") != -1): # Line is Version 
			print("Found Version!")
			sVer = command.split(" ")
			MyRouterInfo.append("Version: " + str(sVer[1]))
		elif (command.find("enable secret") != -1): # Line is Enable Secret
			print("Found Secret Pwd!"),
			sString = CalcMapPwdType(command)
			MyRouterInfo.append(sString)
		elif (command.find("enable password") != -1): # Line is Enable Password
			print("Found password!")
			sString = CalcMapPwdType(command)
			MyRouterInfo.append(sString)
		elif (command.find("hostname") != -1): # Line is setting hostname
			print("Found hostname!")
			lHN = command.split(" ")
			MyRouterInfo.append("Hostname: " + lHN[1])
		elif (command.find("username") != -1): # Line is creating User
			print("Found user!")
			lUsername = command.split(" ")
			sUsr = lUsername[1]
			sPriv = ""
			sPwd = ""
			if (lUsername[2] == "privilege"):
				sPriv = "Privilege: " + lUsername[3]
			if (lUsername[4] == "secret"):
				sPwd = "Secret: "
				if (lUsername[5] == "5"):
					sPwd += "MD5"
				elif (lUsername[5] == "7"):
					sPwd += "Type 7"
				elif (lUsername[5] == "9"):
					sPwd += "Type 9"
				else:
					sPwd += lUsername[5]
			elif (lUsername[4] == "password"):
				sPwd = "Password: "
				if (lUsername[5] == "5"):
					sPwd += "MD5"
				elif (lUsername[5] == "7"):
					sPwd += "Type 7"
				elif (lUsername[5] == "9"):
					sPwd += "Type 9"
				else:
					sPwd += lUsername[5]
			MyRouterInfo.append("User: " + sUsr + " " + sPriv + "\n" + sPwd)
		elif (command.find("snmp-server community") != -1):
			lSNMPComm = command.split(" ")
			MyRouterInfo.append("SNMP Community: " + lSNMPComm[2])
		elif (command.find("line") != -1):
			print("Found line!")
			lCommand = command
			continue
		elif (command.find("password") != -1): # Line is setting password for previous line creation command
			if (lCommand.find("line") != -1): # if a previous command created a line
				
				print("Found line password!",)
				lPwd = command.split(" ")
				sPwd = ""
				lLine = lCommand.split(" ")
				lLineType = lLine[1]
				sLineInfo = (lLineType.upper() + " " + lLine[2] + "-" + lLine[3])
				print(sLineInfo)
				sString = CalcMapPwdType(command)
				MyRouterInfo.append(sLineInfo + " " + sString)
			else:
				print("Unknown Password command!")
				pCommandUnk = True
				continue
		elif (command.find("interface") != -1): # Line is creating interface
			print("Found Interface!",)
			sIntType = ""
			sIntNum = ""
			iStartNum = 0
			iEndNum = 0
			# Find interface type
			if (command.find("GigabitEthernet") != -1):
				sIntType = "G"
			elif (command.find("FastEthernet") != -1):
				sIntType = "F"
			elif (command.find("Ethernet") != -1):
				sIntType = "E"
			elif (command.find("Serial") != -1):
				sIntType = "S"
			else:
				print("Unknown Interface Type!")
				pCommandUnk = True
				continue
			# Find interface number
			if (re.search("\d+/\d+(\.\d+)?$", command)): # Router is Modular and/or a sub interface
				MyRouterIsModular = True
				iStartNum = re.search("\d+/\d+(\.\d+)?$", command).start()
				iEndNum = len(command)
			elif (re.search("\d+$", command)): # Router is non-modular
				if (MyRouterIsModular == False):
					MyRouterIsModular = False
				iStartNum = re.search("\d+$", command).start()
				iEndNum = len(command)
			else:
				print("Unknown Interface Number!")
				pCommandUnk = True
				continue
				
			for index in range(iStartNum, iEndNum, 1):
					sIntNum += str(command[index])
			sInt = sIntType + sIntNum
			print(sInt)
			MyRouterInterfaces.append(sInt)
		else:
			print("Unknown command!")
			pCommandUnk = True
			continue
		# Draw items to screen
		if (len(MyRouterInterfaces) > 0):
			lRouterSize = [MyRouterWidth, MyRouterHeight]
			lWindowSize = [WinWidth, WinHeight]
			lInterfaceNumber = [0,0]
			for index in range(len(MyRouterInterfaces)):
				lDrawInt = CalcIntDrawLocation(index, MyRouterInterfaces[index], lInterfaceNumber ,lMyRouterIntSize, lRouterSize, lWindowSize)
				MyRouterInt = Rectangle(Point(lDrawInt[0], lDrawInt[1]), Point(lDrawInt[2], lDrawInt[3]))
				MyRouterIntText = Text(Point(lDrawInt[0] + lMyRouterIntSize[0]/2, lDrawInt[1] + lMyRouterIntSize[1]/2), MyRouterInterfaces[index])
				MyRouterText.setSize(8)
				for num in range(len(lInterfaceNumber)):
					lInterfaceNumber.pop()
				lInterfaceNumber.append(lDrawInt[4])
				lInterfaceNumber.append(lDrawInt[5])
				if (len(lDrawInt) > 6): # IntDrawLocation returned new router width / height
					MyRouterWidth += lDrawInt[6]
					MyRouterHeight += lDrawInt[7]
					print("whoa")
				MyRouterInt.draw(NetWin)
				MyRouterIntText.draw(NetWin)
		if not (MyRouterHeight > (len(MyRouterInfo) * 25)):
			MyRouterHeight = (len(MyRouterInfo) * 25)
		if (MyRouterIsModular == True):
			try:
				MyRouterInfo.remove("Non-Modular")
				MyRouterInfo.insert(1, "Modular")
			except:
				False
		else:
			try:
				MyRouterInfo.remove("Modular")
				MyRouterInfo.insert(1, "Non-Modular")
			except:
				False
		for item in MyRouterInfo:
			sStr += str(item) + "\n"
		MyRouterText.setTextColor("black")
		MyRouterText.setSize(10)
		MyRouterText.setText(str(sStr))
		MyRouterText.draw(NetWin)
		
		MyRouter = Rectangle(Point(WinWidth/2 - MyRouterWidth/2, WinHeight/2 - MyRouterHeight/2), Point(WinWidth/2 + MyRouterWidth/2, WinHeight/2 + MyRouterHeight/2))
		MyRouter.draw(NetWin)
		continue

#=----------------------------------------=
#=-   Calculate Interface Draw Location
#=----------------------------------------=
	
def CalcIntDrawLocation(intNum, sIntName, lIntNumbers, lIntSize, lRouterSize, lWindowSize):
	# lIntSize = [IntWidth(50), IntHeight(20), IntDefaultDistance(5)]
	# lRouterSize = [RouterWidth, RouterHeight]
	# lWindowSize = [WindowWidth, WindowHeight]
	lDrawLocation = []
	iDefaultX = 0 # Default top left value (for separating E/F/G from S)
	iDefaultY = 0
	
	iDrawTLx = 0 # Top Left corner of rectangle
	iDrawTLy = 0
	iDrawBRx = 0 # Bottom Right Corner of rectangle
	iDrawBRy = 0
	
	iRouterWidth = -1 # For changing Router width
	iRouterHeight = -1 # For changing Router height
	
	intNumMod = 0 # Stores how many numbers to subtract for the left side
	bFitOnRight = True
	bAddOnRight = True
	iMaxHeight = -((((lIntSize[1] * 0) + (lIntSize[2]) * 0) - lRouterSize[1])/((lIntSize[1] + lIntSize[2])))
	print("MaxHeight: " + str(iMaxHeight))
	if (lIntNumbers[0] < iMaxHeight): # Interface can fit on right side
		bFitOnRight = True
		print("Interface can fit on right side!")
	else:
		bFitOnRight = False
		print("Interface cannot fit on the right side")
		if (lIntNumbers[1] >= iMaxHeight):
			print("Cannot fit more interfaces!")
			iRouterHeight = (lIntSize[1] + lIntSize[2]) * 2
	
	if ((bFitOnRight == True) and ((sIntName[0] == "E") or (sIntName[0] == "F") or (sIntName[0] == "G"))):
		rTLx = (lWindowSize[0]/2 - lRouterSize[0]/2) # Router Top Left corner X
		rTLy = (lWindowSize[1]/2 - lRouterSize[1]/2)
		iDefaultX = ((rTLx + lRouterSize[0]) - lIntSize[0]) # Default Interface Top Left Corner X
		iDefaultY = (rTLy) # Default Interface Top Left Corner Y
	else:
		print("Let's move that to the left")
		if (bFitOnRight == True):
			bAddOnRight = False
			intNumMod = lIntNumbers[1]
		else:
			bAddOnRight = False
			intNumMod = lIntNumbers[0]
		rTLx = (lWindowSize[0]/2 - lRouterSize[0]/2) # Router Top Left corner X
		rTLy = (lWindowSize[1]/2 - lRouterSize[1]/2)
		iDefaultX = (rTLx) # Default Interface Top Left Corner X
		iDefaultY = (rTLy) # Default Interface Top Left Corner Y
				
	iDrawTLx = (iDefaultX)
	iDrawBRx = (iDefaultX + (lIntSize[0]))
	if (intNum == 0): # If first interface, we don't want the default spacing
		iDrawTLy = ((iDefaultY + ((lIntSize[1]) * ((intNum - intNumMod)))))
		iDrawBRy = (iDefaultY + ((lIntSize[1]) * ((intNum + 1) - intNumMod)))
	else:
		iDrawTLy = ((iDefaultY + ((lIntSize[1]) * (intNum - intNumMod))) + (lIntSize[2] * (intNum - intNumMod)))
		iDrawBRy = ((iDefaultY + ((lIntSize[1]) * ((intNum + 1) - intNumMod))) + (lIntSize[2] * (intNum - intNumMod)))
		
	"""
		Returns in this order:
		Top Left Corner X
		Top Left Corner Y
		Bottom Right Corner X
		Bottom Right Corner Y
		Total Right Side
		Total Left Side
		Can Include:
		New Router Width
		New Router Height
	"""
	lDrawLocation.append(iDrawTLx)
	lDrawLocation.append(iDrawTLy)
	lDrawLocation.append(iDrawBRx)
	lDrawLocation.append(iDrawBRy)
	if (bAddOnRight == True):
		lDrawLocation.append(int(lIntNumbers[0]) + 1)
		lDrawLocation.append(lIntNumbers[1])
	else:
		lDrawLocation.append(lIntNumbers[0])
		lDrawLocation.append(int(lIntNumbers[1]) + 1)
	if (iRouterHeight != -1):
		lDrawLocation.append(0)
		lDrawLocation.append(iRouterHeight)
	print("iDrawLocation: " + str(lDrawLocation))
	return lDrawLocation

#=------------------------------=
#=-   Calculate Password Type
#=------------------------------=
def CalcMapPwdType(sCommand):
	lCommand = sCommand.split(" ")
	sNameIndex = 0
	sTypeIndex = 1
	sPwd = ""
	sType = ""
	if (lCommand[0] == "enable"):
		sNameIndex = 1
		sTypeIndex = 2
		sType = "Enable "
	if (lCommand[sNameIndex] == "password"):
		sType += "Password: "
	elif (lCommand[sNameIndex] == "secret"):
		sType += "Secret: "
	if (lCommand[sTypeIndex] == "5"):
		sPwd = "MD5"
	elif (lCommand[sTypeIndex] == "7"):
		sPwd = "Type 7"
	elif (lCommand[sTypeIndex] == "9"):
		sPwd = "Type 9"
	else:
		sPwd = lCommand[sTypeIndex]
		
	rString = sType + sPwd
	return rString


#=---------------------=
#=-   Subnetting
#=---------------------=
def Subnet(Network):
	NetInfo = []
	print("Network is: " + str(Network) + "\".")
	iNetCIDR = Network.split("/")
	sNetwork = str(iNetCIDR[0]).split(".")
	iNetCIDR = int(iNetCIDR[1])
	print("sNetwork is: " + str(sNetwork) + "\".")
	BVandOct = CIDRInfoCalc(iNetCIDR)
	iBV = BVandOct[0]
	iOctInt = BVandOct[1]
	cOct = 1
	
	#Calculate Network ID
	NetID = ""
	lNetID = []
	for num in range(0,256,1):
		if ((iBV * num) > 255):
			break
		elif ((int(sNetwork[iOctInt - 1])) >= (iBV * num)) and ((int(sNetwork[iOctInt - 1])) <= (iBV * (num + 1))):
			if ((int(sNetwork[iOctInt - 1]) - 1) == (iBV * num)):
				num += 1
				continue
			print("Num: " + str(num) + "\tVal: " + str(iBV * num))
			while (cOct <= 4):
				if (cOct < iOctInt):
					NetID += str(sNetwork[cOct - 1])
				elif (cOct == iOctInt):
					NetID += str(iBV * (num))
				elif (cOct > iOctInt):
					NetID += "0"
				if not(cOct == 4):
					NetID += "."
				elif (cOct == 4):
					break
				cOct += 1
			break
		print("Checking: " + str(iBV * num))
	slNetID = NetID.split(".")
	print("slNetID: \"" + str(slNetID) + "\".")
	lNetID = []
	for item in slNetID:
		lNetID.append(int(item))
		
	#Calculate First Network
	print("lNedID: \"" + str(lNetID) + "\".")
	NetFirst = ""
	cOct = 1
	for item in lNetID:
		if (cOct < iOctInt):
			NetFirst += str(item)
		elif (cOct < 4):
			NetFirst += str(item)
		elif (cOct == 4):
			NetFirst += str(item + 1)
			break
		if (cOct < 4):
			NetFirst += "."
		cOct += 1
	#Calculate Last Network and Broadcast
	NetLast = ""
	NetBroadcast = ""
	cOct = 1
	for item in lNetID:
		if (cOct < iOctInt):
			NetLast += str(item)
			NetBroadcast += str(item)
		elif (cOct == iOctInt):
			if (iOctInt == 4):
				NetLast += str((item + iBV) - 2)
			else:
				NetLast += str((item + iBV) - 1)
			NetBroadcast += str((item + iBV) - 1)
		elif (cOct < 4):
			NetLast += "255"
			NetBroadcast += "255"
		elif (cOct == 4):
			NetLast += "254"
			NetBroadcast += "255"
		if (cOct < 4):
			NetLast += "."
			NetBroadcast += "."
		cOct += 1
	print("NetLast: " + NetLast)
	print("NetBroadcast: " + NetBroadcast)
	# Calculate Next Network
	NetNext =""
	cOct = 1
	for item in lNetID:
		if (cOct < iOctInt):
			NetNext += str(item)
		elif (cOct == iOctInt):
			NetNext += str(item + iBV)
		elif (cOct > iOctInt):
			NetNext += "0"
		if (cOct < 4):
			NetNext += "."
		cOct += 1
	print("NetNext: " + NetNext)
	# Calculate Total Hosts
	NetHosts = 32 - iNetCIDR
	NetHosts = ((2 ** NetHosts) - 2)
	# Calculate Total Networks
	iBC = 0
	if (lNetID[0] >= 0 and lNetID[0] <= 127):
		iBC = 8
	elif (lNetID[0] >= 128 and lNetID[0] <= 191):
		iBC = 16
	elif (lNetID[0] >= 192 and lNetID[0] <= 223):
		iBC = 24
	elif (lNetID[0] >= 224 and lNetID[0] <= 239):
		iBC = 32
	elif (lNetID[0] >= 240 and lNetID[0] <= 256):
		iBC = 40
	NetNetworks = iNetCIDR - iBC
	NetNetworks = ((2 ** NetNetworks))
	
	NetInfo.append(NetID)
	NetInfo.append(NetFirst)
	NetInfo.append(NetLast)
	NetInfo.append(NetBroadcast)
	NetInfo.append(NetNext)
	NetInfo.append(NetHosts)
	NetInfo.append(NetNetworks)
	NetInfo.append(iBV)
	NetInfo.append(iOctInt)
	return NetInfo
	
#=---------------------=
#=-   Summarization
#=---------------------=
def Summarize(Network):
	print("Summarizing Network")
	Network = re.split("\s|\.", Network)
	print("Network is: \"" + str(Network) + "\".")
	Network1 = []
	Network2 = []
	iOctInt = 0
	iNetInt1 = True
	iNetDif = 0
	iNetBV = 0
	sSummarizedNet = []
	for item in Network:
		if (iOctInt == 4):
			iNetInt1 = False
		if (item == "."):
			continue
		elif (re.search("\d{1,3}", item)):
			if (iNetInt1 == True):
				Network1.append(int(item))
			else:
				Network2.append(int(item))
			iOctInt += 1
	iOctInt = 1
	for index in range(0,4,1):
		if (Network1[index] == Network2[index]):
			iOctInt += 1
			sSummarizedNet.append(str(Network1[index]) + ".")
		else:
			try:
				iNetDif = (int(Network2[index]) - int(Network1[index]))
			except:
				try:
					iNetDif = (int(Network1[index] - int(Network2[index])))
				except:
					print("\t ERR: Invalid Network! \"" + str(Network1[index]) + "\" / \"" +  str(Network2[index]) + "\".")
					return
			break
	print("iNetDif: \"" + str(iNetDif) + "\"\t iOctInt: \"" + str(iOctInt) + "\".")
	bCalcDone = False
	for item in range(0, 8, 1): # Change Network Difference to power of 2
		if (bCalcDone == True):
			break
		elif (iNetDif <= (2 ** item)): # exponential
			iNetBV = (2 ** item)
			print("NetBV: \"" + str(iNetBV) + "\".")
			for num in range(1, 256, 1):
				if (iNetBV * (num) > 255):
					break
				elif (Network1[iOctInt - 1] >= (iNetBV * (num))):
					print("Min is: \"" + str((iNetBV * (num))) + "\" \t Max is: \"" + str(iNetBV * (num + 1)) + "\".")
					if (Network2[iOctInt - 1] <= iNetBV * (num + 1)):
						sSummarizedNet.append(iNetBV * (num))
						bCalcDone = True
						break
					else:
						break
				elif (Network1[iOctInt - 1] <= (iNetBV)):
					print ("Min is: 1, iNetBV: \"" + str(iNetBV) + "\".")
					if (Network2[iOctInt - 1] <= (iNetBV)):
						sSummarizedNet.append("0")
						bCalcDone = True
						break
					else:
						continue
						
				else:
					continue
			if (bCalcDone == True):
				for oct in range(4 - iOctInt):
					sSummarizedNet.append(".0")
				break
		else:
			continue
	# now we know the Network, and the BV, need CIDR
	iCIDRNum = 9
	for num in range(0, 8, 1):
		iCIDRNum -= 1
		print("Num: \"" + str(num) + "\" \t CheckValue: \"" + str(2 ** num) + "\" \t iCIDRNum: \"" + str(iCIDRNum) + "\".")
		if (iNetBV == 2 ** num):
			sSummarizedNet.append("/" + str((iCIDRNum) + ((iOctInt - 1) * 8)))
			break
	return sSummarizedNet
	
#=-----------------------------=
#=-   Reverse Summarization
#=-----------------------------=
	
def rSummarize(sNetwork):
	print("Reverse Summarizing Network")
	sNetwork = re.split("/|\.", sNetwork)
	Network = []
	for item in sNetwork:
		Network.append(int(item))
	print("Network is: \"" + str(Network) + "\".")
	MinNet = ""
	MaxNet = ""
	NetCIDR = Network[4]
	Networks = []
	index = 1
	BVandOct = CIDRInfoCalc(NetCIDR)
	iBV = int(BVandOct[0])
	iOctInt = int(BVandOct[1])
	print("iBV: \"" + str(iBV) + "\"\t iOctInt: \"" + str(iOctInt) + "\"\t Network Length: \"" + str(len(Network)) + "\".")
	for num in range (1, 256, 1):
		iOctInt = int(BVandOct[1])
		if ((iBV * num) > 255):
			break
		elif ((Network[iOctInt - 1]) <= (iBV * num)):
			if (Network[iOctInt - 1] == (iBV * num)):
				num += 1
			print("Num: \"" + str(num) + "\".")
			for item in Network:
				if ((index == 5)):
					break
				elif (index < iOctInt):
						MinNet += (str(item))
						MaxNet += (str(item))
				elif (index == iOctInt):
						MinNet += (str((iBV * (num - 1))))
						MaxNet += (str((iBV * num) - 1))
				elif (index > iOctInt):
						MinNet += ("0")
						MaxNet += ("0")
				if (not(index == 4)):
						MinNet += "."
						MaxNet += "."
				index += 1
				print("MinNet: \"" + MinNet + "\"\t MaxNet: \"" + MaxNet + "\".")
			break
		else:
			continue
	for num in range(1,5,1):
		if (NetCIDR <= ((num) * 8)):
			NetCIDR = ((num) * 8)
			break
	MinNet += ("/" + str(NetCIDR))
	MaxNet += ("/" + str(NetCIDR))
	Networks.append(MinNet)
	Networks.append(MaxNet)
	return Networks
	
#=------------------------------------------------------=
#=-   Calculate CIDR BitValue and Octet of Interest
#=------------------------------------------------------=

def CIDRInfoCalc(iCIDR):
	info = []
	iBitValue = 0
	intOctet = 0
	if ((iCIDR == 1) or (iCIDR == 9) or (iCIDR == 17) or (iCIDR == 25)):
		iBitValue = 128
	elif ((iCIDR == 2) or (iCIDR == 10) or (iCIDR == 18) or (iCIDR == 26)):
		iBitValue = 64
	elif ((iCIDR == 3) or (iCIDR == 11) or (iCIDR == 19) or (iCIDR == 27)):
		iBitValue = 32
	elif ((iCIDR == 4) or (iCIDR == 12) or (iCIDR == 20) or (iCIDR == 28)):
		iBitValue = 16
	elif ((iCIDR == 5) or (iCIDR == 13) or (iCIDR == 21) or (iCIDR == 29)):
		iBitValue = 8
	elif ((iCIDR == 6) or (iCIDR == 14) or (iCIDR == 22) or (iCIDR == 30)):
		iBitValue = 4
	elif ((iCIDR == 7) or (iCIDR == 15) or (iCIDR == 23) or (iCIDR == 31)):
		iBitValue = 2
	elif ((iCIDR == 8) or (iCIDR == 16) or (iCIDR == 24) or (iCIDR == 32)):
		iBitValue = 1
	else:
		print("\t ERR: INVALID CIDR VALUE! \"" + iCIDR + "\".")
		
	info.append(iBitValue)
	if (iCIDR >= 25):
		intOctet = 4
	elif (iCIDR >= 17):
		intOctet = 3
	elif (iCIDR >= 9):
		intOctet = 2
	elif (iCIDR >= 1):
		intOctet = 1
	else:
		print("\t ERR: INVALID CIDR VALUE! \"" + iCIDR + "\".")
		
	info.append(intOctet)
	return info

#=----------------------------------=
#=-   Convert CIDR to Subnet Mask
#=----------------------------------=
def CIDRtoNM(CIDR):
	print("\t Converting CIDR to NM \"" + str(CIDR) + "\".")
	iOctOfInt = 0
	iBitValue = 0
	iNetMask = ""
	if (CIDR >= 25):
		intOctet = 4
	elif (CIDR >= 17):
		intOctet = 3
	elif (CIDR >= 9):
		intOctet = 2
	else:
		intOctet = 1
	for item in range(intOctet - 1):
		iNetMask += "255."
		
	for item in range(0,5,1):
		if ((CIDR - (item * 8)) == 1):
			iNetMask += "128"
		elif ((CIDR - (item * 8)) == 2):
			iNetMask += "192"
		elif ((CIDR - (item * 8)) == 3):
			iNetMask += "224"
		elif ((CIDR - (item * 8)) == 4):
			iNetMask += "240"
		elif ((CIDR - (item * 8)) == 5):
			iNetMask += "248"
		elif ((CIDR - (item * 8)) == 6):
			iNetMask += "252"
		elif ((CIDR - (item * 8)) == 7):
			iNetMask += "254"
		elif ((CIDR - (item * 8)) == 8):
			iNetMask += "255"
			
	for item in range(4 - intOctet):
		iNetMask += ".0"
	return iNetMask
	
#=-----------------------------------=
#=-   Convert Subnet Mask to CIDR
#=-----------------------------------=

def NMtoCIDR(NetMask):
	global iCIDR
	iOctOfInt = 0
	iBitValue = 0
	NetMask = NetMask.split(".")
	print("\t Converting NM to CIDR")
	for item in NetMask:
		if ((item == ".") or (item == " ")):
			continue
		elif (item == 0):
			break
		elif (item == "255"):
			iBitValue = 1
		elif (item == "254"):
			iBitValue = 2
		elif (item == "252"):
			iBitValue = 4
		elif (item == "248"):
			iBitValue = 8
		elif (item == "240"):
			iBitValue = 16
		elif (item == "224"):
			iBitValue = 32
		elif (item == "192"):
			iBitValue = 64
		elif (item == "128"):
			iBitValue = 128
		else:
			break
		iOctOfInt += 1
		
	iCIDRNum = 9
	for num in range(0, 8, 1):
		iCIDRNum =- 1
		if (iBitValue == 2 ** num):
			iCIDR = ((iCIDRNum) + ((iOctOfInt - 1) * 8))
	return iCIDR
	
# Call Main Menu and start Script
MainMenu()
