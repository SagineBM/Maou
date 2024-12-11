from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QTextEdit, QComboBox, QLineEdit, QLabel, QDialog)
from PyQt5.QtCore import Qt
import json
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage

class StreamHandler(BaseCallbackHandler):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def on_llm_new_token(self, token: str, **kwargs):
        self.text_widget.insertPlainText(token)
        self.text_widget.ensureCursorVisible()

class AISettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI Settings")
        self.api_label = QLabel("API Key:")
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # AI Provider Selection
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI", "Ollama", "Custom"])
        layout.addWidget(QLabel("AI Provider:"))
        layout.addWidget(self.provider_combo)

        # Model Selection
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.update_model_list("OpenAI")
        layout.addWidget(QLabel("Model:"))
        layout.addWidget(self.model_combo)

        # API Key / URL
        layout.addWidget(self.api_label)
        self.api_input = QLineEdit()
        layout.addWidget(self.api_input)

        # Save Button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        self.setLayout(layout)
        
        # Connect signals
        self.provider_combo.currentTextChanged.connect(self.update_model_list)

    def update_model_list(self, provider):
        self.model_combo.clear()
        if provider == "OpenAI":
            self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4"])
            self.api_label.setText("API Key:")
        elif provider == "Ollama":
            self.model_combo.addItems(["llama2", "mistral", "codellama"])
            self.api_label.setText("URL (default: http://localhost:11434):")
        else:
            self.model_combo.setEditText("")
            self.api_label.setText("API Endpoint:")

    def load_settings(self):
        try:
            with open("ai_settings.json", "r") as f:
                settings = json.load(f)
                self.provider_combo.setCurrentText(settings.get("provider", "OpenAI"))
                self.model_combo.setCurrentText(settings.get("model", ""))
                self.api_input.setText(settings.get("api_key", ""))
        except FileNotFoundError:
            pass

    def save_settings(self):
        settings = {
            "provider": self.provider_combo.currentText(),
            "model": self.model_combo.currentText(),
            "api_key": self.api_input.text()
        }
        with open("ai_settings.json", "w") as f:
            json.dump(settings, f)
        self.accept()

class ChatView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Settings button
        settings_layout = QHBoxLayout()
        settings_btn = QPushButton("AI Settings")
        settings_btn.clicked.connect(self.show_settings)
        settings_layout.addWidget(settings_btn)
        settings_layout.addStretch()
        layout.addLayout(settings_layout)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        input_layout.addWidget(self.input_field)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def load_settings(self):
        try:
            with open("ai_settings.json", "r") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                "provider": "OpenAI",
                "model": "gpt-3.5-turbo",
                "api_key": ""
            }

    def setup_ai(self):
        if self.settings["provider"] == "OpenAI":
            return ChatOpenAI(
                model_name=self.settings["model"],
                openai_api_key=self.settings["api_key"],
                streaming=True,
                callbacks=[StreamHandler(self.chat_display)]
            )
        elif self.settings["provider"] == "Ollama":
            base_url = self.settings["api_key"] or "http://localhost:11434"
            return Ollama(
                base_url=base_url,
                model=self.settings["model"],
                callbacks=[StreamHandler(self.chat_display)]
            )
        else:
            raise NotImplementedError("Custom AI providers not yet implemented")

    def send_message(self):
        message = self.input_field.toPlainText().strip()
        if not message:
            return

        # Display user message
        self.chat_display.append(f"You: {message}\n")
        self.chat_display.append("AI: ")
        
        try:
            ai = self.setup_ai()
            messages = [HumanMessage(content=message)]
            ai.invoke(messages)
            self.chat_display.append("\n\n")
        except Exception as e:
            self.chat_display.append(f"Error: {str(e)}\n\n")

        self.input_field.clear()

    def show_settings(self):
        dialog = AISettingsDialog(self)
        if dialog.exec():
            self.load_settings()

    def update_view(self):
        # Clear chat history when user changes
        self.chat_display.clear()
        self.load_settings()
