"""Contoh file uji dengan komentar TODO dan FIXME."""


def hitung_diskon(harga, persen):
    # TODO: validasi agar persen tidak lebih dari 100
    potongan = harga * (persen / 100)
    # FIXME: tangani kasus harga negatif
    return harga - potongan
