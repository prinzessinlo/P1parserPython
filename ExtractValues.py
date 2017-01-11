from P1scanner import *


#extractvalues
DataFromTelegram="0-0:96.1.0(52127969)\n1-0:0.9.1(140217)\n1-0:0.9.2(150427)1-0:1.8.0(000688.01*kWh)\n1-0:1.8.1(000131.72*kWh)\n1-0:1.8.2(000000.08*kWh)\n"
buffersize=len(DataFromTelegram)
def extractvalues(DataFromTelegram, buffersize):
	meterValue=0
	meterType=0
	ListofDataValues=[0, 0, 0, 0]
	idx=0
	for letter in DataFromTelegram:
		if (letter) and (p1parserscanner(letter)):
			meterType = P1P_GetType()
			meterValue = P1P_GetValue()
			if meterType==180:
				ListofDataValues[0] = meterValue #energyConsumed
			elif meterType==280:
				ListofDataValues[1] = meterValue  # energyProduced
			elif meterType == 170:
				ListofDataValues[2] = meterValue  # powerConsumed
			elif meterType == 270:
				ListofDataValues[3] = meterValue  # powerProduced
