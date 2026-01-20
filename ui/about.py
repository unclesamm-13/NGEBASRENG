from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from utils.path_helper import resource_path

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About NGEBASRENG")
        self.setFixedSize(420, 360)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        # ===== LOGO =====
        logo = QLabel()
        pixmap = QPixmap(resource_path("assets/logo.png"))
        pixmap = pixmap.scaled(
            80, 80,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        # ===== APP NAME =====
        app_name = QLabel("NGEBASRENG")
        app_name.setFont(QFont("Segoe UI", 18, QFont.Bold))
        app_name.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Aplikasi Manajemen Usaha Basreng")
        subtitle.setStyleSheet("color:#6B7280;")
        subtitle.setAlignment(Qt.AlignCenter)

        # ===== INFO =====
        info = QLabel(
            "Dibuat oleh:\n"
            "MUHAMMAD FAREL\n"
            "NIM (3202416015)\n"
            "Teknik Informatika\n\n"
            "Versi Aplikasi: 1.0.0\n"
            "Tahun: 2026"
        )
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color:#374151;")

        # ===== BUTTON =====
        btn_close = QPushButton("Tutup")
        btn_close.clicked.connect(self.accept)
        btn_close.setFixedWidth(100)

        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(app_name)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(info)
        layout.addStretch()
        layout.addWidget(btn_close, alignment=Qt.AlignCenter)
