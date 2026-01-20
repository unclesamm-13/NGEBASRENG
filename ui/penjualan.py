from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame,QMessageBox
)
from PySide6.QtCore import Qt, QDate
from utils.db import (
    get_semua_penjualan,
    tambah_penjualan,
    update_penjualan,
    get_semua_varian,
    hapus_penjualan
)


class PenjualanPage(QWidget):
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
        title = QLabel("Manajemen Penjualan")
        title.setStyleSheet("font-size:20pt;font-weight:bold;")
        root.addWidget(title)

        # ===== CARD FORM =====
        form_card = QFrame()
        form_card.setObjectName("card")
        form_layout = QHBoxLayout(form_card)
        form_layout.setSpacing(12)

        self.cb_varian = QComboBox()
        self.spin_jumlah = QSpinBox()
        self.spin_jumlah.setMaximum(100000)

        # Tambahkan pilihan status
        self.cb_status = QComboBox()
        self.cb_status.addItems(["lunas", "hutang"])

        self.btn_submit = QPushButton("💾 Simpan")
        self.btn_submit.clicked.connect(self.submit)
        btn_hapus = QPushButton("🗑️ Hapus")
        btn_hapus.clicked.connect(self.hapus_data)
        
        form_layout.addWidget(btn_hapus)
        form_layout.addWidget(self.cb_varian)
        form_layout.addWidget(self.spin_jumlah)
        form_layout.addWidget(self.cb_status)   # tambahkan ke layout
        form_layout.addWidget(self.btn_submit)

        root.addWidget(form_card)

        # ===== CARD TABLE =====
        table_card = QFrame()
        table_card.setObjectName("card")
        table_layout = QVBoxLayout(table_card)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tanggal", "Varian", "Jumlah", "Total", "Status"]
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
        self.cb_varian.clear()

        varian = get_semua_varian()
        for v in varian:
            self.cb_varian.addItem(v[1], v)

        for r, row in enumerate(get_semua_penjualan()):
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def load_to_form(self, row, _):
        self.edit_id = int(self.table.item(row, 0).text())
        self.spin_jumlah.setValue(int(self.table.item(row, 3).text()))
        self.cb_status.setCurrentText(self.table.item(row, 5).text())  # isi status ke combobox
        self.btn_submit.setText("💾 Update")

    def submit(self):
        jumlah = self.spin_jumlah.value()
        status = self.cb_status.currentText()   # ambil status dari combobox

        if self.edit_id:
            status = self.cb_status.currentText()
            update_penjualan(self.edit_id, jumlah, status)
        else:
            varian = self.cb_varian.currentData()
            total = varian[3] * jumlah
            tambah_penjualan(
                QDate.currentDate().toString("yyyy-MM-dd"),
                varian[0],
                jumlah,
                total,
                status   # gunakan pilihan status
            )

        self.reset_form()
        self.load_data()

    def reset_form(self):
        self.edit_id = None
        self.spin_jumlah.setValue(0)
        self.btn_submit.setText("💾 Simpan")
    
    def hapus_data(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Info", "Pilih data yang ingin dihapus")
            return

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus penjualan ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            id_penjualan = int(self.table.item(row, 0).text())
            hapus_penjualan(id_penjualan)
            self.load_data()

    def showEvent(self, event):
        self.load_data()
        super().showEvent(event)
