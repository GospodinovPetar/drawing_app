from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem
from PyQt5.QtGui import QPainter


class DragGraphicsView(QGraphicsView):
    """
    A QGraphicsView that supports dragging groups of items together.
    """

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self._drag_group_id = None
        self._drag_start_positions = {}
        self._drag_origin = None

    def mousePressEvent(self, event):
        """Record initial drag positions and determine group ID."""
        self._drag_start_positions.clear()
        self._drag_origin = self.mapToScene(event.pos())
        for item in self.scene().items():
            if hasattr(item, "shape"):  # Ensure the item has a shape attribute
                self._drag_start_positions[item] = item.pos()

        clicked_item = self.itemAt(event.pos())
        if clicked_item and hasattr(clicked_item, "shape"):
            shape = clicked_item.shape
            if hasattr(shape, "group_id"):  # Check if group_id exists
                self._drag_group_id = shape.group_id

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Apply movement to grouped items in real-time."""
        if not self._drag_origin:
            return
        current_pos = self.mapToScene(event.pos())
        delta = current_pos - self._drag_origin
        if self._drag_group_id is not None:
            for item, start_pos in self._drag_start_positions.items():
                if (
                    hasattr(item, "shape")
                    and item.shape.group_id == self._drag_group_id
                ):
                    item.setPos(start_pos + delta)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Clear internal drag state after releasing the mouse."""
        self._drag_group_id = None
        self._drag_start_positions.clear()
        self._drag_origin = None
        super().mouseReleaseEvent(event)
