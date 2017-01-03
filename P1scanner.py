type = 0
value = 0

def p1parserscanner(c):
    global type
    global value
    DotSeen= False
    ParenthesisSeen = False
    ColonSeen = False
    StarSeen = False
    if c == ':':
        type = 0
        value = 0
        ColonSeen =True
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
        if (DotSeen == 1) and (type != 0):
            return True
        return 0
    elif c == '*':
        StarSeen = True
    elif c.isalnum() and (ParenthesisSeen==True or ColonSeen==True or DotSeen==True):
        DsmrValue = 10 * value + (c - '0')
    elif c.isalpha and not (StarSeen):
        p1pDsmrValue = 0
        p1pParenthesisSeen = False
        p1pWrongValueIsHere = True
        return 0
    elif (p1pStarSeen) and (c == 'k' or c == 'W' or c == 'h'):
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
        return 0 #non valid type

