import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem, QDialog,
                             QFormLayout, QLineEdit, QTextEdit, QComboBox,
                             QDateTimeEdit, QHeaderView, QSizePolicy)
from PyQt5.QtCore import Qt, QDateTime
from models.base import get_session
from models.task import Task, TaskStatus, TaskPriority
from models.contact import Contact

class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Task" if not self.task else "Edit Task")
        layout = QFormLayout()

        # Create input fields
        self.title = QLineEdit()
        self.description = QTextEdit()
        
        self.status = QComboBox()
        self.status.addItems([status.value for status in TaskStatus])
        
        self.priority = QComboBox()
        self.priority.addItems([priority.value for priority in TaskPriority])
        
        self.due_date = QDateTimeEdit(QDateTime.currentDateTime())
        self.due_date.setCalendarPopup(True)
        
        self.reminder_date = QDateTimeEdit(QDateTime.currentDateTime())
        self.reminder_date.setCalendarPopup(True)
        
        self.contact = QComboBox()
        self.load_contacts()

        # Add fields to layout
        layout.addRow("Title:", self.title)
        layout.addRow("Description:", self.description)
        layout.addRow("Status:", self.status)
        layout.addRow("Priority:", self.priority)
        layout.addRow("Due Date:", self.due_date)
        layout.addRow("Reminder:", self.reminder_date)
        layout.addRow("Contact:", self.contact)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow(button_box)

        self.setLayout(layout)

        # If editing, populate fields
        if self.task:
            self.title.setText(self.task.title)
            self.description.setText(self.task.description)
            self.status.setCurrentText(self.task.status.value)
            self.priority.setCurrentText(self.task.priority.value)
            if self.task.due_date:
                self.due_date.setDateTime(self.task.due_date)
            if self.task.reminder_date:
                self.reminder_date.setDateTime(self.task.reminder_date)
            if self.task.contact:
                self.contact.setCurrentText(self.task.contact.full_name)

    def load_contacts(self):
        session = get_session(self.parent.parent.engine)
        contacts = session.query(Contact).filter_by(
            owner_id=self.parent.parent.user.id
        ).all()
        
        self.contact.addItem("None", None)
        for contact in contacts:
            self.contact.addItem(contact.full_name, contact.id)
        
        session.close()

class TasksView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.engine = parent.engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header with title and add button
        header_layout = QHBoxLayout()
        header = QLabel("Tasks")
        header.setObjectName("page-header")
        header_layout.addWidget(header)

        add_btn = QPushButton("Add Task")
        add_btn.setMaximumWidth(100)  # Limit button width
        add_btn.clicked.connect(self.add_task)
        header_layout.addWidget(add_btn)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        
        # Tasks table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Title", "Status", "Priority", "Due Date", "Contact", "Reminder", "Actions"
        ])
        # Set section resize mode to Stretch for all columns
        for i in range(self.table.columnCount()):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        # Make table expand and adjust automatically
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setStretchLastSection(True)  # stretch last column

        # Ensure rows adjust to content
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.table)

        self.setLayout(layout)


    def update_view(self):
        if not self.parent.user:
            return

        session = get_session(self.engine)
        tasks = session.query(Task).filter_by(assigned_to_id=self.parent.user.id).all()

        self.table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, QTableWidgetItem(task.title))
            self.table.setItem(row, 1, QTableWidgetItem(task.status.value))
            self.table.setItem(row, 2, QTableWidgetItem(task.priority.value))
            self.table.setItem(row, 3, QTableWidgetItem(
                task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else ""
            ))
            self.table.setItem(row, 4, QTableWidgetItem(
                task.contact.full_name if task.contact else ""
            ))
            self.table.setItem(row, 5, QTableWidgetItem(
                task.reminder_date.strftime("%Y-%m-%d %H:%M") if task.reminder_date else ""
            ))

           # Create action buttons with dynamic size
            actions_layout = QHBoxLayout()
            actions_layout.setSpacing(2)
            actions_layout.setContentsMargins(2, 2, 2, 2)

            edit_btn = QPushButton("Edit")
            edit_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Make button expand
            edit_btn.setStyleSheet("min-height: 20px; max-height: 25px; min-width: 30px; max-width: 40px;")
            delete_btn = QPushButton("Del")
            delete_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Make button expand
            delete_btn.setStyleSheet("min-height: 20px; max-height: 25px; min-width: 30px; max-width: 40px;")

            edit_btn.clicked.connect(lambda checked, t=task: self.edit_task(t))
            delete_btn.clicked.connect(lambda checked, t=task: self.delete_task(t))

            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)

            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.table.setCellWidget(row, 6, actions_widget)


        session.close()

    def add_task(self):
        dialog = TaskDialog(self)
        if dialog.exec_():
            session = get_session(self.engine)
            task = Task(
                title=dialog.title.text(),
                description=dialog.description.toPlainText(),
                status=TaskStatus(dialog.status.currentText()),
                priority=TaskPriority(dialog.priority.currentText()),
                due_date=dialog.due_date.dateTime().toPyDateTime(),
                reminder_date=dialog.reminder_date.dateTime().toPyDateTime(),
                assigned_to_id=self.parent.user.id,
                contact_id=dialog.contact.currentData()
            )
            session.add(task)
            session.commit()
            session.close()
            self.update_view()

    def edit_task(self, task):
        dialog = TaskDialog(self, task)
        if dialog.exec_():
            session = get_session(self.engine)
            task = session.merge(task)
            task.title = dialog.title.text()
            task.description = dialog.description.toPlainText()
            task.status = TaskStatus(dialog.status.currentText())
            task.priority = TaskPriority(dialog.priority.currentText())
            task.due_date = dialog.due_date.dateTime().toPyDateTime()
            task.reminder_date = dialog.reminder_date.dateTime().toPyDateTime()
            task.contact_id = dialog.contact.currentData()
            session.commit()
            session.close()
            self.update_view()

    def delete_task(self, task):
        session = get_session(self.engine)
        task = session.merge(task)
        session.delete(task)
        session.commit()
        session.close()
        self.update_view()
