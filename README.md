# NGEBASRENG 🍟

Aplikasi manajemen penjualan basreng (baso goreng) dengan tampilan GUI berbasis **Python + PySide6**.  
Project ini dibuat untuk kebutuhan kuliah **Pemrograman Visual** dan dikembangkan agar mudah digunakan untuk mengelola transaksi, hutang, dan piutang.

---

## 🚀 Fitur Utama
- **Dashboard interaktif**: menampilkan ringkasan hutang (pembelian) dan piutang (penjualan).
- **Manajemen transaksi**: input, edit, dan hapus data penjualan/pembelian.
- **Laporan otomatis**: sinkronisasi data transaksi dengan summary table.
- **Cross-platform**: bisa dijalankan di Windows, Linux, dan macOS.
- **UI modern**: menggunakan PySide6 untuk tampilan yang lebih elegan.

---

## 🛠️ Teknologi yang Digunakan
- **Python 3.10+**
- **PySide6** (GUI)
- **SQLite3** (database lokal)
- **Utils & Assets** untuk modularisasi kode

---

## 📂 Struktur Project
BASRENG_APP/ 

│── ui/              # File tampilan (UI) 

│── utils/           # Helper & fungsi tambahan 

│── assets/          # Gambar/icon 


│── main.py          # Entry point aplikasi 

│── requirements.txt # Dependency project

│── README.md        # Dokumentasi project

---

## ⚙️ Instalasi & Menjalankan
1. Clone repo:
   ```bash
   git clone https://github.com/unclesamm-13/NGEBASRENG.git
   cd NGEBASRENG
2. Buat virtual environment (opsional tapi disarankan):
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
3. Install dependencies:
    pip install -r requirements.txt
4. Jalankan aplikasi:
python main.py

## 📌 Catatan
- Pastikan Python sudah terinstall minimal versi 3.10.
- Database default menggunakan SQLite, bisa diganti sesuai kebutuhan.
- Project ini masih dalam tahap pengembangan.

## 👨‍💻 Author
Muhammad Farel (unclesamm-13)
Mahasiswa Semester 3 Teknik Informatika – Pemrograman Visual
Pontianak, Kalimantan Barat, Indonesia


