class ShapeBase:
    """
    Base class for all shapes.

    Contains shared attributes like selection state and group ID.
    """

    def __init__(self):
        self.selected = False
        self.group_id = None


class RectangleShape(ShapeBase):
    """
    A rectangle shape with position, dimensions, and style attributes.
    """

    def __init__(self, x, y, w, h, fill=(255, 255, 255)):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.width = float(w)
        self.height = float(h)
        self.fill_color = fill
        self.border_color = (255, 255, 255)
        self.stroke_width = 2
        self.alpha = 255


class EllipseShape(ShapeBase):
    """
    An ellipse shape defined by bounding box dimensions and styling.
    """

    def __init__(self, x, y, w, h, fill=(255, 255, 255)):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.width = float(w)
        self.height = float(h)
        self.fill_color = fill
        self.border_color = (255, 255, 255)
        self.stroke_width = 2
        self.alpha = 255


class SquareShape(RectangleShape):
    """
    A square shape that inherits from RectangleShape,
    but ensures equal width and height.
    """

    def __init__(self, x, y, size, fill=(255, 255, 255)):
        super().__init__(x, y, size, size, fill)


class LineShape(ShapeBase):
    """
    A line defined by two endpoints and color/stroke settings.
    """

    def __init__(self, x1, y1, x2, y2, fill=(255, 255, 255)):
        super().__init__()
        self.x = float(x1)
        self.y = float(y1)
        self.x2 = float(x2)
        self.y2 = float(y2)
        self.fill_color = fill
        self.border_color = (255, 255, 255)
        self.stroke_width = 2
        self.alpha = 255
