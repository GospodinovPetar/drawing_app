# Drawing Application (PyQt5)

This is a simple graphical drawing application built with **PyQt5**. The app allows users to create basic shapes like rectangles, ellipses, squares, lines and manipulate them by selecting, moving, rotating, resizing, and grouping. Additionally, users can save and load their drawings in a JSON format.

## Features

### 1. **Create Shapes**
   - The user can create the following shapes:
     - **Rectangle**: A basic rectangular shape.
     - **Ellipse**: An ellipse or circle shape.
     - **Square**: A square, which is a special case of the rectangle with equal width and height.
     - **Line**: A simple line connecting two points.

   - **How to create shapes**:
     - Use the toolbar at the top to select the type of shape you want to draw.
     - After you click on the shape it appears on the canvas.

### 2. **Select Shapes**
   - You can select a single shape by clicking on it.
   - **Selecting Multiple Shapes**: To select multiple shapes, simply click and drag with the mouse. Any shapes that fall within the selection area will be selected.
   - Once shapes are selected, you can perform various operations on them like moving, rotating, and changing their colors.

### 3. **Move Shapes**
   - **Single shape movement**: Click and drag any shape to move it around the canvas.
   - **Multiple shapes movement**: If multiple shapes are selected or are in a group, click and drag any of the shapes. All shapes in the selection or in the group will move/rotate/scale together.

### 4. **Group and Ungroup Shapes**
   - **Group**: After selecting multiple shapes, click the "Group" button to group them together. Once grouped, transformations (move, rotate, scale) will be applied to all shapes in the group simultaneously.
   - **Ungroup**: Click the "Ungroup" button to separate the shapes in the group, allowing them to be manipulated independently again.

### 5. **Rotate Shapes**
   - You can rotate shapes by 15 degrees (either left or right) using the "Rotate Left" or "Rotate Right" buttons.
   - If multiple shapes are selected or grouped, all selected shapes will rotate simultaneously.

### 6. **Scale Shapes**
   - **Scale selected shapes**: You can scale the size of selected shapes by a factor. A dialog will appear where you can enter the scaling factor (e.g., 1.0 for no scaling, 2.0 for double the size, etc.).
   - **Scaling for grouped shapes**: If multiple shapes are grouped, scaling will apply to all shapes in the group.

### 7. **Change Color**
   - You can change the color of the selected shapes. Clicking the "Color" button opens a color dialog, allowing you to pick a new color for the selected shapes.
   - The color change will be applied to all selected shapes. If they are grouped, the entire group will change color at once.

### 8. **Delete Shapes**
   - **Delete selected shapes**: Press the "Clear Selected" button to remove the selected shapes from the canvas.
   - **Delete all shapes**: Press the "Clear All" button to clear the entire canvas.

### 9. **Save and Load Drawings**
   - **Save**: You can save the current drawing to a JSON file by clicking the "Save" button. This saves all the shapes, their positions, sizes, and other properties.
   - **Load**: To load a previously saved drawing, click the "Load" button. The shapes will be reloaded onto the canvas.

### 10. **Interactive Canvas**
   - The application provides a real-time drawing experience with all shapes being immediately displayed as you interact with the app.

---

## How to Use

1. **Start the App**: 
   - Run the Python script to launch the application. A window will appear where you can draw and manipulate shapes.

2. **Creating Shapes**: 
   - Select a shape type from the toolbar at the top (e.g., Rectangle, Ellipse, Line, etc.), and it will appear on the canvas.

3. **Selecting Multiple Shapes**: 
   - Click and drag to create a selection box. Any shapes inside the selection box will be selected.

4. **Manipulating Shapes**: 
   - After selecting shapes, you can move them around, rotate them, change their color, or group them for collective transformations.

5. **Saving and Loading**: 
   - Use the "Save" button to save your current work, and "Load" to load a previously saved drawing.

---

## Code Structure

- **`shapes.py`**: Contains the shape classes (e.g., `RectangleShape`, `EllipseShape`, `CircleWithDiagonalLine`, etc.).
- **`view.py`**: Contains the custom view for the canvas, including mouse event handling, shape drawing, and interaction logic.
- **`app.py`**: The main application logic, including the user interface, toolbar, and functionality for manipulating shapes.

---

## How to Install

1. **Install Dependencies**:
   To install the required Python packages, use the following command:

   ```bash
   pip install -r requirements.txt
