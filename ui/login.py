from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor
from models.base import get_session
from models.user import User
import ui.resources_rc

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.engine = parent.engine
        self.init_ui()

    def init_ui(self):
        # Set window background
        self.setStyleSheet("QWidget { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f8f9fd, stop:1 #ffffff); }")
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create centered container
        container = QFrame()
        container.setObjectName("login-container")
        container.setFixedWidth(400)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout()
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container.setLayout(container_layout)

        # Add logo
        logo = QLabel()
        logo.setPixmap(QIcon(":/icons/logo.svg").pixmap(QSize(48, 48)))
        logo.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(logo)

        # Add title
        title = QLabel("Ladex")
        title.setObjectName("login-title")
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        # Add welcome message
        welcome = QLabel("Welcome back!")
        welcome.setObjectName("login-subtitle")
        welcome.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(welcome)

        subtitle = QLabel("Please sign in to continue")
        subtitle.setObjectName("login-text")
        subtitle.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(subtitle)

        # Add some spacing
        container_layout.addSpacing(20)

        # Username input with icon
        username_container = QFrame()
        username_layout = QHBoxLayout()
        username_layout.setContentsMargins(0, 0, 0, 0)
        username_container.setLayout(username_layout)

        username_icon = QLabel()
        username_icon.setPixmap(QIcon(":/icons/user.svg").pixmap(QSize(20, 20)))
        username_layout.addWidget(username_icon)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(48)
        username_layout.addWidget(self.username_input)

        container_layout.addWidget(username_container)

        # Password input with icon
        password_container = QFrame()
        password_layout = QHBoxLayout()
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_container.setLayout(password_layout)

        password_icon = QLabel()
        password_icon.setPixmap(QIcon(":/icons/lock.svg").pixmap(QSize(20, 20)))
        password_layout.addWidget(password_icon)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(48)
        password_layout.addWidget(self.password_input)

        container_layout.addWidget(password_container)

        # Add some spacing
        container_layout.addSpacing(20)

        # Login button
        login_btn = QPushButton("Sign In")
        login_btn.setObjectName("login-button")
        login_btn.setMinimumHeight(48)
        login_btn.clicked.connect(self.handle_login)
        container_layout.addWidget(login_btn)

        # Center the container
        main_layout.addStretch()
        main_layout.addWidget(container, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        session = get_session(self.engine)
        user = session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            self.parent.show_main(user)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

        session.close()
