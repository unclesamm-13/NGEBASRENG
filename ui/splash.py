from PySide6.QtWidgets import (
    QSplashScreen, QWidget, QLabel,
    QVBoxLayout, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QPixmap, QFont
from utils.path_helper import resource_path

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()

        # ===== WINDOW CONFIG =====
        self.setFixedSize(520, 320)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.center_on_screen()

        # ===== CONTAINER =====
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 520, 320)
        self.container.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border-radius: 14px;
            }
        """)

        layout = QVBoxLayout(self.container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        # ===== LOGO =====
        logo = QLabel()
        pixmap = QPixmap(resource_path("assets/logo.png"))
        pixmap = pixmap.scaled(
            90, 90,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        # ===== TITLE =====
        title = QLabel("NGEBASRENG")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Manajemen Usaha Basreng")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #9CA3AF;")
        subtitle.setAlignment(Qt.AlignCenter)

        # ===== PROGRESS BAR =====
        self.progress = QProgressBar()
        self.progress.setFixedWidth(300)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #2A2A2A;
                border-radius: 6px;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #3B82F6;
                border-radius: 6px;
            }
        """)

        self.loading_text = QLabel("Loading…")
        self.loading_text.setStyleSheet("color: #D1D5DB;")
        self.loading_text.setAlignment(Qt.AlignCenter)

        footer = QLabel("© 2026 Basreng Management")
        footer.setStyleSheet("color: #6B7280; font-size:9pt;")
        footer.setAlignment(Qt.AlignCenter)

        # ===== ADD TO LAYOUT =====
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(self.progress)
        layout.addWidget(self.loading_text)
        layout.addSpacing(18)
        layout.addWidget(footer)

        # ===== FADE IN =====
        self.setWindowOpacity(0)
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(700)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()

        # ===== PROGRESS TIMER =====
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)

    # ===== CENTER WINDOW =====
    def center_on_screen(self):
        screen = self.screen().availableGeometry()
        geo = self.frameGeometry()
        geo.moveCenter(screen.center())
        self.move(geo.topLeft())

    # ===== PROGRESS UPDATE =====
    def update_progress(self):
        value = self.progress.value() + 1
        self.progress.setValue(value)
        if value >= 100:
            self.timer.stop()

    # ===== FADE OUT (DIPANGGIL DARI main.py) =====
    def fade_out(self, callback):
        self.fade_out_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_anim.setDuration(600)
        self.fade_out_anim.setStartValue(1)
        self.fade_out_anim.setEndValue(0)
        self.fade_out_anim.finished.connect(callback)
        self.fade_out_anim.start()
