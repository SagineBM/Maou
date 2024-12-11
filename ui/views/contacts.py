from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem, QDialog,
                             QFormLayout, QLineEdit, QTextEdit, QHeaderView,
                             QSizePolicy)
from PyQt5.QtCore import Qt
from models.base import get_session
from models.contact import Contact

class ContactDialog(QDialog):
    def __init__(self, parent=None, contact=None):
        super().__init__(parent)
        self.contact = contact
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Contact" if not self.contact else "Edit Contact")
        layout = QFormLayout()

        # Create input fields
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.company = QLineEdit()
        self.position = QLineEdit()
        self.address = QTextEdit()
        self.notes = QTextEdit()

        # Add fields to layout
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Email:", self.email)
        layout.addRow("Phone:", self.phone)
        layout.addRow("Company:", self.company)
        layout.addRow("Position:", self.position)
        layout.addRow("Address:", self.address)
        layout.addRow("Notes:", self.notes)

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
        if self.contact:
            self.first_name.setText(self.contact.first_name)
            self.last_name.setText(self.contact.last_name)
            self.email.setText(self.contact.email)
            self.phone.setText(self.contact.phone)
            self.company.setText(self.contact.company)
            self.position.setText(self.contact.position)
            self.address.setText(self.contact.address)
            self.notes.setText(self.contact.notes)

class ContactsView(QWidget):
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
        header = QLabel("Contacts")
        header.setObjectName("page-header")
        header_layout.addWidget(header)

        add_btn = QPushButton("Add Contact")
        add_btn.setMaximumWidth(100)  # Limit button width
        add_btn.clicked.connect(self.add_contact)
        header_layout.addWidget(add_btn)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Contacts table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "First Name", "Last Name", "Email", "Phone", "Company",
            "Position", "Address", "Notes", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(False)  # Don't stretch last column
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.Fixed)  # Fix actions column width
        self.table.setColumnWidth(8, 100)  # Set actions column width
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Make table expand
        layout.addWidget(self.table)

        self.setLayout(layout)

    def update_view(self):
        if not self.parent.user:
            return

        session = get_session(self.engine)
        contacts = session.query(Contact).filter_by(owner_id=self.parent.user.id).all()

        self.table.setRowCount(len(contacts))
        for row, contact in enumerate(contacts):
            self.table.setItem(row, 0, QTableWidgetItem(contact.first_name))
            self.table.setItem(row, 1, QTableWidgetItem(contact.last_name))
            self.table.setItem(row, 2, QTableWidgetItem(contact.email))
            self.table.setItem(row, 3, QTableWidgetItem(contact.phone))
            self.table.setItem(row, 4, QTableWidgetItem(contact.company))
            self.table.setItem(row, 5, QTableWidgetItem(contact.position))
            self.table.setItem(row, 6, QTableWidgetItem(contact.address))
            self.table.setItem(row, 7, QTableWidgetItem(contact.notes))

            # Create action buttons with smaller size
            actions_layout = QHBoxLayout()
            actions_layout.setSpacing(2)
            actions_layout.setContentsMargins(2, 2, 2, 2)

            edit_btn = QPushButton("Edit")
            edit_btn.setMaximumWidth(12)
            edit_btn.setMaximumHeight(24)
            delete_btn = QPushButton("Del")
            delete_btn.setMaximumWidth(12)
            delete_btn.setMaximumHeight(24)

            edit_btn.clicked.connect(lambda checked, c=contact: self.edit_contact(c))
            delete_btn.clicked.connect(lambda checked, c=contact: self.delete_contact(c))

            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)

            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.table.setCellWidget(row, 8, actions_widget)

        session.close()

    def add_contact(self):
        dialog = ContactDialog(self)
        if dialog.exec_():
            session = get_session(self.engine)
            contact = Contact(
                first_name=dialog.first_name.text(),
                last_name=dialog.last_name.text(),
                email=dialog.email.text(),
                phone=dialog.phone.text(),
                company=dialog.company.text(),
                position=dialog.position.text(),
                address=dialog.address.toPlainText(),
                notes=dialog.notes.toPlainText(),
                owner_id=self.parent.user.id
            )
            session.add(contact)
            session.commit()
            session.close()
            self.update_view()

    def edit_contact(self, contact):
        dialog = ContactDialog(self, contact)
        if dialog.exec_():
            session = get_session(self.engine)
            contact = session.merge(contact)
            contact.first_name = dialog.first_name.text()
            contact.last_name = dialog.last_name.text()
            contact.email = dialog.email.text()
            contact.phone = dialog.phone.text()
            contact.company = dialog.company.text()
            contact.position = dialog.position.text()
            contact.address = dialog.address.toPlainText()
            contact.notes = dialog.notes.toPlainText()
            session.commit()
            session.close()
            self.update_view()

    def delete_contact(self, contact):
        session = get_session(self.engine)
        contact = session.merge(contact)
        session.delete(contact)
        session.commit()
        session.close()
        self.update_view()
