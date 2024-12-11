from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidget, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

class BaseTableView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.engine = parent.engine

    def setup_table(self, table):
        """Configure table widget with consistent styling"""
        # Set selection behavior
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # Set column resize modes
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStretchLastSection(False)
        
        # Set row height
        table.verticalHeader().setDefaultSectionSize(48)
        table.verticalHeader().setVisible(False)
        
        # Enable sorting
        table.setSortingEnabled(True)
        
        # Set alternating row colors
        table.setAlternatingRowColors(True)
        
        return table

    def create_action_button(self, icon_path, text, action_type="true"):
        """Create a consistently styled action button"""
        button = QPushButton()
        button.setProperty("action", action_type)
        
        # Set icon if provided
        if icon_path:
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(16, 16))
        
        # Set text if provided
        if text:
            button.setText(text)
        
        # Set fixed size for consistent button dimensions
        button.setFixedSize(QSize(100, 36))
        
        return button

    def create_action_layout(self, edit_callback=None, delete_callback=None):
        """Create a layout with edit and delete buttons"""
        layout = QHBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(4, 4, 4, 4)
        
        if edit_callback:
            edit_btn = self.create_action_button(":/icons/edit.svg", "Edit")
            edit_btn.clicked.connect(edit_callback)
            layout.addWidget(edit_btn)
        
        if delete_callback:
            delete_btn = self.create_action_button(":/icons/delete.svg", "Delete", "delete")
            delete_btn.clicked.connect(delete_callback)
            layout.addWidget(delete_btn)
        
        layout.addStretch()
        return layout
