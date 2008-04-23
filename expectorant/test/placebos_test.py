from __future__ import with_statement
from expectorant.placebos import Dispenser, Expectation
from expectorant.diagnosis import surely, raises, same_as, equals

class PlaceboExpectation(object):
    def __init__(self):
        self.count = 0
    
    def verify(self):
        self.count += 1


class TestDispenser(object):
    def setUp(self):
        global dispenser
        dispenser = Dispenser()

    def test_verify_all(self):
        dispenser.FailPlacebo.receives('doit').once()
        surely(lambda: dispenser.verify(), raises, AssertionError,
            "<Expectation 'FailPlacebo.doit'> expected to be called 1 times, but was called 0 times")

    def test_with_statement(self):
        exps = [PlaceboExpectation() for i in range(10)]
        dispenser.Mocked.expectations = exps
        with dispenser:
            for exp in exps: 
                surely(exp.count, equals, 0)
        for exp in exps: 
            surely(exp.count, equals, 1)

    def test_with_statement_style2(self):
        exps = [PlaceboExpectation() for i in range(10)]
        with Dispenser() as m:
            m.Mocked.expectations = exps
            for exp in exps: 
                surely(exp.count, equals, 0)
        for exp in exps: 
            surely(exp.count, equals, 1)

    def test_manual(self):
        exps = [PlaceboExpectation() for i in range(10)]
        dispenser.Mocked.expectations = exps
        dispenser.verify()
        for exp in exps: 
            surely(exp.count, equals, 1)

class TestPlacebo(object):
    def setUp(self):
        global dispenser
        dispenser = Dispenser()
        self.placebo = dispenser.Placebo
    
    def test_name(self):
        surely(self.placebo.name, equals, 'Placebo')
    
    def test_identity(self):
        surely(dispenser.Placebo, same_as, self.placebo)
    
    def test_verify(self):
        exps = [PlaceboExpectation() for i in range(10)]
        dispenser.Placebo.expectations = exps
        dispenser.Placebo.verify()
        for exp in exps: 
            surely(exp.count, equals, 1)

class TestExpectation(object):
    def setUp(self):
        self.exp = Expectation(dispenser.Parent, 'test')

    def test_parent_mock_sugar(self):
        surely(self.exp.mock, same_as, dispenser.Parent)

    def test_once_passes(self):
        self.exp.once()
        self.exp()
        self.exp.verify()

    def test_called_fails(self):
        self.exp.twice()
        surely(lambda: self.exp.verify(), raises, AssertionError,
            "<Expectation 'Parent.test'> expected to be called 1 times, but was called 0 times")

    def test_twice_passes(self):
        self.exp.twice()
        self.exp()
        self.exp()
        self.exp.verify()

    def test_called_fails(self):
        self.exp.twice()
        surely(lambda: self.exp.verify(), raises, AssertionError,
            "<Expectation 'Parent.test'> expected to be called 2 times, but was called 0 times")

    def test_called_passes(self):
        self.exp.called(3)
        self.exp()
        self.exp()
        self.exp()
        self.exp.verify()

    def test_called_fails(self):
        self.exp.called(3)
        surely(lambda: self.exp.verify(), raises, AssertionError,
            "<Expectation 'Parent.test'> expected to be called 3 times, but was called 0 times")

    def test_returns(self):
        self.exp.returns(1)
        surely(self.exp(), equals, 1)

    def test_expecting_args_length_fails(self):
        self.exp.with_args(1, 2 , 3, four=4, five=5)
        surely(self.exp, raises, AssertionError)

    def test_expecting_args_length_passes(self):
        self.exp.with_args(1, 2 , 3, four=4, five=5)
        self.exp(1, 2, 3, four=4, five=5)

    def test_expecting_args_values_passes(self):
        self.exp.with_args(dispenser.One, dispenser.Two)
        self.exp(dispenser.One, dispenser.Two)

    def test_expecting_args_values_fails(self):
        self.exp.with_args(dispenser.One, dispenser.Two)
        surely(lambda: self.exp(dispenser.One, 2), raises, AssertionError,
                "<Expectation 'Parent.test'> at position 1: expected: <Mock 'Two'> received: 2")

    def test_expecting_kwargs_values_passes(self):
        self.exp.with_args(one=1, two=2)
        self.exp(one=1, two=2)

    def test_expecting_kwargs_values_fails(self):
        self.exp.with_args(one=1, two=2)
        surely(lambda: self.exp(one=1, two=3), raises, AssertionError,
                "<Expectation 'Parent.test'> keyword two: expected: 2 received: 3")

    def test_chaining_with_with_args(self):
        surely(self.exp, equals, self.exp.with_args([]))

    def test_chaining_called(self):
        surely(self.exp, equals, self.exp.called(1))

    def test_chaining_once(self):
        surely(self.exp, equals, self.exp.once())

    def test_chaining_twice(self):
        surely(self.exp, equals, self.exp.twice())

    def test_chaining_returns(self):
        surely(self.exp, equals, self.exp.returns(1))
