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

    def factor(self):
        '''Parse and Translate a factor'''
        if self.look == '(':
            self.match('(')
            self.expression()
            self.match(')')
        else:
            self.emitLn('MOV EAX, %s     ;eax = INT' % self.getNum())

    def multiply(self):
        '''Recognize and translate a multiply'''
        self.match('*')
        self.factor()
        self.emitLn('MOV EBX, EAX   ;ebx = eax (ebx will hold 2nd factor)')
        self.emitLn('POP EAX        ;retrieve 1st factor from stack, store in eax')
        self.emitLn('IMUL EAX, EBX  ;eax *= ebx')

    def divide(self):
        '''Recognize and translate a divide'''
        self.match('/')
        self.factor()
        self.emitLn('MOV EBX, EAX   ;ebx = eax (ebx will hold 2nd factor)')
        self.emitLn('POP EAX        ;retrieve 1st factor from stack, store in eax')
        self.emitLn('CDQ            ;Sign extend eax into edx')
        self.emitLn('IDIV EBX       ;edx:eax / ebx, quotient in eax, rem in edx')

    def term(self):
        '''Parse and Translate a term'''

        '''Python doesn't have switch/case.  Using a dictionary
        of lambdas to simulate it.'''
        case = {'*': lambda: self.multiply()
               ,'/': lambda: self.divide()
               }
        default = lambda: self.expected('Mulop')

        self.factor()
        while self.look in ('*', '/'):
            self.emitLn('PUSH EAX       ;put eax on stack (eax hold result of most recenlty computed factor)')
            case.get(self.look, default)() # get() returns a lambda then the () invokes it

    def add(self):
        self.match('+')
        self.term()
        self.emitLn('MOV EBX, EAX   ;ebx = eax (ebx will hold 2nd term)')
        self.emitLn('POP EAX        ;retrieve 1st term from stack, store in eax')
        self.emitLn('ADD EAX, EBX   ;eax += ebx')

    def subtract(self):
        self.match('-')
        self.term()
        self.emitLn('MOV EBX, EAX   ;ebx = eax (ebx will hold 2nd term)')
        self.emitLn('POP EAX        ;retrieve 1st term from stack, store in eax')
        self.emitLn('SUB EAX, EBX   ;eax -= ebx')

    def expression(self):
        '''Parse and Translate an expression'''
        if self.isAddop(self.look):
            self.emitLn('XOR EAX, EAX   ;unary - or + so first operand is zero')
        else:
            self.term()

        '''Python doesn't have switch/case.  Using a dictionary
        of lambdas to simulate it.'''
        case = {'+': lambda: self.add()
               ,'-': lambda: self.subtract()
               }
        default = lambda: self.expected('Addop')

        while self.isAddop(self.look):
            self.emitLn('PUSH EAX       ;put eax on stack (eax holds result of most recently computed term)')
            case.get(self.look, default)() # get() returns a lambda then the () invokes it

    def isAddop(self, c):
        return c in ('+', '-')

    def start(self):
        self.getChar()      # initialization
        self.expression()   # get it going



def stdStreams():
    import sys
    c = Cradle(sys.stdin, sys.stdout)
    c.start()

def main():
    stdStreams()

if __name__ == '__main__':
	main()
