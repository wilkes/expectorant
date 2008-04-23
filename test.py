from __future__ import with_statement
from expectorant import mock, Mockery, Expectation, VerificationFailure, surely, surely_not, raises, same_as, is_same_as, is_the_same_as
import unittest
import operator

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
        surely(lambda: mock.verify(), VerificationFailure,
            "<Expectation 'FailingMock.doit'> expected to be called 1 times, but was called 0 times")

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
        surely(lambda: self.exp.verify(), raises, VerificationFailure, 
            "<Expectation 'ParentMock.test'> expected to be called 2 times, but was called 0 times")

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
        surely(self.exp, raises, VerificationFailure)
    
    def test_expecting_args_length_passes(self):
        self.exp.with_args(1, 2 , 3, four=4, five=5)                
        self.exp(1, 2, 3, four=4, five=5)
    
    def test_expecting_args_values_passes(self):
        self.exp.with_args(mock.One, mock.Two)
        self.exp(mock.One, mock.Two)

    def test_expecting_args_values_fails(self):
        self.exp.with_args(mock.One, mock.Two)
        surely(lambda: self.exp(mock.One, 2), raises, VerificationFailure,
                "<Expectation 'ParentMock.test'> at position 1: expected: <Mock 'Two'> received: 2")
        
    def test_expecting_kwargs_values_passes(self):
        self.exp.with_args(one=1, two=2)
        self.exp(one=1, two=2)

    def test_expecting_kwargs_values_fails(self):
        self.exp.with_args(one=1, two=2)
        surely(lambda: self.exp(one=1, two=3), raises, VerificationFailure,
                "<Expectation 'ParentMock.test'> keyword two: expected: 2 received: 3")

    def test_chaining_with_with_args(self):
        assert self.exp == self.exp.with_args([])

    def test_chaining_called(self):
        assert self.exp == self.exp.called(1)

    def test_chaining_returns(self):
        assert self.exp == self.exp.returns(1)
        
class SurelyTest(unittest.TestCase):
    def test_surely_operator_is(self):
        surely(1, same_as, 1)
        surely(1, is_same_as, 1)
        surely(1, is_the_same_as, 1)
            
    def test_surely_not_operator_is(self):
        surely_not(2, same_as, 1)
        
    def test_same_as_message(self):
        surely(lambda: surely(1, same_as, 2), raises,  VerificationFailure, '1 is not the same as 2')

    def test_same_as_not_message(self):
        surely(lambda: surely_not(1, same_as, 1), raises, VerificationFailure, '1 is the same as 1')

    def test_custom_error(self):
        def barfs(x): assert False, 'Barf!'
        surely(lambda: surely(1, barfs), raises, AssertionError, 'Barf!')
        
    def test_unary(self):
        is_the_truth = lambda x: x is True
        is_the_truth.surely_message = lambda x: "%s is not True" % x
        is_the_truth.surely_not_message = lambda x: "%s is True" % x

        surely(True, is_the_truth)
        surely(lambda: surely(False, is_the_truth), raises, VerificationFailure, "False is not True")            
        surely_not(False, is_the_truth)
        surely(lambda: surely_not(True, is_the_truth), raises, VerificationFailure, "True is True")