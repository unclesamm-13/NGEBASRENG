from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QDialog, QFormLayout, QComboBox, QDoubleSpinBox,
    QSpinBox, QTextEdit, QDateEdit, QHBoxLayout
)
from PySide6.QtCore import QDate
from utils.db import (
    get_semua_pembelian,
    tambah_pembelian,
    update_pembelian,
    hapus_pembelian
)

# ===================== DIALOG TAMBAH / EDIT =====================
class PembelianDialog(QDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Tambah Pembelian" if data is None else "Edit Pembelian")

        layout = QFormLayout(self)

        self.tanggal = QDateEdit(QDate.currentDate())
        self.tanggal.setCalendarPopup(True)

        self.jenis = QComboBox()
        self.jenis.addItems(["basreng", "kemasan"])

        self.berat = QDoubleSpinBox()
        self.berat.setMaximum(100000)

        self.jumlah = QSpinBox()
        self.jumlah.setMaximum(100000)

        self.total = QDoubleSpinBox()
        self.total.setMaximum(100_000_000)

        self.status = QComboBox()
        self.status.addItems(["lunas", "utang"])

        self.ket = QTextEdit()

        layout.addRow("Tanggal", self.tanggal)
        layout.addRow("Jenis", self.jenis)
        layout.addRow("Berat (g)", self.berat)
        layout.addRow("Jumlah", self.jumlah)
        layout.addRow("Total", self.total)
        layout.addRow("Status", self.status)
        layout.addRow("Keterangan", self.ket)

        # MODE EDIT
        self.id_pembelian = None
        if data:
            self.id_pembelian = int(data[0])
            self.tanggal.setDate(QDate.fromString(data[1], "yyyy-MM-dd"))
            self.jenis.setCurrentText(data[2])
            self.berat.setValue(float(data[3]))
            self.jumlah.setValue(int(data[4]))
            self.total.setValue(float(data[5]))
            self.status.setCurrentText(data[6])
            self.ket.setText(data[7])

        btn = QPushButton("💾 Simpan")
        btn.clicked.connect(self.accept)
        layout.addRow(btn)

    def get_data(self):
        return (
            self.tanggal.date().toString("yyyy-MM-dd"),
            self.jenis.currentText(),
            self.berat.value(),
            self.jumlah.value(),
            self.total.value(),
            self.status.currentText(),
            self.ket.toPlainText()
        )

# ===================== PAGE =====================
class PembelianPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)

        judul = QLabel("Manajemen Pembelian")
        judul.setStyleSheet("font-size:18pt;font-weight:bold;")
        layout.addWidget(judul)

        # ===== TOMBOL ATAS =====
        btn_layout = QHBoxLayout()

        btn_tambah = QPushButton("➕ Tambah Pembelian")
        btn_tambah.clicked.connect(self.tambah_data)

        btn_edit = QPushButton("✏️ Edit (Modal)")
        btn_edit.clicked.connect(self.edit_data)

        btn_hapus = QPushButton("🗑️ Hapus")
        btn_hapus.clicked.connect(self.hapus_data)

        btn_layout.addWidget(btn_tambah)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_hapus)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        # ===== TABEL =====
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tanggal", "Jenis", "Berat",
            "Jumlah", "Total", "Status", "Keterangan"
        ])
        self.table.setColumnHidden(0, True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellClicked.connect(self.highlight_row)

        layout.addWidget(self.table)

    # ================= LOGIC =================
    def highlight_row(self, row, _):
        self.table.clearSelection()
        self.table.selectRow(row)

    def load_data(self):
        self.table.setRowCount(0)
        for r, row in enumerate(get_semua_pembelian()):
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

    def tambah_data(self):
        dialog = PembelianDialog(parent=self)
        if dialog.exec():
            tambah_pembelian(*dialog.get_data())
            self.load_data()

    def edit_data(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Info", "Pilih data terlebih dahulu")
            return

        data = [self.table.item(row, i).text() for i in range(8)]
        dialog = PembelianDialog(data, self)

        if dialog.exec():
            update_pembelian(
                int(data[0]),
                *dialog.get_data()
            )
            self.load_data()

    def hapus_data(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Info", "Pilih data yang ingin dihapus")
            return

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus data pembelian ini?\n\n"
            "Tindakan ini tidak dapat dibatalkan.",
            QMessageBox.Yes | QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            id_pembelian = int(self.table.item(row, 0).text())
            hapus_pembelian(id_pembelian)
            self.load_data()

    def showEvent(self, e):
        self.load_data()
        super().showEvent(e)
