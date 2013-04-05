import sys

# Variable declarations
look = '' # Lookahead character

# Read New Character From Input Stream
def GetChar():
    global look
    look = sys.stdin.read(1)

# Report an Error
def Error(s):
    print ''
    print 'Error: ' + s + '.'

# Report Error and Halt
def Abort(s):
    Error(s)
    sys.exit()

# Report What Was Expected
def Expected(s):
    Abort(s + ' Expected')

# Match a Specific Input Character
def Match(x):
    global look
    if look == x:
        GetChar()
    else:
        Expected("'%s'" % x)

# Recognize an Alpha Character
def IsAlpha(c):
    return c.isalpha()

# Recognize a Decimal Digit
def IsDigit(c):
    return c.isdigit()

# Get an Identifier
def GetName():
    val = 0
    global look
    if not IsAlpha(look):
        Expected('Name')
    else:
        val = look.upper()
        GetChar()
        return val #? maybe not intented?

# Get a Number
def GetNum():
    val = 0
    global look
    if not IsDigit(look):
        Expected('Integer')
    else:
        val = look.upper()
        GetChar()
        return val #? maybe not intented?

# Output a String with Tab
def Emit(s):
    print '\t' , s

# Output a String with Tab and CRLF
def EmitLn(s):
    Emit(s)
    print '\n'

# Initialize 
def Init():
    GetChar()

#def main():
#	Init()

#if __name__ == '__main__':
#	main()
