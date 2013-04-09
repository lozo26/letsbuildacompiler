import unittest
import StringIO

from cradle import Cradle

class TestCradle(unittest.TestCase):

    def setUp(self):
        self.inf = StringIO.StringIO()
        self.outf = StringIO.StringIO()
        self.cradle = Cradle(self.inf, self.outf)

    def test_getCharSingle(self):
        inStr = 'Cain Pena'
        inf = StringIO.StringIO(inStr)
        expectedChar = inStr[0]
        cradle = Cradle(inf, None)
        cradle.getChar()
        self.assertEqual(expectedChar, cradle.look)

    def test_getCharMany(self):
        inStr = 'Cain Pena'
        inf = StringIO.StringIO(inStr)
        cradle = Cradle(inf, None)
        for i in xrange(len(inStr)):
            expectedChar = inStr[i]
            cradle.getChar()
            self.assertEqual(expectedChar, cradle.look)

    def test_error(self):
        outf = StringIO.StringIO()
        cradle = Cradle(None, outf)
        cradle.error('hello world')
        self.assertEqual(outf.getvalue(), '\nError: hello world.')

    def test_abort(self):
        outf = StringIO.StringIO()
        cradle = Cradle(None, outf)
        cradle.abort('Integer')
        self.assertEqual(outf.getvalue(), '\nError: Integer.')
        self.assertFalse(cradle.go)

    def test_expected(self):
        outf = StringIO.StringIO()
        cradle = Cradle(None, outf)
        cradle.expected('Integer')
        self.assertEqual(outf.getvalue(), '\nError: Integer Expected.')

    def test_matchSuccess(self):
        inStr = 'Cain Pena'
        inf = StringIO.StringIO(inStr)
        outf = StringIO.StringIO()
        expectedChar = inStr[0]
        cradle = Cradle(inf, outf)

        cradle.getChar()
        cradle.match(expectedChar)

        # after match, look reads next char
        self.assertEqual(inStr[1], cradle.look)

    def test_matchFail(self):
        inStr = 'Cain Pena'
        inf = StringIO.StringIO(inStr)
        outf = StringIO.StringIO()
        expectedChar = 'Z'
        cradle = Cradle(inf, outf)

        cradle.getChar()
        cradle.match(expectedChar)

        # after failed match, error shows
        self.assertEqual(outf.getvalue(), "\nError: 'Z' Expected.")

    def test_getNameSuccess(self):
        inStr = 'Cain Pena'
        inf = StringIO.StringIO(inStr)
        outf = StringIO.StringIO()
        cradle = Cradle(inf, outf)

        cradle.getChar()
        c = cradle.getName()
        self.assertEqual(c, inStr[0])
        
    def test_getNameFail(self):
        inStr = '1234'
        inf = StringIO.StringIO(inStr)
        outf = StringIO.StringIO()
        cradle = Cradle(inf, outf)

        cradle.getChar()
        cradle.getName()
        self.assertEqual(outf.getvalue(), "\nError: Name Expected.")

    def test_getNumSuccess(self):
        inStr = '1234'
        inf = StringIO.StringIO(inStr)
        outf = StringIO.StringIO()
        cradle = Cradle(inf, outf)

        cradle.getChar()
        c = cradle.getNum()
        self.assertEqual(c, inStr[0])
        
    def test_getNumFail(self):
        inStr = 'Cain Pena'
        inf = StringIO.StringIO(inStr)
        outf = StringIO.StringIO()
        cradle = Cradle(inf, outf)

        cradle.getChar()
        cradle.getNum()
        self.assertEqual(outf.getvalue(), "\nError: Integer Expected.")
 
    def test_emit(self):
        outf = StringIO.StringIO()
        cradle = Cradle(None, outf)

        cradle.emit('cain pena')
        self.assertEqual(outf.getvalue(), "\tcain pena")

    def test_emitLn(self):
        outf = StringIO.StringIO()
        cradle = Cradle(None, outf)

        cradle.emitLn('cain pena')
        self.assertEqual(outf.getvalue(), "\tcain pena\n")

if __name__ == '__main__':

    unittest.main()
