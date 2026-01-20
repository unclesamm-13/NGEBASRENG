import os
import sys
import shutil
import sqlite3
from pathlib import Path

# ======================================================
# PATH DATABASE (AMAN PYINSTALLER & MODE DEV)
# ======================================================

def get_base_path():
    """
    Mengembalikan base path aplikasi.
    Support Python biasa & PyInstaller (.exe)
    """
    if getattr(sys, 'frozen', False):
        # Mode EXE (PyInstaller)
        return sys._MEIPASS
    else:
        # Mode Python biasa
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_database():
    """
    Setup database: copy template kosong ke folder permanen user
    jika belum ada, lalu kembalikan path database permanen.
    """
    # Lokasi database permanen di Documents
    db_path = Path.home() / "Documents" / "NGEBASRENG" / "basreng.db"

    # Buat folder kalau belum ada
    os.makedirs(db_path.parent, exist_ok=True)

    # Path template database (di bundle / project)
    base_dir = get_base_path()
    template_db = os.path.join(base_dir, "database", "basreng.db")

    # Kalau database permanen belum ada, copy dari template
    if not db_path.exists():
        shutil.copy(template_db, db_path)

    return str(db_path)


def get_connection():
    """
    Membuat koneksi ke database SQLite permanen.
    """
    db_file = setup_database()
    return sqlite3.connect(db_file)



def init_db():
    """
    Inisialisasi database dan membuat tabel-tabel
    jika belum tersedia.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pembelian (
            id_pembelian INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            jenis TEXT,
            berat_gram REAL,
            jumlah INTEGER,
            total_harga REAL,
            status_bayar TEXT,
            keterangan TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS varian_produk (
            id_varian INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_varian TEXT,
            berat_per_paket REAL,
            harga_jual REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perhitungan_kemasan (
            id_hitung INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pembelian INTEGER,
            id_varian INTEGER,
            hasil_teoritis REAL,
            rekom_min INTEGER,
            rekom_aman INTEGER,
            hpp_per_paket REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penjualan (
            id_penjualan INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            id_varian INTEGER,
            jumlah_paket INTEGER,
            total_harga REAL,
            status_bayar TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pemasukan (
            id_pemasukan INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            sumber TEXT,
            jumlah REAL,
            keterangan TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pengeluaran (
            id_pengeluaran INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            sumber TEXT,
            jumlah REAL,
            keterangan TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utang_piutang (
            id_up INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            tipe TEXT,
            nama_pihak TEXT,
            jumlah REAL,
            status TEXT,
            keterangan TEXT
        )
    """)

    conn.commit()
    conn.close()


# ======================================================
# VARIAN PRODUK
# ======================================================

def tambah_varian(nama, berat, harga):
    """
    Menyimpan data varian produk ke database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO varian_produk (nama_varian, berat_per_paket, harga_jual) VALUES (?, ?, ?)",
        (nama, berat, harga)
    )
    conn.commit()
    conn.close()


def get_semua_varian():
    """
    Mengambil seluruh data varian produk.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_varian, nama_varian, berat_per_paket, harga_jual FROM varian_produk"
    )
    data = cursor.fetchall()
    conn.close()
    return data


def hapus_varian(id_varian):
    """
    Menghapus data varian berdasarkan ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM varian_produk WHERE id_varian = ?",
        (id_varian,)
    )
    conn.commit()
    conn.close()


# ======================================================
# PEMBELIAN
# ======================================================

def tambah_pembelian(tanggal, jenis, berat_gram, jumlah, total_harga, status_bayar, keterangan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pembelian
        (tanggal, jenis, berat_gram, jumlah, total_harga, status_bayar, keterangan)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (tanggal, jenis, berat_gram, jumlah, total_harga, status_bayar, keterangan))

    # Jika status hutang, simpan juga ke utang_piutang
    if status_bayar.lower() in ("utang", "hutang"):
        cursor.execute("""
            INSERT INTO utang_piutang (tanggal, tipe, nama_pihak, jumlah, status, keterangan)
            VALUES (?, 'utang', ?, ?, 'belum lunas', ?)
        """, (tanggal, "Supplier", total_harga, keterangan))

    conn.commit()
    conn.close()

def get_semua_pembelian():
    """
    Mengambil seluruh data pembelian.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_pembelian, tanggal, jenis, berat_gram, jumlah,
               total_harga, status_bayar, keterangan
        FROM pembelian
        ORDER BY tanggal DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def get_pembelian_basreng():
    """
    Mengambil data pembelian khusus basreng.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_pembelian, tanggal, berat_gram, total_harga
        FROM pembelian
        WHERE jenis = 'basreng'
        ORDER BY tanggal DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


# ======================================================
# PERHITUNGAN
# ======================================================

def simpan_perhitungan(id_pembelian, id_varian, hasil_teoritis, rekom_min, rekom_aman, hpp_per_paket):
    """
    Menyimpan hasil perhitungan kemasan dan HPP.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO perhitungan_kemasan
        (id_pembelian, id_varian, hasil_teoritis, rekom_min, rekom_aman, hpp_per_paket)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_pembelian, id_varian, hasil_teoritis, rekom_min, rekom_aman, hpp_per_paket))
    conn.commit()
    conn.close()


# ======================================================
# PENJUALAN & PEMASUKAN
# ======================================================

