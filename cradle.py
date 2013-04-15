class Cradle:
    def __init__(self, inf, outf):
        self.outf = outf
        self.inf = inf
        self.go = False
        self.look = ''

    def getChar(self):
        '''Read new character from input stream'''
        self.look = self.inf.read(1)

    def error(self, s):
        '''Report an error'''
        self.outf.write('\nError: %s.' % s)
        
    def abort(self, s):
        '''Report an error and halt'''
        self.error(s)
        self.go = False
        raise ValueError(s)

    def expected(self, s):
        '''Report what was expected'''
        self.abort(s + ' Expected')

    def match(self, x):
        '''Match a specific input character'''
        if self.look == x:
            self.getChar()
        else:
            self.expected("'%s'" % x)

    def isAlpha(self, c):
        '''Recognize an Alpha Character'''
        return c.isalpha()

    def isDigit(self, c):
        '''Recognize a Decimal Digit'''
        return c.isdigit()

    def getName(self):
        '''Get an Identifier'''
        val = 0
        if not self.isAlpha(self.look):
            self.expected('Name')
        else:
            val = self.look.upper()
            self.getChar()
            return val #? maybe not intented?

    def getNum(self):
        '''Get a Number'''
        val = 0
        if not self.isDigit(self.look):
            self.expected('Integer')
        else:
            val = self.look
            self.getChar()
            return val #? maybe not intented?

    def emit(self, s):
        '''Output a String with Tab'''
        self.outf.write("\t%s" % s)

    def emitLn(self, s):
        '''Output a String with Tab and LF'''
        self.outf.write("\t%s\n" % s)

    def expression(self):
        '''Parse and Translate a Math Expression'''
        self.emitLn('MOV EAX, %s' % self.getNum())

    def start(self):
        self.go = True
        """while self.go:
            self.getChar()
            self.expression()"""
        self.getChar()
        self.expression()



def stdStreams():
    import sys
    c = Cradle(sys.stdin, sys.stdout)
    c.start()

def main():
    stdStreams()

if __name__ == '__main__':
	main()
