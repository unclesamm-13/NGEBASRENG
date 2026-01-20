from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from utils.db import laporan_ringkas, reset_semua_data


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    # ================= UI =================
    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 32, 40, 32)
        root.setSpacing(24)

        # ===== HEADER =====
        title = QLabel("Dashboard Usaha Basreng")
        title.setStyleSheet("""
            font-size: 22pt;
            font-weight: bold;
            color: #111827;
        """)

        subtitle = QLabel("Ringkasan kondisi usaha secara real-time")
        subtitle.setStyleSheet("""
            color: #6B7280;
            font-size: 10.5pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        # ===== KPI GRID =====
        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(20)

        self.card_penjualan = self.kpi_card("Total Penjualan", "#2563EB")
        self.card_pembelian = self.kpi_card("Total Pembelian", "#7C3AED")
        self.card_laba = self.kpi_card("Laba Bersih", "#16A34A")
        self.card_utang = self.kpi_card("Utang", "#DC2626")
        self.card_piutang = self.kpi_card("Piutang", "#F59E0B")

        grid.addWidget(self.card_penjualan, 0, 0)
        grid.addWidget(self.card_pembelian, 0, 1)
        grid.addWidget(self.card_laba, 0, 2)
        grid.addWidget(self.card_utang, 1, 0)
        grid.addWidget(self.card_piutang, 1, 1)

        root.addLayout(grid)
        root.addStretch()  # dorong tombol ke bawah

        # ===== RESET BUTTON (BOTTOM) =====
        btn_reset = QPushButton("🧹 Reset Semua Data")
        btn_reset.setCursor(Qt.PointingHandCursor)
        btn_reset.setFixedHeight(36)
        btn_reset.clicked.connect(self.reset_data)
        btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)

        root.addWidget(btn_reset, alignment=Qt.AlignRight)

        # ===== CARD STYLE =====
        self.setStyleSheet("""
            QFrame#kpi_card {
                background-color: white;
                border-radius: 14px;
            }
        """)

    # ================= KPI CARD =================
    def kpi_card(self, title, color):
        card = QFrame()
        card.setObjectName("kpi_card")
        card.setMinimumHeight(130)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("""
            font-size: 10.5pt;
            color: #6B7280;
        """)

        lbl_value = QLabel("Rp 0")
        lbl_value.setStyleSheet(f"""
            font-size: 20pt;
            font-weight: bold;
            color: {color};
        """)

        layout.addWidget(lbl_title)
        layout.addStretch()
        layout.addWidget(lbl_value)

        card.value_label = lbl_value
        return card

    # ================= DATA =================
    def load_data(self):
        data = laporan_ringkas("0000-01-01", "9999-12-31")

        self.card_penjualan.value_label.setText(f"Rp {data['penjualan']:,.0f}")
        self.card_pembelian.value_label.setText(f"Rp {data['pembelian']:,.0f}")
        self.card_laba.value_label.setText(f"Rp {data['laba']:,.0f}")
        self.card_utang.value_label.setText(f"Rp {data['utang']:,.0f}")
        self.card_piutang.value_label.setText(f"Rp {data['piutang']:,.0f}")

        if data["laba"] < 0:
            self.card_laba.value_label.setStyleSheet(
                "font-size:20pt;font-weight:bold;color:#DC2626;"
            )
        else:
            self.card_laba.value_label.setStyleSheet(
                "font-size:20pt;font-weight:bold;color:#16A34A;"
            )

    # ================= RESET =================
    def reset_data(self):
        confirm = QMessageBox.question(
            self,
            "Reset Semua Data",
            "Semua data akan dihapus dan aplikasi kembali ke kondisi awal.\n\n"
            "⚠️ Tindakan ini tidak dapat dibatalkan.\n\n"
            "Apakah Anda yakin?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            reset_semua_data()
            self.load_data()

            QMessageBox.information(
                self,
                "Berhasil",
                "Semua data berhasil direset.\nAplikasi kembali ke kondisi awal."
            )

    # ================= AUTO REFRESH =================
    def showEvent(self, event):
        self.load_data()
        super().showEvent(event)
