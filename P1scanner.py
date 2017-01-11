#TOFIX function call in P1Parser.py

def testfunctioncall():
    global test
    print("test function call! ")
    test = 5005
    print(test)


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

