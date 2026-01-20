from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QPushButton,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from utils.db import get_pembelian_basreng, get_semua_varian, simpan_perhitungan
from utils.kalkulasi import hitung_paket, rekomendasi_kemasan, hitung_hpp


class PerhitunganPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    # ================= UI =================
    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(20)

        # ===== JUDUL =====
        judul = QLabel("Perhitungan Kemasan & HPP")
        judul.setStyleSheet("""
            font-size: 20pt;
            font-weight: bold;
            color: #111827;
        """)
        root.addWidget(judul)

        # ================= INPUT CARD =================
        input_card = QFrame()
        input_card.setObjectName("card")
        input_layout = QHBoxLayout(input_card)
        input_layout.setSpacing(12)

        self.cb_pembelian = QComboBox()
        self.cb_varian = QComboBox()

        self.input_buffer = QSpinBox()
        self.input_buffer.setMinimum(0)
        self.input_buffer.setMaximum(100)
        self.input_buffer.setValue(1)

        btn_hitung = QPushButton("🧮 Hitung")
        btn_hitung.setCursor(Qt.PointingHandCursor)
        btn_hitung.clicked.connect(self.hitung)

        input_layout.addWidget(self._field("Pembelian Basreng", self.cb_pembelian))
        input_layout.addWidget(self._field("Varian Produk", self.cb_varian))
        input_layout.addWidget(self._field("Buffer (cadangan)", self.input_buffer))
        input_layout.addWidget(btn_hitung)

        root.addWidget(input_card)

        # ================= OUTPUT CARD =================
        output_card = QFrame()
        output_card.setObjectName("card")
        output_layout = QVBoxLayout(output_card)
        output_layout.setSpacing(10)

        self.lbl_teoritis = QLabel("-")
        self.lbl_min = QLabel("-")
        self.lbl_aman = QLabel("-")
        self.lbl_hpp = QLabel("-")
        self.lbl_laba = QLabel("-")

        output_layout.addWidget(self._result("Jumlah Paket (Teoritis)", self.lbl_teoritis))
        output_layout.addWidget(self._result("Rekomendasi Minimal", self.lbl_min))
        output_layout.addWidget(self._result("Rekomendasi Aman", self.lbl_aman))
        output_layout.addWidget(self._result("HPP per Paket", self.lbl_hpp))
        output_layout.addWidget(self._result("Laba per Paket", self.lbl_laba))

        root.addWidget(output_card)

        # ===== STYLE CARD =====
        self.setStyleSheet("""
            QFrame#card {
                background-color: white;
                border-radius: 12px;
                padding: 16px;
            }
        """)

    # ================= HELPER UI =================
    def _field(self, label_text, widget):
        box = QVBoxLayout()
        lbl = QLabel(label_text)
        lbl.setStyleSheet("font-weight:600; color:#374151;")
        box.addWidget(lbl)
        box.addWidget(widget)

        container = QWidget()
        container.setLayout(box)
        return container

    def _result(self, title, value_label):
        row = QHBoxLayout()
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color:#374151;")

        value_label.setStyleSheet("""
            font-weight: bold;
            color: #111827;
        """)

        row.addWidget(lbl_title)
        row.addStretch()
        row.addWidget(value_label)

        container = QWidget()
        container.setLayout(row)
        return container

    # ================= DATA =================
    def load_data(self):
        self.cb_pembelian.clear()
        self.cb_varian.clear()

        self.pembelian_data = get_pembelian_basreng()
        self.varian_data = get_semua_varian()

        for p in self.pembelian_data:
            self.cb_pembelian.addItem(
                f"{p[1]} | {p[2]} g | Rp {p[3]:,.0f}",
                userData=p
            )

        for v in self.varian_data:
            self.cb_varian.addItem(
                f"{v[1]} ({v[2]} g) - Rp {v[3]:,.0f}",
                userData=v
            )

    # ================= LOGIC =================
    def hitung(self):
        if not self.pembelian_data or not self.varian_data:
            QMessageBox.warning(self, "Info", "Data pembelian atau varian belum tersedia")
            return

        pembelian = self.cb_pembelian.currentData()
        varian = self.cb_varian.currentData()

        id_pembelian, _, berat_total, total_biaya = pembelian
        id_varian, _, berat_paket, harga_jual = varian

        jumlah_teoritis = hitung_paket(berat_total, berat_paket)
        min_pack, aman_pack = rekomendasi_kemasan(
            jumlah_teoritis, self.input_buffer.value()
        )
        hpp = hitung_hpp(total_biaya, aman_pack)
        laba = harga_jual - hpp

        self.lbl_teoritis.setText(f"{jumlah_teoritis:.2f} paket")
        self.lbl_min.setText(f"{min_pack} paket")
        self.lbl_aman.setText(f"{aman_pack} paket")
        self.lbl_hpp.setText(f"Rp {hpp:,.0f}")
        self.lbl_laba.setText(f"Rp {laba:,.0f}")

        if laba > 0:
            self.lbl_laba.setStyleSheet("color:#16A34A; font-weight:bold;")
        else:
            self.lbl_laba.setStyleSheet("color:#DC2626; font-weight:bold;")

        simpan_perhitungan(
            id_pembelian, id_varian,
            jumlah_teoritis, min_pack,
            aman_pack, hpp
        )

        QMessageBox.information(
            self,
            "Berhasil",
            "Perhitungan berhasil dilakukan dan disimpan"
        )

    def showEvent(self, event):
        self.load_data()
        super().showEvent(event)
