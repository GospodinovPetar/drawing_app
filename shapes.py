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


class PolygonWithLines(QGraphicsItemGroup):
    def __init__(
        self,
        vertices,
        line_vertices=None,
        fill=(255, 255, 255),
        border_color=(0, 0, 0),
        stroke_width=2,
        group_id=None,
    ):
        super().__init__()

        self.group_id = group_id  # Assign group_id to the polygon item

        # Create the polygon from the vertices
        self.polygon_item = QGraphicsPolygonItem(
            QPolygonF([QPointF(x, y) for x, y in vertices])
        )
        self.polygon_item.setPen(QPen(QColor(*border_color), stroke_width))
        self.polygon_item.setBrush(QBrush(QColor(*fill)))

        # Add the polygon item to the group
        self.addToGroup(self.polygon_item)

        # Create and add lines if provided
        self.lines = []  # List to store line items
        if line_vertices:
            for line in line_vertices:
                line_item = QGraphicsLineItem(
                    line[0][0], line[0][1], line[1][0], line[1][1]
                )
                line_item.setPen(
                    QPen(QColor(0, 0, 0))
                )  # Set line color (black by default)
                self.addToGroup(line_item)
                self.lines.append(line_item)
                line_item.shape = self  # Associate the line with this group

        # Enable interaction for the group (selection and movement)
        self.setFlags(
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
        )

    def set_line(self, line_index, start_point, end_point):
        """Method to set the start and end point of a specific line."""
        if 0 <= line_index < len(self.lines):
            line_item = self.lines[line_index]
            line_item.setLine(
                start_point[0], start_point[1], end_point[0], end_point[1]
            )

    def add_to_scene(self, scene):
        """Method to add the group to the scene."""
        scene.addItem(self)


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
