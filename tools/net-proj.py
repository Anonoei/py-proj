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

iCIDR = 0

def clear():
	if name == "nt":
		_ = system("cls")
	else:
		_ = system("clear")

NetworkBytes = []

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
		print("\t =                                                       =")
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
		else:
			sErrMsg = ("That's not a valid option!")
			continue
		sErrMsg = ""
		
def mSubnetting():
	sErrMsg = ""
	while (True):
		clear()
		sNetwork = ""
		Network = ""
		NetCIDR = ""
		NetFirst = ""
		NetLast = ""
		NetBroadcast = ""
		NetNext = ""
		NetHosts = ""
		NetNetworks = ""
		NetSM = ""
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
		NetID = lNetwork[0]
		NetFirst = lNetwork[1]
		NetLast = lNetwork[2]
		NetBroadcast = lNetwork[3]
		NetNext = lNetwork[4]
		NetHosts = lNetwork[5]
		NetNetworks = lNetwork[6]
		NetBV = lNetwork[7]
		NetOctInt = lNetwork[8]
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
		system("pause")
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
		elif (re.search("^/\d{1,2}$", sUsrInput)): # Usr Inputted CIDR Value
			sUsrInput = int((sUsrInput[1:]))
			if ((sUsrInput <= 32) and (sUsrInput >= 0)):
				iCIDR = sUsrInput
				iNetMask = CIDRtoNM(sUsrInput)
			else:
				sErrMsg = ("\t ERR: Invalid CIDR value! \"" + sUsrInput[1] + "\".")
				continue
		elif (re.search("^(\d{1,3}\.){3}\d{1,3}$", sUsrInput)): # Usr Inputted Subnet Mask 
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
		system("pause")
		sErrMsg = ""
	
	
def mSummarization():
	sErrMsg = ""
	while (True):
		sNetwork1 = ""
		sNetwork2 = ""
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
			system("pause")
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
			system("pause")
		else:
			sErrMsg = ("\t ERR: That's not a valid input! \"" + sUsrInput + "\".")
	
	
	
	
	
	
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
	""" Above for loop replaces
	if (iBitValue == 128):
		iCIDR = 1 + ((iOctOfInt - 1) * 8)
	elif (iBitValue == 64):
		iCIDR = 2 + ((iOctOfInt - 1) * 8)
	elif (iBitValue == 32):
		iCIDR = 3 + ((iOctOfInt - 1) * 8)
	elif (iBitValue == 16):
		iCIDR = 4 + ((iOctOfInt - 1) * 8)
	elif (iBitValue == 8):
		iCIDR = 5 + ((iOctOfInt - 1) * 8)
	elif (iBitValue == 4):
		iCIDR = 6 + ((iOctOfInt - 1) * 8)
	elif (iBitValue == 2):
		iCIDR = 7 + ((iOctOfInt - 1) * 8)
	elif (iBitValue == 1):
		iCIDR = (iOctOfInt * 8)
	if (iCIDR == 0):
		print("\t ERR: iCIDR Could not be set!")
		return
	else:
	"""
	return iCIDR
	
# Call Main Menu and start Script
MainMenu()
