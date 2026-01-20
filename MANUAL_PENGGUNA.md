📄 Lisensi

Aplikasi ini dibuat untuk keperluan akademik (UAS).

# 📕 2️⃣ MANUAL PENGGUNA (USER MANUAL)

## 🧾 MANUAL PENGGUNA  
**Aplikasi NGEBASRENG**

## 1. Pendahuluan
NGEBASRENG adalah aplikasi desktop yang digunakan untuk membantu pengelolaan usaha
penjualan basreng secara sederhana dan terstruktur.

Aplikasi ini ditujukan untuk pelaku UMKM kecil serta keperluan akademik.

## 2. Instalasi Aplikasi

### 2.1 Persyaratan Sistem
- Sistem Operasi: Windows
- Python 3.12
- Library PySide6

### 2.2 Instalasi
1. Install Python dari https://www.python.org
2. Buka Command Prompt
3. Install PySide6:
```bash
pip install PySide6
4.Jalankan aplikasi :
python main.py atau 

3. Cara Menggunakan Aplikasi
    3.1 Dashboard

        Menampilkan ringkasan:

            Total penjualan

            Total pembelian

            Laba bersih

            Utang dan piutang

        Terdapat tombol Reset Semua Data untuk menghapus seluruh data usaha.

    3.2 Manajemen Pembelian

        Tambah data pembelian basreng atau kemasan

        Edit data melalui dialog (modal)

        Hapus data pembelian

        Data otomatis tersimpan ke database

    3.3 Manajemen Varian Produk

        Tambah varian (berat & harga jual)

        Edit dan hapus varian

        Varian digunakan untuk perhitungan dan penjualan

    3.4 Perhitungan Kemasan & HPP

        Pilih pembelian basreng

        Pilih varian produk

        Aplikasi menghitung:

            Jumlah paket teoritis

            Rekomendasi kemasan

            HPP per paket

            Estimasi laba

    3.5 Penjualan

        Input transaksi penjualan

        Data penjualan otomatis masuk ke laporan dan dashboard

    3.6 Laporan Keuangan
        Menampilkan:

            Total pembelian

            Total penjualan

            Laba

            Utang & piutang

        Filter berdasarkan rentang tanggal

    3.7 About

        Menampilkan informasi aplikasi dan pengembang
4. Penutupan Aplikasi

    Saat menutup aplikasi, akan muncul dialog konfirmasi

    Bertujuan mencegah kehilangan data secara tidak sengaja

5. Catatan

    Database bersifat lokal (SQLite)

    Data tidak dikirim ke server

    Aplikasi aman digunakan secara offline