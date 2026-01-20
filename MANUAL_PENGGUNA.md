## 📖 Manual Pengguna – NGEBASRENG

## 1. Pendahuluan
NGEBASRENG adalah aplikasi berbasis Python + PySide6 untuk mengelola penjualan basreng (baso goreng). Aplikasi ini menyediakan fitur pencatatan transaksi, hutang, piutang, serta laporan ringkas dalam bentuk dashboard.

## 2. Persyaratan Sistem
- OS: Windows 10/11, Linux, atau macOS
- Python: Versi 3.10 atau lebih baru
- Library tambahan: PySide6, SQLite3, dan modul Python standar

## 3. Instalasi
    1. Clone repository:
        git clone https://github.com/unclesamm-13/NGEBASRENG.git
        cd NGEBASRENG
    2. Buat virtual environment (opsional):
        python -m venv venv
        venv\Scripts\activate   # Windows
        source venv/bin/activate # Linux/Mac
   3. Install dependencies:
      
        pip install -r requirements.txt

## 4. Menjalankan Aplikasi
   1.Pastikan berada di folder project.
   2.Jalankan perintah:
       python main.py
   3.Tampilan GUI akan muncul dengan menu utama.
   
## 5. Fitur Utama
- Dashboard
Menampilkan ringkasan hutang (pembelian) dan piutang (penjualan).
- Transaksi Penjualan
Input data penjualan, edit, dan hapus transaksi.
- Transaksi Pembelian
Catat hutang dari pembelian barang.
- Laporan
Data transaksi otomatis tersinkronisasi ke summary table untuk laporan keuangan.

## 6. Navigasi Aplikasi
- Menu Utama → akses ke Dashboard, Penjualan, Pembelian, dan Laporan.
- Form Input → isi detail transaksi (tanggal, jumlah, harga, status).
- Tombol Simpan/Edit/Hapus → mengelola data transaksi.
- Summary Table → menampilkan total hutang/piutang secara otomatis.

## 7. Tips Penggunaan
- Gunakan virtual environment agar dependency tetap terkontrol.
- Pastikan database SQLite tidak dihapus agar data transaksi tetap tersimpan.
- Lakukan commit berkala ke GitHub untuk menjaga versi aplikasi.

## 8. Troubleshooting
- Aplikasi tidak jalan → cek versi Python (python --version).
- GUI error → pastikan PySide6 sudah terinstall (pip install PySide6).
- Data tidak tersimpan → cek file database .sqlite3 di folder project.

## 9. Pengembang
    
Author: Muhammad Farel(unclesamm-13)
Tujuan: Project UAS Pemrograman Visual – Semester 3


