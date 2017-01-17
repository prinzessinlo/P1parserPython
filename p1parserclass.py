class P1Parser:
    Parserstates = {"PARSER_LOOKING_FOR_BEGIN", "PARSER_LOOKING_FOR_LETTER1", "PARSER_LOOKING_FOR_LETTER2",
                    "PARSER_LOOKING_FOR_LETTER3", "PARSER_LOOKING_FOR_NUMBER", "PARSER_LOOKING_FOR_CR1", "PARSER_LOOKING_FOR_LF1",
                    "PARSER_LOOKING_FOR_CR2", "PARSER_LOOKING_FOR_LF2", "PARSER_LOOKING_FOR_DATAGeneral", "PARSER_LOOKING_FOR_ENDOFBLOC",
                    "PARSER_LOOKING_FOR_CRC", "PARSER_LOOKING_FOR_CR", "PARSER_LOOKING_FOR_LF"}

    def __init__(self):  # Notre méthode constructeur
        self.ListofDataValues = [0, 0, 0, 0]
        self.type = 0
        self.value = 0
        self.DotSeen = False
        self.ParenthesisSeen = False
        self.ColonSeen = False
        self.StarSeen = False

    def __getattr__(self, ListofDataValues):
        return self.ListofDataValues
    def p1parserscanner(self, c):
        if c == ':':
            self.type = 0
            self.value = 0
            self.ColonSeen = True
            return 0
        elif c == '(':
            if (self.type == 0):
                self.type = self.value
            self.value = 0
            self.DotSeen = False
            self.ColonSeen = False
            self.ParenthesisSeen = True
            return 0
        elif c == '.':
            self.DotSeen = True
            return 0
        elif c == ')':
            if (self.DotSeen == True) and (self.type != 0):
                return True
            return 0
        elif c == '*':
            self.StarSeen = True
        elif c.isdigit() and ((self.ParenthesisSeen == True) or (self.ColonSeen == True) or (self.DotSeen == True)):
            b = int(float(c))
            self.value = 10 * self.value + b
        elif c.isalpha and not self.StarSeen:
            self.value = 0
            self.ParenthesisSeen = False
            self.WrongValueIsHere = True
            return 0
        elif (self.StarSeen) and (c == 'k' or c == 'W' or c == 'h'):
            return 0
        else:
            self.DotSeen = False
            self.ParenthesisSeen = False
            self.ColonSeen = False
            self.StarSeen = False
        return 0
#=======================================
    def P1P_GetValue(self):
        if (self.type >= 100) and (self.type <= 999):
            return self.value
        else:
            return 0
# =======================================
    def P1P_GetType(self):
        if (self.type >= 100) and (self.type <= 999):
            return self.type
        else:
            return 0  # non valid type
