from __future__ import with_statement
from expectorant import Mockery, mock, Expectation, VerificationFailure
import unittest

class MockedExpection:
    def __init__(self):
        self.count = 0
        
    def verify(self):
        self.count += 1

class ExpectorantTest(unittest.TestCase):
    def setUp(self):
        mock.reset()
        self.before_each()
    
    def before_each(self): pass


class MockeryTest(ExpectorantTest):
    def test_verify_all(self):
        mock.FailingMock.receives('doit').called(1)
        try:
            mock.verify()
            self.fail()
        except VerificationFailure, e:
            assert str(e) == "<Expectation 'FailingMock.doit'> expected to be called 1 times, but was called 0 times", str(e)

    def test_with_statement(self):
        exps = [MockedExpection() for i in range(10)]
        mock.Mocked.expectations = exps
        with mock: 
            for exp in exps: assert exp.count == 0, str(exp.count)
        for exp in exps: assert exp.count == 1, str(exp.count)

    def test_with_statement_style2(self):
        exps = [MockedExpection() for i in range(10)]
        with Mockery() as m: 
            m.Mocked.expectations = exps
            for exp in exps: assert exp.count == 0, str(exp.count)
        for exp in exps: assert exp.count == 1, str(exp.count)

    def test_manual(self):
        exps = [MockedExpection() for i in range(10)]
        mock.Mocked.expectations = exps
        mock.verify()
        for exp in exps: assert exp.count == 1, str(exp.count)

        
class MockTest(ExpectorantTest):    
    def before_each(self):
        self.mocked = mock.Mocked

    def test_name(self):
        assert self.mocked.name == 'Mocked'

    def test_identity(self):
        assert mock.Mocked is self.mocked
    
    def test_verify(self):
        exps = [MockedExpection() for i in range(10)]
        mock.Mocked.expectations = exps
        mock.Mocked.verify()
        for exp in exps: assert exp.count == 1, str(exp.count)
        
        
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
        
    def test_chaining_with_with_args(self):
        assert self.exp == self.exp.with_args([])

    def test_chaining_called(self):
        assert self.exp == self.exp.called(1)

    def test_chaining_returns(self):
        assert self.exp == self.exp.returns(1)
        
    