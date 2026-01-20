import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

from ui.splash import SplashScreen
from utils.db import init_db

from ui.dashboard import DashboardPage
from ui.pembelian import PembelianPage
from ui.varian import VarianPage
from ui.perhitungan import PerhitunganPage
from ui.penjualan import PenjualanPage
from ui.laporan import LaporanPage
from ui.about import AboutDialog
from utils.path_helper import resource_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Pengatur Usaha Basreng")

        # Ukuran awal aman
        self.resize(820, 520)
        self.setMinimumSize(780, 480)

        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setObjectName("sidebar")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)
        sidebar_layout.setSpacing(4)

        self.nav_buttons = []
        

        def nav_button(text, index):
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(38)
            btn.clicked.connect(lambda: self.switch_page(index, btn))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            return btn

        self.btn_dashboard = nav_button("Dashboard", 0)
        self.btn_pembelian = nav_button("Pembelian", 1)
        self.btn_varian = nav_button("Varian Produk", 2)
        self.btn_perhitungan = nav_button("Perhitungan", 3)
        self.btn_penjualan = nav_button("Penjualan", 4)
        self.btn_laporan = nav_button("Laporan", 5)

        sidebar_layout.addStretch()

        # ================= ABOUT (BOTTOM) =================
        btn_about = QPushButton("  About")
        btn_about.setCursor(Qt.PointingHandCursor)
        btn_about.setFixedHeight(34)
        btn_about.setIcon(QIcon(resource_path("assets/about.png")))
        btn_about.setToolTip("Tentang aplikasi & pengembang")
        btn_about.clicked.connect(self.show_about)

        btn_about.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #9CA3AF;
                border-radius: 6px;
                padding-left: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2D2D30;
                color: white;
            }
        """)

        sidebar_layout.addWidget(btn_about)

        # ================= CONTENT =================
        self.stack = QStackedWidget()
        self.stack.setObjectName("content")

        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(PembelianPage())
        self.stack.addWidget(VarianPage())
        self.stack.addWidget(PerhitunganPage())
        self.stack.addWidget(PenjualanPage())
        self.stack.addWidget(LaporanPage())

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self.stack)

        # Default page
        self.switch_page(0, self.btn_dashboard)

        self.apply_style()

    # ================= NAVIGATION =================
    def switch_page(self, index, active_button):
        self.stack.setCurrentIndex(index)

        for btn in self.nav_buttons:
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        active_button.setProperty("active", True)
        active_button.style().unpolish(active_button)
        active_button.style().polish(active_button)

    # ================= ABOUT =================
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    # ================= EXIT CONFIRM =================
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Keluar Aplikasi",
            "Apakah Anda yakin ingin keluar dari aplikasi?\n\n"
            "Pastikan semua data sudah disimpan.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # ================= STYLE =================
    def apply_style(self):
        self.setStyleSheet("""
        * {
            font-family: Segoe UI;
            font-size: 10.5pt;
        }

        QWidget#sidebar {
            background-color: #1E1E1E;
        }

        QWidget#sidebar QPushButton {
            background-color: transparent;
            color: #D1D5DB;
            border-radius: 6px;
            padding-left: 12px;
            text-align: left;
        }

        QWidget#sidebar QPushButton:hover {
            background-color: #2A2A2A;
        }

        QWidget#sidebar QPushButton[active="true"] {
            background-color: #2D2D30;
            color: white;
            font-weight: bold;
            border-left: 4px solid #3B82F6;
        }

        QStackedWidget#content {
            background-color: #F5F7FA;
        }
        """)


# ================= ENTRY =================
if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    def start_main_window():
        window = MainWindow()
        window.show()
        splash.fade_out(lambda: splash.finish(window))

    QTimer.singleShot(2500, start_main_window)
    sys.exit(app.exec())
