from expectorant import mock, Expectation, VerificationFailure
import unittest

class ExpectorantTest(unittest.TestCase):
    def setUp(self):
        mock.reset()
        self.before_each()
    
    def before_each(self): pass

class MockFactoryTest(unittest.TestCase):
    def test_verify_all(self):
        mock.FailingMock.receives('doit').called(1)
        try:
            mock.verify()
            self.fail()
        except VerificationFailure, e:
            assert str(e) == "<Expectation 'FailingMock.doit'> expected to be called 1 times, but was called 0 times", str(e)

class MockTest(ExpectorantTest):    
    def before_each(self):
        self.mock = mock.Mocked

    def test_name(self):
        assert self.mock.name == 'Mocked'

    def test_identity(self):
        assert mock.Mocked is self.mock
    
    def test_verify(self):
        exps = [getattr(mock, 'mock' + str(i)).receives('verify').called(1).mock for i in range(10)]
        self.mock.expecations = exps
        self.mock.verify()
        for exp in exps:
            exp.verify()

class ExpectationTest(ExpectorantTest):
    def before_each(self):
        self.exp = Expectation(mock.ParentMock, 'test')
    
    def test_parent_mock_sugar(self):
        assert self.exp.mock == mock.ParentMock

    def test_called_fails(self):
        self.exp.called(2)
        try:
            self.exp.verify()
            self.fail()
        except VerificationFailure, e:
            assert str(e) == "<Expectation 'ParentMock.test'> expected to be called 2 times, but was called 0 times", str(e)

    def test_called_passes(self):
        self.exp.called(2)
        self.exp()
        self.exp()
        self.exp.verify()
    
    def test_returns(self):
        self.exp.returns(1)
        assert 1 == self.exp()
    
    def test_expecting_args_length_fails(self):
        self.exp.with_args(1, 2 , 3, four=4, five=5)
        try:
            self.exp()
            self.fail()
        except VerificationFailure: pass

    def test_expecting_args_length_passes(self):
        self.exp.with_args(1, 2 , 3, four=4, five=5)                
        self.exp(1, 2, 3, four=4, five=5)
    
    def test_expecting_args_values_passes(self):
        self.exp.with_args(mock.One, mock.Two)
        self.exp(mock.One, mock.Two)

    def test_expecting_args_values_fails(self):
        self.exp.with_args(mock.One, mock.Two)
        try:
            self.exp(mock.One, 2)
            self.fail()
        except VerificationFailure, e:
            expected = "<Expectation 'ParentMock.test'> at position 1: expected: <Mock 'Two'> received: 2"
            assert str(e) == expected, str(e)
        
    def test_expecting_kwargs_values_passes(self):
        self.exp.with_args(one=1, two=2)
        self.exp(one=1, two=2)

    def test_expecting_kwargs_values_fails(self):
        self.exp.with_args(one=1, two=2)
        try:
            self.exp(one=1, two=3)
            self.fail()
        except VerificationFailure, e:
            assert str(e) == "<Expectation 'ParentMock.test'> keyword two: expected: 2 received: 3", str(e)
        
        