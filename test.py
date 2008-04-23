from expectorant import Mock, Expectation, sentinel, VerificationFailure
import unittest

class SentinelTest(unittest.TestCase):
    def test_bookkeeping(self):
        expected = sentinel.Expected
        assert expected is sentinel.Expected

class ExpectationTest(unittest.TestCase):
    def setUp(self):
        self.exp = Expectation('test')
    
    def test_called_fails(self):
        self.exp.called(2)
        try:
            self.exp.verify()
            self.fail()
        except VerificationFailure, e:
            assert str(e) == "Expected 'test' to be called 2 times, but was called 0 times", str(e)

    def test_called_passes(self):
        self.exp.called(2)
        self.exp()
        self.exp()
        self.exp.verify()
    
    def test_returns(self):
        self.exp.returns(1)
        assert 1 == self.exp()
    
    def test_expecting_args_length_fails(self):
        self.exp.expecting(1, 2 , 3, four=4, five=5)
        try:
            self.exp()
            self.fail()
        except VerificationFailure: pass

    def test_expecting_args_length_passes(self):
        self.exp.expecting(1, 2 , 3, four=4, five=5)                
        self.exp(1, 2, 3, four=4, five=5)
    
    def test_expecting_args_values_passes(self):
        self.exp.expecting(sentinel.One, sentinel.Two)
        self.exp(sentinel.One, sentinel.Two)

    def test_expecting_args_values_fails(self):
        self.exp.expecting(sentinel.One, sentinel.Two)
        try:
            self.exp(sentinel.One, 2)
            self.fail()
        except VerificationFailure, e:
            expected = 'position 1: expected: <SentinelObject "Two"> received: 2'
            assert str(e) == expected, str(e)
        
    def test_expecting_kwargs_values_passes(self):
        self.exp.expecting(one=1, two=2)
        self.exp(one=1, two=2)

    def test_expecting_kwargs_values_fails(self):
        self.exp.expecting(one=1, two=2)
        try:
            self.exp(one=1, two=3)
            self.fail()
        except VerificationFailure, e:
            assert str(e) == 'keyword two: expected: 2 received: 3', str(e)
        
        