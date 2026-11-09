import math


# Problem 1 - complex numbers
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return Complex(self.real - other.real, self.imag - other.imag)

    def __eq__(self, other):
        return self.real == other.real and self.imag == other.imag

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        return f"{self.real} {sign} {abs(self.imag)}i"


# Problem 2 - compare persons by age
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __gt__(self, other):
        return self.age > other.age

    def __repr__(self):
        return f"Person({self.name}, {self.age})"


# Problem 4 - dot product
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


# Problem 5 - all comparisons on the radius
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def __lt__(self, other):
        return self.radius < other.radius

    def __gt__(self, other):
        return self.radius > other.radius

    def __eq__(self, other):
        return self.radius == other.radius

    def __ne__(self, other):
        return self.radius != other.radius

    def __le__(self, other):
        return self.radius <= other.radius

    def __ge__(self, other):
        return self.radius >= other.radius

    def __repr__(self):
        return f"Circle(r={self.radius})"


# Problem 6 - compare points with their distance to the origin
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __gt__(self, other):
        return self.distance() > other.distance()

    def __eq__(self, other):
        return self.distance() == other.distance()

    def __le__(self, other):
        return self.distance() <= other.distance()

    def __ge__(self, other):
        return self.distance() >= other.distance()

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# Problem 7 - matrix product
class Matrix:
    def __init__(self, rows):
        self.rows = rows
        self.n = len(rows)
        self.m = len(rows[0])

    def __mul__(self, other):
        if self.m != other.n:
            raise ValueError("incompatible sizes")
        result = []
        for i in range(self.n):
            line = []
            for j in range(other.m):
                s = 0
                for k in range(self.m):
                    s += self.rows[i][k] * other.rows[k][j]
                line.append(s)
            result.append(line)
        return Matrix(result)

    def __eq__(self, other):
        return self.rows == other.rows

    def __repr__(self):
        return "\n".join(str(r) for r in self.rows)


if __name__ == "__main__":
    print(Complex(1, 2) + Complex(3, -5))
    print(Complex(1, 2) - Complex(3, 5))

    alice = Person("Alice", 21, "F")
    bob = Person("Bob", 19, "M")
    print(alice > bob)

    print(Vector(1, 2, 3) * Vector(4, 5, 6))

    print(Circle(2) < Circle(3), Circle(2) == Circle(2), Circle(5) >= Circle(1))

    print(Point(3, 4) > Point(1, 1))

    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    print(a * b)
