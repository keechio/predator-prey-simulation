import math

class Vector:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def set(self, x, y):
        """Set the two coordinates in self.
        
        Parameters:
            self: a Vector object
            x: a number representing a new first coordinate for self
            y: a number representing a new second coordinate for self
            
        Return value: None
        """
        
        self._x = x
        self._y = y

    def __add__(self, secondVector):
        return Vector(self._x + secondVector._x, self._y + secondVector._y)

    def __truediv__(self, scalar):
        return Vector((self._x / scalar), (self._y / scalar))

    def magnitude(self):
        """
        using the distance equation, it finds the distance between 0,0 and the
        vector's x and y value
        """
        return math.sqrt((self._x ** 2) + (self._y ** 2))

    def scale(self, scalar):
        """Multiply the coordinates in self by a scalar value.
        
        Parameters:
            self: a Vector object
            scalar: a number by which to scale the coordinates in self
                        
        Return value: None
        """
        
        self.set(self._x * scalar, self._y * scalar)
        
    def unitScale(self):
        """
        using the truediv and magnitude method, it divides the x and y value
        of the method by the magnitude which returns the x and y coordinates
        of the vector if the magnitude was only 1
        """
        mag = self.magnitude()
        if mag > 0:
            return (self / self.magnitude())
        return self

    def __str__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ')'
        


    
