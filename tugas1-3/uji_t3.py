import os
import json as js
from pathlib import Path
from datetime import datetime, timezone


def sapa(nama):
    """Mengembalikan pesan sapaan."""
    pesan = f"Halo, {nama}"
    print(pesan)
    return pesan


def tambah(a, b, c=0):
    "Menjumlahkan dua atau tiga angka."
    return a + b + c


def tanpa_docstring():
    x = 10
    print("nilai:", x)
    return x


if __name__ == "__main__":
    sapa("Budi")
    print(tambah(1, 2, 3))