def tambah_penjualan(tanggal, id_varian, jumlah_paket, total_harga, status_bayar):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO penjualan
        (tanggal, id_varian, jumlah_paket, total_harga, status_bayar)
        VALUES (?, ?, ?, ?, ?)
    """, (tanggal, id_varian, jumlah_paket, total_harga, status_bayar))

    # Jika status hutang, simpan juga ke utang_piutang
    if status_bayar == "hutang":
        cursor.execute("""
            INSERT INTO utang_piutang (tanggal, tipe, nama_pihak, jumlah, status, keterangan)
            VALUES (?, 'piutang', ?, ?, 'belum lunas', ?)
        """, (tanggal, "Pelanggan", total_harga, "dari penjualan"))

    conn.commit()
    conn.close()


def get_semua_penjualan():
    """
    Mengambil seluruh data penjualan.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_penjualan, p.tanggal, v.nama_varian,
               p.jumlah_paket, p.total_harga, p.status_bayar
        FROM penjualan p
        JOIN varian_produk v ON p.id_varian = v.id_varian
        ORDER BY p.tanggal DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def tambah_pemasukan(tanggal, sumber, jumlah, keterangan):
    """
    Menyimpan data pemasukan keuangan.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pemasukan
        (tanggal, sumber, jumlah, keterangan)
        VALUES (?, ?, ?, ?)
    """, (tanggal, sumber, jumlah, keterangan))
    conn.commit()
    conn.close()


# ======================================================
# LAPORAN
# ======================================================

def laporan_ringkas(tgl_awal, tgl_akhir):
    """
    Menghasilkan laporan ringkas pembelian, penjualan,
    laba, utang, dan piutang.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT IFNULL(SUM(total_harga), 0)
        FROM pembelian
        WHERE tanggal BETWEEN ? AND ?
    """, (tgl_awal, tgl_akhir))
    total_pembelian = cursor.fetchone()[0]

    cursor.execute("""
        SELECT IFNULL(SUM(total_harga), 0)
        FROM penjualan
        WHERE tanggal BETWEEN ? AND ?
    """, (tgl_awal, tgl_akhir))
    total_penjualan = cursor.fetchone()[0]

    cursor.execute("""
        SELECT IFNULL(SUM(jumlah), 0)
        FROM pemasukan
        WHERE tanggal BETWEEN ? AND ?
    """, (tgl_awal, tgl_akhir))
    total_pemasukan = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            SUM(CASE WHEN tipe='utang' AND status='belum lunas' THEN jumlah ELSE 0 END),
            SUM(CASE WHEN tipe='piutang' AND status='belum lunas' THEN jumlah ELSE 0 END)
        FROM utang_piutang
    """)
    utang, piutang = cursor.fetchone()
    conn.close()

    return {
        "pembelian": total_pembelian,
        "penjualan": total_penjualan,
        "pemasukan": total_pemasukan,
        "laba": total_penjualan - total_pembelian,
        "utang": utang or 0,
        "piutang": piutang or 0
    }

def hapus_pembelian(id_pembelian):
    """
    Menghapus data pembelian berdasarkan ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM pembelian WHERE id_pembelian = ?",
        (id_pembelian,)
    )
    conn.commit()
    conn.close()
def hapus_pembelian(id_pembelian):
    """
    Menghapus satu data pembelian berdasarkan ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM pembelian WHERE id_pembelian = ?",
        (id_pembelian,)
    )
    conn.commit()
    conn.close()

def hapus_penjualan(id_penjualan):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM penjualan WHERE id_penjualan = ?", (id_penjualan,))
    conn.commit()
    conn.close()

def hapus_semua_pembelian():
    """
    Menghapus seluruh data pembelian.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pembelian")
    conn.commit()
    conn.close()

def reset_semua_data():
    """
    Menghapus seluruh data pada semua tabel (reset aplikasi).
    """
    conn = get_connection()
    cursor = conn.cursor()

    tables = [
        "pembelian",
        "penjualan",
        "perhitungan_kemasan",
        "pemasukan",
        "pengeluaran",
        "utang_piutang",
        "varian_produk"
    ]

    for table in tables:
        cursor.execute(f"DELETE FROM {table}")

    conn.commit()
    conn.close()

def update_pembelian(
    id_pembelian, tanggal, jenis,
    berat_gram, jumlah, total_harga,
    status_bayar, keterangan
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pembelian
        SET tanggal = ?, jenis = ?, berat_gram = ?,
            jumlah = ?, total_harga = ?, status_bayar = ?, keterangan = ?
        WHERE id_pembelian = ?
    """, (
        tanggal, jenis, berat_gram, jumlah,
        total_harga, status_bayar, keterangan,
        id_pembelian
    ))

    conn.commit()
    conn.close()

def update_varian(id_varian, nama, berat, harga):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE varian_produk
        SET nama_varian = ?, berat_per_paket = ?, harga_jual = ?
        WHERE id_varian = ?
    """, (nama, berat, harga, id_varian))

    conn.commit()
    conn.close()

def update_penjualan(id_penjualan, jumlah_paket, status_bayar):
    conn = get_connection()
    cursor = conn.cursor()

    # Ambil harga jual varian terkait
    cursor.execute("""
        SELECT v.harga_jual
        FROM penjualan p
        JOIN varian_produk v ON p.id_varian = v.id_varian
        WHERE p.id_penjualan = ?
    """, (id_penjualan,))
    harga = cursor.fetchone()[0]

    total = harga * jumlah_paket

    cursor.execute("""
        UPDATE penjualan
        SET jumlah_paket = ?, total_harga = ?, status_bayar = ?
        WHERE id_penjualan = ?
    """, (jumlah_paket, total, status_bayar, id_penjualan))

    conn.commit()
    conn.close()



