class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector2d(new_x, new_y)
    
    def __mul__(self, k):
        new_x = self.x * k
        new_y = self.y * k
        return Vector2d(new_x, new_y)
    
    def __pow__(self, k):
        new_x = self.x ** k
        new_y = self.y ** k
        return Vector2d(new_x, new_y)
    
    def __neg__(self): # -self
        return self * -1
    
    def __radd__(self, other): # other + self
        return self + other

    def __sub__(self, other): # self - other
        return self + (-other)

    def __rsub__(self, other): # other - self
        return other + (-self)

    def __rmul__(self, other): # other * self
        return self * other
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def modulo(self):
        return (self.x**2 + self.y**2)**(1/2)
    
    @property
    def val(self):
        return self.x, self.y
     

