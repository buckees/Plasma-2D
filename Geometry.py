"""
Geometry module.

Geometry module defines the basic shapes, such as 
1D: Interval 
2D: Rectangle, Triangle, etc.

Geometry module defines the construction of the geometry.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patch

class Domain:
    """Define the Domian."""
    
    def __init__(self, name='Demo'):
        """
        Init the Domain.
        
        name: str, var, name of domain.
        """
        self.name = name

    def __str__(self):
        """Print Domain info."""
        return f'label = {self.name}'

class Shape(Domain):
    """Init the Shape."""
    
    def __init__(self, label):
        """
        Init the Shape.
        
        label: str, var, label of shape.
        """
        self.label = label

    def __str__(self):
        """Print Shape info."""
        return f'label = {self.label}'


class Interval(Shape):
    """Interval is a 1D basic shape."""
    
    def __init__(self, begin, end, axis=0):
        """
        Init the Interval.
        
        begin: unit in m, var
        end: unit in m, var
        axis: ???
        """
        self.begin = begin
        self.end = end
        self.axis = axis
        self.type = 'Interval'

    def __str__(self):
        """Print Interval info."""
        res = 'Interval:'
        res += f'\nbegin = {self.begin} m'
        res += f'\nend = {self.end} m'
        res += f'\naxis = {self.axis}'
        return res

    def __contains__(self, posn):
        """
        Determind if a position is inside the Interval.
        
        posn: unit in m, var, position as input
        boundaries are not consindered as "Inside"
        """
        return self.begin < posn[self.axis] < self.end
    
    def boundary(self):
        """Return the boundary."""
        pass

class Rectangle(Shape):
    """Rectangle is a 2D basic shape."""
    
    def __init__(self, bottom_left, up_right):
        """
        Init the Rectangle.
        
        bottom_left: unit in m, (2, ) array
        up_right: unit in m, (2, ) array
        """
        self.bl = bottom_left
        self.ur = up_right
        self.width = self.ur[0] - self.bl[0]
        self.height = self.ur[1] - self.bl[1]
        self.type = 'Rectangle'

    def __str__(self):
        """Print Rectangle info."""
        res = 'Rectangle:'
        res += f'\nbottom left = {self.bl} m'
        res += f'\nup right = {self.ur} m'
        return res

    def __contains__(self, posn):
        """
        Determind if a position is inside the Interval.
        
        posn: unit in m, (2, ) array, position as input
        boundaries are not consindered as "Inside"
        """
        return all(self.bl < posn < self.ur)


class Geometry:
    """Constuct the geometry."""
    
    def __init__(self, dim=2, is_cyl=False):
        """
        Init the geometry.
        
        dim: dimless, int, must be in [1, 2, 3], 1:1D; 2:2D; 3:3D
        is_cyl: bool, wether the geometry is cylidrical symmetric or not
        """
        self.dim = dim
        self.is_cyl = is_cyl
        self.sequence = list()

    def __str__(self):
        """Print Geometry info."""
        res = f'Geometry dimension {self.dim}D'
        if self.is_cyl:
            res += ' cylindrical'
        res += '\nGeometry sequence:'
        for shape in self.sequence:
            res += '\n' + str(shape)
        return res

    def add_shape(self, shape):
        """
        Add shape to the geometry.
        
        shape: class
        1D - shape is an instance of Interval()
        2D - shape is an instance of Rectangle()
        """
        self.sequence.append(shape)

    def get_label(self, posn):
        """
        Return the label of a position.
        
        posn: unit in m, var or (2, ) array, position as input
        label: str, var, label of the shape
        """
        # what if return None
        label = None
        for shape in self.sequence:
            if posn in shape:
                label = shape.label
        return label

    def label_check(self, posn, label):
        """
        Check if labelf of posn == label of input.
        
        posn: unit in m, var or (2, ) array, position as input
        label: str, var, label as input
        """
        # cannot determined if the posn is in domain
        res = False
        posn_label = self.get_label(posn)
        return res or (posn_label == label)
    
    def plot(self, figsize=(8, 8), dpi=300):
        """
        Plot the geometry.
        
        figsize: unit in inch, (2, ) tuple, determine the fig/canvas size
        dpi: dimless, int, Dots Per Inch
        """
        fig, axes = plt.subplots(1, 2, figsize=figsize, dpi=dpi,
                         constrained_layout=True)
        ax = axes[0]
        for shape in self.sequence:
            if shape.type == 'Rectangle':
                ax.add_patch(
                    patch.Rectangle(shape.bl, shape.width, shape.height,
                                    edgecolor='k'))
        plt.show()
                
if __name__ == '__main__':
    import numpy as np
    icp2d = Geometry(dim=2, is_cyl=False)
    plasma = Rectangle(np.array([0.0, 0.0]), np.array([1.0, 2.0]))
    icp2d.add_shape(plasma)
    top = Rectangle(np.array([0.0, 1.9]), np.array([1.0, 2.0]))
    icp2d.add_shape(top)
    bott = Rectangle(np.array([0.0, 0.0]), np.array([1.0, 0.1]))
    icp2d.add_shape(bott)
    wall = Rectangle(np.array([0.9, 0.0]), np.array([0.0, 2.0]))
    icp2d.add_shape(wall)
    icp2d.plot()