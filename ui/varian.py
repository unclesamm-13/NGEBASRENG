from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QDoubleSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from utils.db import get_semua_varian, tambah_varian, update_varian, hapus_varian


class VarianPage(QWidget):
    def __init__(self):
        super().__init__()
        self.edit_id = None
        self.init_ui()
        self.load_data()

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(20)

        # ===== JUDUL =====
        title = QLabel("Manajemen Varian Produk")
        title.setStyleSheet("font-size:20pt;font-weight:bold;")
        root.addWidget(title)

        # ===== CARD FORM =====
        form_card = QFrame()
        form_card.setObjectName("card")
        form_layout = QHBoxLayout(form_card)
        form_layout.setSpacing(12)

        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Nama Varian")

        self.input_berat = QDoubleSpinBox()
        self.input_berat.setSuffix(" g")
        self.input_berat.setMaximum(10000)

        self.input_harga = QDoubleSpinBox()
        self.input_harga.setPrefix("Rp ")
        self.input_harga.setMaximum(1_000_000)

        self.btn_submit = QPushButton("💾 Simpan")
        self.btn_submit.clicked.connect(self.submit)
        btn_hapus = QPushButton("🗑️ Hapus")
        btn_hapus.clicked.connect(self.hapus_data)

        form_layout.addWidget(btn_hapus)
        form_layout.addWidget(self.input_nama)
        form_layout.addWidget(self.input_berat)
        form_layout.addWidget(self.input_harga)
        form_layout.addWidget(self.btn_submit)

        root.addWidget(form_card)

        # ===== CARD TABLE =====
        table_card = QFrame()
        table_card.setObjectName("card")
        table_layout = QVBoxLayout(table_card)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nama Varian", "Berat (g)", "Harga"]
        )
        self.table.setColumnHidden(0, True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellClicked.connect(self.load_to_form)

        table_layout.addWidget(self.table)
        root.addWidget(table_card)

        # ===== STYLE =====
        self.setStyleSheet("""
            QFrame#card {
                background-color: white;
                border-radius: 14px;
                padding: 16px;
            }
        """)

    # ================= LOGIC =================
    def load_data(self):
        self.table.setRowCount(0)
        for r, row in enumerate(get_semua_varian()):
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def load_to_form(self, row, _):
        self.edit_id = int(self.table.item(row, 0).text())
        self.input_nama.setText(self.table.item(row, 1).text())
        self.input_berat.setValue(float(self.table.item(row, 2).text()))
        self.input_harga.setValue(float(self.table.item(row, 3).text()))
        self.btn_submit.setText("💾 Update")

    def submit(self):
        nama = self.input_nama.text()
        berat = self.input_berat.value()
        harga = self.input_harga.value()

        if self.edit_id:
            update_varian(self.edit_id, nama, berat, harga)
        else:
            tambah_varian(nama, berat, harga)

        self.reset_form()
        self.load_data()

    def reset_form(self):
        self.edit_id = None
        self.input_nama.clear()
        self.input_berat.setValue(0)
        self.input_harga.setValue(0)
        self.btn_submit.setText("💾 Simpan")
    
    def hapus_data(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Info", "Pilih data yang ingin dihapus")
            return

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus varian ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            id_varian = int(self.table.item(row, 0).text())
            hapus_varian(id_varian)
            self.load_data()

    def showEvent(self, event):
        self.load_data()
        super().showEvent(event)
