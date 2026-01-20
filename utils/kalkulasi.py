import math

def hitung_paket(total_berat, berat_per_paket):
    """Hitung jumlah paket teoritis (desimal)"""
    if berat_per_paket <= 0:
        return 0
    return total_berat / berat_per_paket


def rekomendasi_kemasan(jumlah_teoritis, buffer=0):
    """Rekomendasi kemasan minimal & aman"""
    minimal = math.ceil(jumlah_teoritis)
    aman = minimal + max(0, buffer)
    return minimal, aman


def hitung_hpp(total_biaya, jumlah_paket):
    """HPP per paket"""
    if jumlah_paket <= 0:
        return 0
    return total_biaya / jumlah_paket
