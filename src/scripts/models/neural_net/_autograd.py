from math import tanh, log, log10, exp
import numpy as np 

class Var:
    """
    A variable which holds a number and enables gradient computations.
    """

    def __init__(self, val, parents=None):
        assert type(val) in {float, int}
        if parents is None:
            parents = []
        self.v = val
        self.parents = parents
        self.grad = 0.0

    def backprop(self, bp):
        self.grad += bp
        for parent, grad in self.parents:
            parent.backprop(grad * bp)

    def backward(self):
        self.backprop(1.0)

    def __add__(self, other):
        return Var(self.v + other.v, [(self, 1.0), (other, 1.0)])

    def __mul__(self, other): 
        return Var(self.v * other.v, [(self, other.v), (other, self.v)])

    def __pow__(self, power):
        assert type(power) in {float, int}, "power must be float or int"
        return Var(self.v ** power, [(self, power * self.v ** (power - 1))])

    def __neg__(self):
        return Var(-1.0) * self

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        return self * other ** -1

    def __lt__(self, other):
        return self.v < other.v 

    def tanh(self):
        return Var(tanh(self.v), [(self, 1 - tanh(self.v) ** 2)])

    def relu(self):
        return Var(self.v if self.v > 0.0 else 0.0, [(self, 1.0 if self.v > 0.0 else 0.0)])

    def log(self):
        return Var(log10(self.v), [(self, 1 / self.v * log(10))]) 

    def exp(self):
        return Var(exp(self.v), [(self, exp(self.v))])

    def __float__(self):
        return self.v

    def __int__(self):
        return int(self.v)

    def __repr__(self):
        return f'{self.v}'
        #return f"Var(v={self.v}, grad={self.grad})"


if __name__ == '__main__':
    import numpy as np

    p = np.array([[Var(.8), Var(.2)], [Var(.2), Var(.8)]])
    y = np.array([[Var(1), Var(0)], [Var(0), Var(1)]])

    print(-np.sum(np.log(p) * y))

    def ce(p, y):
        print(p)
        print(np.log(p))
        return -np.sum(np.log(p) * y)

    print(ce(p, y))

    """
    activation = np.vectorize(lambda x:x.relu())

    x = np.array([[Var(5), Var(3)], [Var(2), Var(2)]])
    y = np.array([Var(2), Var(2)])

    print(activation(x @ y + Var(1)))
    """
