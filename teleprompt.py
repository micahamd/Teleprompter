import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QSlider, QLabel)
from PyQt6.QtCore import Qt, QTimer, QSettings
from PyQt6.QtGui import QFont, QPalette, QColor, QKeySequence, QShortcut

class Teleprompter(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create settings object to store user preferences
        self.settings = QSettings("MyCompany", "Teleprompter")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Teleprompter')
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Text edit for input
        self.text_edit = QTextEdit()
        main_layout.addWidget(self.text_edit)

        # Controls layout
        controls_layout = QHBoxLayout()

        # Play button
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.toggle_play)
        controls_layout.addWidget(self.play_button)

        # Font size slider
        self.font_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_size_slider.setRange(10, 30)
        # Load saved font size or use default of 14
        saved_font_size = self.settings.value("font_size", 14, type=int)
        self.font_size_slider.setValue(saved_font_size)
        self.font_size_slider.valueChanged.connect(self.change_font_size)
        controls_layout.addWidget(QLabel('Font Size:'))
        controls_layout.addWidget(self.font_size_slider)

        # Speed slider
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 10)
        # Load saved speed or use default of 5
        saved_speed = self.settings.value("speed", 5, type=int)
        self.speed_slider.setValue(saved_speed)
        controls_layout.addWidget(QLabel('Speed:'))
        controls_layout.addWidget(self.speed_slider)

        # Theme toggle button
        self.theme_button = QPushButton('Toggle Theme')
        self.theme_button.clicked.connect(self.toggle_theme)
        controls_layout.addWidget(self.theme_button)

        main_layout.addLayout(controls_layout)

        # Set up scrolling timer
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.scroll_text)

        # Initialize variables
        self.is_playing = False
        # Load saved theme preference or use light theme as default
        self.is_dark_theme = self.settings.value("dark_theme", False, type=bool)
        self.change_font_size(self.font_size_slider.value())
        self.apply_theme()

        # Keyboard shortcuts
        QShortcut(QKeySequence("Ctrl+P"), self, self.toggle_play)
        QShortcut(QKeySequence("Ctrl+R"), self, self.reset_scroll)

        # Connect the closing event to save settings
        self.destroyed.connect(self.save_settings)

    def toggle_play(self):
        """Toggle between play and pause states"""
        if self.is_playing:
            self.scroll_timer.stop()
            self.play_button.setText('Play')
        else:
            self.scroll_timer.start(50)  # Timer fires every 50ms
            self.play_button.setText('Pause')
        self.is_playing = not self.is_playing

    def scroll_text(self):
        """Scroll the text in the QTextEdit"""
        scrollbar = self.text_edit.verticalScrollBar()
        if scrollbar.value() < scrollbar.maximum():
            # Increment scroll position by speed value
            scrollbar.setValue(scrollbar.value() + self.speed_slider.value())
        else:
            # If we've reached the end, stop playing
            self.toggle_play()

    def change_font_size(self, size):
        """Change the font size of the text edit"""
        font = QFont('Arial', size)
        self.text_edit.setFont(font)

    def toggle_theme(self):
        """Switch between light and dark themes"""
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to the text edit"""
        palette = self.text_edit.palette()
        if self.is_dark_theme:
            palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        else:
            palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        self.text_edit.setPalette(palette)

    def reset_scroll(self):
        """Reset the scroll position to the top"""
        self.text_edit.verticalScrollBar().setValue(0)

    def resizeEvent(self, event):
        """Handle window resize event"""
        super().resizeEvent(event)
        # Adjust font size based on window width
        width = self.width()
        new_size = max(10, min(30, width // 40))
        self.font_size_slider.setValue(new_size)

    def save_settings(self):
        """Save user preferences"""
        self.settings.setValue("font_size", self.font_size_slider.value())
        self.settings.setValue("speed", self.speed_slider.value())
        self.settings.setValue("dark_theme", self.is_dark_theme)

    def closeEvent(self, event):
        """Handle window close event"""
        self.save_settings()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    teleprompter = Teleprompter()
    teleprompter.show()
    sys.exit(app.exec())