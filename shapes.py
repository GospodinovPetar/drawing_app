from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen, QColor, QPolygonF, QBrush
from PyQt5.QtWidgets import (
    QGraphicsPolygonItem,
    QGraphicsLineItem,
    QGraphicsItemGroup,
    QGraphicsScene,
    QGraphicsItem,
)


class ShapeBase:
    """
    Base class for all shapes.

    Contains shared attributes like selection state and group ID.
    """

    def __init__(self):
        self.selected = False
        self.group_id = None


import math
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItemGroup
from PyQt5.QtGui import QPen, QColor, QBrush


class PolygonWithLines(QGraphicsItemGroup):
    def __init__(self, center, radius, line_vertices=None, fill=(255, 255, 255), border_color=(0, 0, 0), stroke_width=2, group_id=None):
        super().__init__()

        self.group_id = group_id  # Assign group_id to the polygon item

        # Create the circle by replacing the polygon with an ellipse
        self.circle_item = QGraphicsEllipseItem(-radius, -radius, 2*radius, 2*radius)  # Define the bounding box of the circle
        self.circle_item.setPen(QPen(QColor(*border_color), stroke_width))
        self.circle_item.setBrush(QBrush(QColor(*fill)))

        # Add the circle item to the group
        self.addToGroup(self.circle_item)

        self.lines = []  # List to store line items
        if line_vertices:
            for line in line_vertices:
                # Constrain the line to fit inside the circle
                constrained_line = self.constrain_line_to_circle(line, radius)
                line_item = QGraphicsLineItem(constrained_line[0], constrained_line[1], constrained_line[2], constrained_line[3])
                line_item.setPen(QPen(QColor(0, 0, 0)))  # Set line color (black by default)
                self.addToGroup(line_item)
                self.lines.append(line_item)
                line_item.shape = self  # Associate the line with this group

        # Enable interaction for the group (selection and movement)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)

    def set_line(self, line_index, start_point, end_point):
        """Method to set the start and end point of a specific line."""
        if 0 <= line_index < len(self.lines):
            line_item = self.lines[line_index]
            line_item.setLine(start_point[0], start_point[1], end_point[0], end_point[1])

    def add_to_scene(self, scene):
        """Method to add the group to the scene."""
        scene.addItem(self)

    def clear(self):
        """Method to remove both the circle and its lines from the scene."""
        self.scene().removeItem(self.circle_item)  # Remove the circle
        for line_item in self.lines:
            self.scene().removeItem(line_item)  # Remove each line
        self.scene().removeItem(self)  # Remove the entire group itself

    def constrain_line_to_circle(self, line, radius):
        """Constrain line to be inside the circle."""
        # Unpack the two points that define the line
        (x1, y1), (x2, y2) = line  # line is now a list of tuples (start_point, end_point)
        center_x, center_y = 0, 0  # Assuming the circle's center is at (0, 0)

        # Calculate the distance from the center to the line endpoints
        dist1 = math.sqrt((x1 - center_x) ** 2 + (y1 - center_y) ** 2)
        dist2 = math.sqrt((x2 - center_x) ** 2 + (y2 - center_y) ** 2)

        # Scale the endpoints to fit inside the circle
        if dist1 > radius:
            scale_factor = radius / dist1
            x1 = center_x + (x1 - center_x) * scale_factor
            y1 = center_y + (y1 - center_y) * scale_factor

        if dist2 > radius:
            scale_factor = radius / dist2
            x2 = center_x + (x2 - center_x) * scale_factor
            y2 = center_y + (y2 - center_y) * scale_factor

        return (x1, y1, x2, y2)

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
