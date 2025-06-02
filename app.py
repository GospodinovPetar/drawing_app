from shapes import RectangleShape, EllipseShape, SquareShape, LineShape
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
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor


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
        group_id = id(self) + len(self.scene.selectedItems())
        for item in self.scene.selectedItems():
            item.shape.group_id = group_id

    def ungroupSelected(self):
        """Remove group ID from selected shapes."""
        for item in self.scene.selectedItems():
            item.shape.group_id = None

    def changeColorSelected(self):
        """Change the color of selected shapes (or their groups)."""
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        selected = self.scene.selectedItems()
        group_ids = {item.shape.group_id for item in selected}
        for item in self.items:
            if item.shape.group_id in group_ids or (
                item.shape.group_id is None and item in selected
            ):
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
            line = item.line()
            center = line.pointAt(0.5)
            new_p1 = center + (line.p1() - center) * factor
            new_p2 = center + (line.p2() - center) * factor
            item.setLine(new_p1.x(), new_p1.y(), new_p2.x(), new_p2.y())
        else:
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
            entry = {
                "type": type(shape).__name__,
                "x": shape.x,
                "y": shape.y,
                "group_id": shape.group_id,
                "fill_color": shape.fill_color,
            }
            if isinstance(shape, LineShape):
                entry["x2"] = shape.x2
                entry["y2"] = shape.y2
            else:
                entry["width"] = shape.width
                entry["height"] = shape.height
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
        offset_x, offset_y = 0, 0
        for entry in data:
            shape_type = entry["type"]
            fill = tuple(entry["fill_color"])
            if shape_type == "RectangleShape":
                shape = RectangleShape(
                    offset_x, offset_y, entry["width"], entry["height"], fill
                )
            elif shape_type == "EllipseShape":
                shape = EllipseShape(
                    offset_x, offset_y, entry["width"], entry["height"], fill
                )
            elif shape_type == "SquareShape":
                shape = SquareShape(offset_x, offset_y, entry["width"], fill)
            elif shape_type == "LineShape":
                shape = LineShape(offset_x, offset_y, offset_x, offset_y, fill)
            else:
                continue
            shape.group_id = entry.get("group_id")
            self.addShape(shape)


def main():
    """Entry point: Launch the drawing application."""
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
