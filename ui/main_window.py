from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QStackedWidget, QLineEdit, QFrame,
                             QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from .views.contacts import ContactsView
from .views.tasks import TasksView
from .views.dashboard import DashboardView
from .views.chat import ChatView
import ui.resources_rc

class TopBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("top-bar")
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)

        # Search bar
        search_container = QFrame()
        search_container.setObjectName("search-container")
        search_layout = QHBoxLayout()
        search_container.setLayout(search_layout)

        search_icon = QLabel()
        search_icon.setPixmap(QIcon(":/icons/search.svg").pixmap(QSize(16, 16)))
        search_layout.addWidget(search_icon)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search...")
        search_input.setObjectName("search-input")
        search_layout.addWidget(search_input)

        layout.addWidget(search_container)

        # Subscription notice
        sub_notice = QLabel("Try Premium Features")
        sub_notice.setObjectName("sub-notice")
        layout.addWidget(sub_notice)

        subscribe_btn = QPushButton("Subscribe")
        subscribe_btn.setObjectName("subscribe-button")
        layout.addWidget(subscribe_btn)

        # User profile
        user_btn = QPushButton()
        user_btn.setIcon(QIcon(":/icons/user.svg"))
        user_btn.setIconSize(QSize(24, 24))
        user_btn.setObjectName("user-button")
        layout.addWidget(user_btn)

        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.user = None
        self.engine = parent.engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Top bar
        self.top_bar = TopBar(self)
        layout.addWidget(self.top_bar)

        # Main content area
        content = QHBoxLayout()
        content.setSpacing(0)

        # Side navigation
        nav = QFrame()
        nav.setObjectName("side-nav")
        nav_layout = QVBoxLayout()
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(10, 20, 10, 20)

        # Navigation buttons
        self.nav_buttons = []

        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.setIcon(QIcon(":/icons/dashboard.svg"))
        dashboard_btn.clicked.connect(lambda: self.show_view(0))
        nav_layout.addWidget(dashboard_btn)
        self.nav_buttons.append(dashboard_btn)

        contacts_btn = QPushButton("Contacts")
        contacts_btn.setIcon(QIcon(":/icons/contacts.svg"))
        contacts_btn.clicked.connect(lambda: self.show_view(1))
        nav_layout.addWidget(contacts_btn)
        self.nav_buttons.append(contacts_btn)

        tasks_btn = QPushButton("Tasks")
        tasks_btn.setIcon(QIcon(":/icons/tasks.svg"))
        tasks_btn.clicked.connect(lambda: self.show_view(2))
        nav_layout.addWidget(tasks_btn)
        self.nav_buttons.append(tasks_btn)

        chat_btn = QPushButton("AI Chat")
        chat_btn.setIcon(QIcon(":/icons/chat.svg"))
        chat_btn.clicked.connect(lambda: self.show_view(3))
        nav_layout.addWidget(chat_btn)
        self.nav_buttons.append(chat_btn)

        nav_layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setIcon(QIcon(":/icons/logout.svg"))
        logout_btn.clicked.connect(self.handle_logout)
        nav_layout.addWidget(logout_btn)

        nav.setLayout(nav_layout)
        content.addWidget(nav)

        # Stacked widget for different views
        self.stack = QStackedWidget()
        self.dashboard = DashboardView(self)
        self.contacts = ContactsView(self)
        self.tasks = TasksView(self)
        self.chat = ChatView(self)

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.contacts)
        self.stack.addWidget(self.tasks)
        self.stack.addWidget(self.chat)

        content.addWidget(self.stack)
        layout.addLayout(content)

        self.setLayout(layout)

        # Set initial view
        self.show_view(0)

    def show_view(self, index):
        self.stack.setCurrentIndex(index)
        
        # Update button states
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def set_user(self, user):
        self.user = user
        self.dashboard.update_view()
        self.contacts.update_view()
        self.tasks.update_view()
        self.chat.update_view()

    def handle_logout(self):
        self.user = None
        self.parent.show_login()
