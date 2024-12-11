from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QColor
from models.base import get_session
from models.task import Task
from models.contact import Contact
from datetime import datetime, timedelta
import ui.resources_rc

class StatCard(QFrame):
    def __init__(self, title, value, icon_path, parent=None):
        super().__init__(parent)
        self.setObjectName("stat-card")
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(32, 32)))
        layout.addWidget(icon_label)
        
        # Text container
        text_container = QVBoxLayout()
        text_container.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setObjectName("stat-title")
        
        value_label = QLabel(str(value))
        value_label.setObjectName("stat-value")
        value_label.setProperty("value", True)
        
        text_container.addWidget(title_label)
        text_container.addWidget(value_label)
        
        layout.addLayout(text_container)
        layout.addStretch()
        
        self.setLayout(layout)
        self.value_label = value_label

    def update_value(self, value):
        self.value_label.setText(str(value))

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.engine = parent.engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)

        # Header section
        header_container = QHBoxLayout()
        
        # Title and subtitle
        title_container = QVBoxLayout()
        title_container.setSpacing(8)
        
        header = QLabel("Dashboard")
        header.setObjectName("page-header")
        
        subtitle = QLabel("Welcome back! Here's an overview of your CRM")
        subtitle.setObjectName("page-subtitle")
        
        title_container.addWidget(header)
        title_container.addWidget(subtitle)
        
        header_container.addLayout(title_container)
        header_container.addStretch()
        
        layout.addLayout(header_container)

        # Statistics section
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(24)

        # Create stat cards with icons
        self.contacts_card = StatCard("Total Contacts", "0", ":/icons/contacts.svg")
        self.tasks_card = StatCard("Active Tasks", "0", ":/icons/tasks.svg")
        self.overdue_card = StatCard("Overdue Tasks", "0", ":/icons/tasks.svg")

        stats_layout.addWidget(self.contacts_card)
        stats_layout.addWidget(self.tasks_card)
        stats_layout.addWidget(self.overdue_card)

        layout.addLayout(stats_layout)

        # Recent Activity Section
        activity_container = QFrame()
        activity_container.setObjectName("activity-container")
        activity_layout = QVBoxLayout()
        activity_layout.setContentsMargins(24, 24, 24, 24)
        activity_layout.setSpacing(16)
        
        # Activity header with icon
        activity_header = QHBoxLayout()
        
        activity_icon = QLabel()
        activity_icon.setPixmap(QIcon(":/icons/tasks.svg").pixmap(QSize(24, 24)))
        activity_header.addWidget(activity_icon)
        
        activity_label = QLabel("Recent Activity")
        activity_label.setObjectName("section-header")
        activity_header.addWidget(activity_label)
        activity_header.addStretch()
        
        activity_layout.addLayout(activity_header)

        # Activity content
        self.activity_area = QScrollArea()
        self.activity_area.setWidgetResizable(True)
        self.activity_area.setObjectName("activity-area")
        
        self.activity_widget = QWidget()
        self.activity_layout = QVBoxLayout(self.activity_widget)
        self.activity_layout.setContentsMargins(0, 0, 0, 0)
        self.activity_layout.setSpacing(8)
        
        self.activity_area.setWidget(self.activity_widget)
        activity_layout.addWidget(self.activity_area)
        
        activity_container.setLayout(activity_layout)
        layout.addWidget(activity_container, 1)

        self.setLayout(layout)

    def update_view(self):
        if not self.parent.user:
            return

        session = get_session(self.engine)
        
        # Update statistics
        contact_count = session.query(Contact).filter_by(owner_id=self.parent.user.id).count()
        active_tasks = session.query(Task).filter_by(
            assigned_to_id=self.parent.user.id
        ).filter(Task.status != 'completed').count()
        
        overdue_tasks = session.query(Task).filter_by(
            assigned_to_id=self.parent.user.id
        ).filter(
            Task.due_date < datetime.utcnow()
        ).filter(Task.status != 'completed').count()

        # Update card values
        self.contacts_card.update_value(contact_count)
        self.tasks_card.update_value(active_tasks)
        self.overdue_card.update_value(overdue_tasks)

        session.close()
