from shapes import (
    RectangleShape,
    EllipseShape,
    SquareShape,
    LineShape,
    PolygonWithLines,
)
from view import DragGraphicsView

import sys
import json
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsItem,
    QToolBar,
    QAction,
    QColorDialog,
    QFileDialog,
    QInputDialog,
    QGraphicsPolygonItem,
)
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF


class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drawing App")
        self.resize(800, 600)
        self.scene = QGraphicsScene()
        self.view = DragGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.items = []
        self.initUI()

    def initUI(self):
        """Initialize the toolbar and UI actions."""
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        for label, handler in [
            ("Rectangle", self.addRectangle),
            ("Ellipse", self.addEllipse),
            ("Square", self.addSquare),
            ("Line", self.addLine),
            ("Polygon", self.addPolygon),
            ("Group", self.groupSelected),
            ("Ungroup", self.ungroupSelected),
            ("Color", self.changeColorSelected),
            ("Rotate Left", lambda: self.rotateSelected(-15)),
            ("Rotate Right", lambda: self.rotateSelected(15)),
            ("Scale", self.scaleSelected),
            ("Clear All", self.clearAll),
            ("Clear Selected", self.clearSelected),
            ("Save", self.saveToFile),
            ("Load", self.loadFromFile),
        ]:
            action = QAction(label, self)
            action.triggered.connect(handler)
            toolbar.addAction(action)

    def addShape(self, shape):
        """Add a shape to the scene with graphics and interaction."""
        if isinstance(shape, RectangleShape):
            item = QGraphicsRectItem(shape.x, shape.y, shape.width, shape.height)
        elif isinstance(shape, EllipseShape):
            item = QGraphicsEllipseItem(shape.x, shape.y, shape.width, shape.height)
        elif isinstance(shape, SquareShape):
            item = QGraphicsRectItem(shape.x, shape.y, shape.width, shape.width)
        elif isinstance(shape, LineShape):
            item = QGraphicsLineItem(shape.x, shape.y, shape.x2, shape.y2)
        elif isinstance(shape, PolygonWithLines):
            item = self.createPolygonItem(
                shape
            )  # Use PolygonWithLines for the polygon + lines
        else:
            return
        item.shape = shape
        item.setTransformOriginPoint(item.boundingRect().center())
        item.setFlags(
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
        )
        if isinstance(item, QGraphicsLineItem):
            item.setPen(QPen(QColor(*shape.fill_color), shape.stroke_width))
        else:
            item.setBrush(QBrush(QColor(*shape.fill_color)))
            item.setPen(QPen(QColor(*shape.border_color), shape.stroke_width))
        self.scene.addItem(item)
        self.items.append(item)

    def addPolygon(self):
        # Define the vertices of the polygon
        vertices = [(100, 0), (-100, 0), (-40, -40), (70, -40)]

        # Define the lines as pairs of start and end points
        line_vertices = [
            # [(-40, -40), (100, 0)],
            # [(0, 0), (200, 300)]
        ]

        # Create the polygon with lines, passing group_id if needed
        polygon_item = PolygonWithLines(
            vertices,
            line_vertices,
            fill=(173, 216, 230),
            border_color=(0, 0, 255),
            group_id="group1",
        )

        # Add the polygon and lines to the scene
        polygon_item.add_to_scene(self.scene)

        # Update the second line
        polygon_item.set_line(1, (-100, 20), (50, 50))

    def addRectangle(self):
        self.addShape(RectangleShape(50, 50, 100, 60))

    def addEllipse(self):
        self.addShape(EllipseShape(60, 60, 100, 60))

    def addSquare(self):
        self.addShape(SquareShape(70, 70, 80))

    def addLine(self):
        self.addShape(LineShape(100, 100, 200, 200))

    def clearAll(self):
        """Remove all items from the scene."""
        for item in self.items:
            self.scene.removeItem(item)
        self.items.clear()

    def clearSelected(self):
        """Remove only the selected shapes from the scene."""
        for item in self.scene.selectedItems():
            if item in self.items:
                self.scene.removeItem(item)
                self.items.remove(item)

    def groupSelected(self):
        """Assign a group ID to selected shapes."""
        group_id = id(self) + len(
            self.scene.selectedItems()
        )  # Create a unique group ID

        for item in self.scene.selectedItems():
            if hasattr(item, "shape") and item.shape is not None:
                shape = item.shape
                if hasattr(
                    shape, "group_id"
                ):  # Ensure the shape has a group_id attribute
                    shape.group_id = group_id

    def ungroupSelected(self):
        """Remove group ID from selected shapes."""
        for item in self.scene.selectedItems():
            if hasattr(item, "shape") and item.shape is not None:
                shape = item.shape
                if hasattr(
                    shape, "group_id"
                ):  # Ensure the shape has a group_id attribute
                    shape.group_id = None

    def changeColorSelected(self):
        """Change the color of selected shapes (or their groups)."""
        color = QColorDialog.getColor()
        if not color.isValid():
            return

        selected = self.scene.selectedItems()

        # Get the group_ids of all selected items
        group_ids = {
            item.shape.group_id for item in selected if item.shape.group_id is not None
        }

        for item in self.items:
            # If the item is selected directly (and not in a group), or it shares a group ID with a selected item
            if (
                item in selected and item.shape.group_id is None
            ) or item.shape.group_id in group_ids:
                if isinstance(item, QGraphicsLineItem):
                    item.setPen(QPen(color, item.pen().width()))
                else:
                    item.setBrush(QBrush(color))
                item.shape.fill_color = (color.red(), color.green(), color.blue())

    def rotateSelected(self, angle):
        """Rotate selected shapes (or their group) by a given angle."""
        rotated = set()
        for item in self.scene.selectedItems():
            gid = getattr(item.shape, "group_id", None)
            if gid and gid not in rotated:
                for obj in self.items:
                    if getattr(obj.shape, "group_id", None) == gid:
                        obj.setRotation(obj.rotation() + angle)
                rotated.add(gid)
            elif not gid:
                item.setRotation(item.rotation() + angle)

    def scaleSelected(self):
        """Apply scaling to selected shapes (or their group)."""
        factor, ok = QInputDialog.getDouble(
            self, "Scale Selected", "Enter scale factor:", 1.0, 0.1, 10.0, 2
        )
        if not ok:
            return
        scaled_groups = set()
        for item in self.scene.selectedItems():
            gid = getattr(item.shape, "group_id", None)
            if gid and gid not in scaled_groups:
                for obj in self.items:
                    if getattr(obj.shape, "group_id", None) == gid:
                        self._applyScale(obj, factor)
                scaled_groups.add(gid)
            elif not gid:
                self._applyScale(item, factor)

    def _applyScale(self, item, factor):
        """Resize the item's dimensions by a given scale factor."""
        if isinstance(item, QGraphicsLineItem):
            # Scale a line item
            line = item.line()
            center = line.pointAt(0.5)
            new_p1 = center + (line.p1() - center) * factor
            new_p2 = center + (line.p2() - center) * factor
            item.setLine(new_p1.x(), new_p1.y(), new_p2.x(), new_p2.y())
        elif isinstance(item, QGraphicsPolygonItem):
            # Scale a polygon item
            polygon = item.polygon()
            center = polygon.boundingRect().center()

            # Scale each vertex of the polygon
            new_points = []
            for point in polygon:
                new_x = center.x() + (point.x() - center.x()) * factor
                new_y = center.y() + (point.y() - center.y()) * factor
                new_points.append(QPointF(new_x, new_y))

            item.setPolygon(QPolygonF(new_points))  # Set the new scaled polygon
        else:
            # For other shapes
            rect = item.rect()
            center = rect.center()
            new_width = rect.width() * factor
            new_height = rect.height() * factor
            new_rect = QRectF(
                center.x() - new_width / 2,
                center.y() - new_height / 2,
                new_width,
                new_height,
            )
            item.setRect(new_rect)
            item.setTransformOriginPoint(new_rect.center())

    def saveToFile(self):
        """Save all shape data to a JSON file."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "JSON Files (*.json)"
        )
        if not filename:
            return

        data = []
        for item in self.items:
            shape = item.shape

            # Gather the shape's transformation and state
            entry = {
                "type": type(shape).__name__,
                "x": item.pos().x(),
                "y": item.pos().y(),
                "rotation": item.rotation(),  # Rotation angle
                "scale_x": item.scale(),  # Scale (uniform scaling, assumes same scale for both axes)
                "fill_color": shape.fill_color,
                "border_color": shape.border_color,
                "group_id": shape.group_id if shape.group_id else None,
            }

            # Add shape-specific attributes
            if isinstance(shape, RectangleShape):
                entry["width"] = shape.width
                entry["height"] = shape.height
            elif isinstance(shape, EllipseShape):
                entry["width"] = shape.width
                entry["height"] = shape.height
            elif isinstance(shape, SquareShape):
                entry["width"] = shape.width  # Just the side of the square
            elif isinstance(shape, LineShape):
                entry["x2"] = shape.x2
                entry["y2"] = shape.y2
            elif isinstance(shape, PolygonShape):
                # Restore the polygon with the scaled vertices
                polygon = item.polygon()
                center = polygon.boundingRect().center()
                scaled_vertices = []
                for point in polygon:
                    new_x = center.x() + (point.x() - center.x()) * item.scale()
                    new_y = center.y() + (point.y() - center.y()) * item.scale()
                    scaled_vertices.append((new_x, new_y))
                entry["vertices"] = scaled_vertices  # Save the scaled vertices

            data.append(entry)

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    def loadFromFile(self):
        """Load shape data from a JSON file and add it to the scene."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "JSON Files (*.json)"
        )
        if not filename:
            return

        with open(filename, "r") as f:
            data = json.load(f)

        for entry in data:
            shape_type = entry["type"]
            fill_color = tuple(entry["fill_color"])  # Convert to tuple
            border_color = tuple(entry["border_color"])  # Convert to tuple

            # Create the shape based on the type
            shape = None
            if shape_type == "RectangleShape":
                shape = RectangleShape(
                    entry["x"], entry["y"], entry["width"], entry["height"], fill_color
                )
            elif shape_type == "EllipseShape":
                shape = EllipseShape(
                    entry["x"], entry["y"], entry["width"], entry["height"], fill_color
                )
            elif shape_type == "PolygonShape":
                # Restore the polygon with the scaled vertices
                scaled_vertices = entry["vertices"]
                shape = PolygonShape(scaled_vertices, fill_color)
            elif shape_type == "SquareShape":
                shape = SquareShape(entry["x"], entry["y"], entry["width"], fill_color)
            elif shape_type == "LineShape":
                shape = LineShape(
                    entry["x"], entry["y"], entry["x2"], entry["y2"], fill_color
                )

            if shape:
                shape.group_id = entry.get("group_id")  # Restore the group ID

                # Add shape to the scene
                self.addShape(shape)

                # Set the position of the shape as per the saved data
                shape_item = self.scene.items()[-1]  # Get the last item added
                shape_item.setPos(entry["x"], entry["y"])  # Set the position

                # Apply rotation and scale
                shape_item.setRotation(entry["rotation"])  # Set rotation
                shape_item.setScale(
                    entry["scale_x"]
                )  # Apply uniform scale (for non-uniform scaling, we need to tweak)

                # Apply colors based on the shape type
                if isinstance(shape_item, QGraphicsLineItem):
                    # For lines, use setPen to apply the color
                    shape_item.setPen(QPen(QColor(*border_color)))  # Set border color
                    shape_item.setPen(
                        QPen(QColor(*fill_color))
                    )  # Set the fill color for the line (if applicable)
                else:
                    # For other shapes, use setBrush for the fill color
                    shape_item.setBrush(QBrush(QColor(*fill_color)))  # Set fill color
                    shape_item.setPen(QPen(QColor(*border_color)))  # Set border color


def main():
    """Entry point: Launch the drawing application."""
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
