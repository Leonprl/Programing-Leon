from operator_overloading import Complex, Vector, Circle, Point, Matrix
from inheritance import Car, Bicycle, Student, BankAccount, SavingsAccount


def test_complex():
    assert Complex(1, 2) + Complex(3, 4) == Complex(4, 6)
    assert Complex(1, 2) - Complex(3, 4) == Complex(-2, -2)


def test_vector_dot():
    assert Vector(1, 2, 3) * Vector(4, 5, 6) == 32


def test_circle_and_point():
    assert Circle(1) < Circle(2)
    assert Circle(2) != Circle(3)
    assert Point(3, 4) == Point(0, 5)
    assert Point(1, 1) < Point(3, 4)


def test_matrix():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    assert a * b == Matrix([[19, 22], [43, 50]])


def test_inheritance():
    assert Car().drive() == "Driving a car"
    assert Bicycle().drive() == "Riding a bicycle"
    assert "I study AI" in Student("Leon", 19, "Paris", "AI").introduce()


def test_transfer():
    a = BankAccount("A", 100)
    s = SavingsAccount("B", 0, 0.1)
    assert a.transfer(s, 60)
    assert not a.transfer(s, 60)
    assert a.balance == 40
    s.add_interest()
    assert s.check_balance() == 66
