from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QDateEdit,
    QFrame, QGridLayout
)
from PySide6.QtCore import QDate
from utils.db import laporan_ringkas


class KPI(QFrame):
    def __init__(self, title, value="Rp 0", color="#111827"):
        super().__init__()
        self.setObjectName("card")

        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color:#6B7280; font-size:9.5pt;")

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(
            f"font-size:16pt; font-weight:bold; color:{color};"
        )

        layout.addWidget(lbl_title)
        layout.addWidget(self.lbl_value)

    def set_value(self, value):
        self.lbl_value.setText(value)


class LaporanPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # ===== JUDUL =====
        judul = QLabel("Laporan Keuangan")
        judul.setStyleSheet("""
            font-size: 20pt;
            font-weight: bold;
            color: #111827;
        """)
        layout.addWidget(judul)

        # ===== FILTER =====
        filter_layout = QHBoxLayout()

        self.tgl_awal = QDateEdit()
        self.tgl_awal.setDate(QDate.currentDate().addMonths(-1))
        self.tgl_awal.setCalendarPopup(True)

        self.tgl_akhir = QDateEdit()
        self.tgl_akhir.setDate(QDate.currentDate())
        self.tgl_akhir.setCalendarPopup(True)

        btn = QPushButton("📊 Tampilkan Laporan")
        btn.clicked.connect(self.load_laporan)

        filter_layout.addWidget(QLabel("Dari"))
        filter_layout.addWidget(self.tgl_awal)
        filter_layout.addWidget(QLabel("Sampai"))
        filter_layout.addWidget(self.tgl_akhir)
        filter_layout.addStretch()
        filter_layout.addWidget(btn)

        layout.addLayout(filter_layout)

        # ===== KPI GRID =====
        grid = QGridLayout()
        grid.setSpacing(16)

        self.kpi_pembelian = KPI("Total Pembelian", "Rp 0")
        self.kpi_penjualan = KPI("Total Penjualan", "Rp 0")
        self.kpi_laba = KPI("Laba", "Rp 0", "#16A34A")

        self.kpi_pemasukan = KPI("Total Pemasukan", "Rp 0")
        self.kpi_utang = KPI("Utang Belum Lunas", "Rp 0", "#DC2626")
        self.kpi_piutang = KPI("Piutang Belum Lunas", "Rp 0", "#CA8A04")

        grid.addWidget(self.kpi_pembelian, 0, 0)
        grid.addWidget(self.kpi_penjualan, 0, 1)
        grid.addWidget(self.kpi_laba, 0, 2)

        grid.addWidget(self.kpi_pemasukan, 1, 0)
        grid.addWidget(self.kpi_utang, 1, 1)
        grid.addWidget(self.kpi_piutang, 1, 2)

        layout.addLayout(grid)
        layout.addStretch()

    def load_laporan(self):
        tgl_awal = self.tgl_awal.date().toString("yyyy-MM-dd")
        tgl_akhir = self.tgl_akhir.date().toString("yyyy-MM-dd")

        data = laporan_ringkas(tgl_awal, tgl_akhir)

        self.kpi_pembelian.set_value(f"Rp {data['pembelian']:,.0f}")
        self.kpi_penjualan.set_value(f"Rp {data['penjualan']:,.0f}")
        self.kpi_pemasukan.set_value(f"Rp {data['pemasukan']:,.0f}")
        self.kpi_laba.set_value(f"Rp {data['laba']:,.0f}")
        self.kpi_utang.set_value(f"Rp {data['utang']:,.0f}")
        self.kpi_piutang.set_value(f"Rp {data['piutang']:,.0f}")
