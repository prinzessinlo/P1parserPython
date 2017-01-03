# from ExtractValues import *

from P1scanner import *

DataFromTelegram = ""  # buffer which contain the telegram as string
buffersize = 0  # size of telegram length

DataFromTelegram = "1-0:1.8.0(000688.01*kWh)\n1-0:2.8.0(000131.72*kWh)\n1-0:1.7.0(000220.08*kWh)\n1-0:2.7.0(000999.08*kWh)\n"
buffersize = len(DataFromTelegram)
ListofDataValues = [0, 0, 0, 0]
type = 0
value = 0


def p1parserscanner(c):
    global type
    global value
    global DotSeen
    global ParenthesisSeen
    global ColonSeen
    global StarSeen

    if c == ':':
        type = 0
        value = 0
        ColonSeen = True
        return 0
    elif c == '(':
        if (type == 0):
            type = value
        value = 0
        DotSeen = False
        ColonSeen = False
        ParenthesisSeen = True
        return 0
    elif c == '.':
        DotSeen = True
        return 0
    elif c == ')':
        if (DotSeen == True) and (type != 0):
            return True
        return 0
    elif c == '*':
        StarSeen = True
    elif c.isdigit() and ((ParenthesisSeen == True) or (ColonSeen == True) or (DotSeen == True)):
        b = int(float(c))
        value =10*value+b
        #print(value)
    elif c.isalpha and not(StarSeen):
        value = 0
        ParenthesisSeen = False
        WrongValueIsHere = True
        return 0
    elif (StarSeen) and (c == 'k' or c == 'W' or c == 'h'):
        return 0
    else:
        p1pDotSeen = False
        p1pParenthesisSeen = False
        p1pColonSeen = False
        p1pStarSeen = False
    return 0


def P1P_GetValue():
    if (type >= 100) and (type <= 999):
        return value
    else:
        return 0


def P1P_GetType():
    if (type >= 100) and (type <= 999):
        return type
    else:
        return 0  # non valid type


def extractvalues(DataFromTelegram):
    meterValue = 0
    meterType = 0
    global ListofDataValues
    global a, b, c, d
    for letter in DataFromTelegram:
        if (p1parserscanner(letter)):
            #print("Je suis là!")
            meterType = P1P_GetType()
            meterValue = P1P_GetValue()
            if meterType == 180:
                ListofDataValues[0] = meterValue  # energyConsumed
                a= meterValue  # energyConsumed
            elif meterType == 280:
                ListofDataValues[1] = meterValue  # energyProduced
                b= meterValue  # energyProduced
            elif meterType == 170:
                ListofDataValues[2] = meterValue  # powerConsumed
                c= meterValue  # powerConsumed
            elif meterType == 270:
                ListofDataValues[3] = meterValue  # powerProduced
                d= meterValue  # powerProduced

def f():
    global s
    print(s)
    s = "tu dois être global"
    print(s)


#-----------------------MAIN------------------------#

#for letter in DataFromTelegram:
    #print(letter)
DotSeen = False
ParenthesisSeen = False
ColonSeen = False
StarSeen = False
extractvalues(DataFromTelegram)
print("energyConsumed: ", ListofDataValues[0])
print("energyProduced: ", ListofDataValues[1])
print("powerConsumed: ", ListofDataValues[2])
print("powerProduced: ", ListofDataValues[3])
print("*****************")

#---------------------------
str1 = "Hello"
str2 = "World"
str3=str1+ str2
#print("str3: "+str3)

a = "9.9"

#b=int(float(a))
#print("b: ",b)
#x= int(float(a))
#print("x: ",x)

#s = "Tu appartients à main()"
#f()
#print(s)