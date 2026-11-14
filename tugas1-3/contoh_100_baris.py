"""Modul contoh manajemen tiket untuk uji penjelajah node (>= 100 baris)."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Tiket:
    """Representasi satu tiket dukungan pelanggan."""

    id_tiket: int
    judul: str
    pelapor: str
    prioritas: int = 1
    status: str = "open"
    label: List[str] = field(default_factory=list)
    dibuat_pada: str = field(default_factory=lambda: datetime.now().isoformat())

    def tutup(self, catatan: Optional[str] = None) -> None:
        """Menandai tiket sebagai selesai."""
        self.status = "closed"
        if catatan:
            self.label.append(f"catatan:{catatan}")

    def eskalasi(self) -> int:
        """Menaikkan prioritas tiket hingga batas maksimum 5."""
        if self.prioritas < 5:
            self.prioritas += 1
        return self.prioritas


class AntreanTiket:
    """Pengelola daftar tiket berdasarkan prioritas dan status."""

    def __init__(self) -> None:
        self._daftar: Dict[int, Tiket] = {}
        self._urutan_id: int = 1

    def tambah(self, judul: str, pelapor: str, prioritas: int = 1) -> Tiket:
        """Membuat dan menyimpan tiket baru."""
        if not judul.strip():
            raise ValueError("Judul tiket tidak boleh kosong")
        if prioritas < 1 or prioritas > 5:
            raise ValueError("Prioritas harus antara 1 sampai 5")

        tiket = Tiket(
            id_tiket=self._urutan_id,
            judul=judul.strip(),
            pelapor=pelapor.strip(),
            prioritas=prioritas,
        )
        self._daftar[tiket.id_tiket] = tiket
        self._urutan_id += 1
        return tiket

    def ambil(self, id_tiket: int) -> Optional[Tiket]:
        """Mengambil tiket berdasarkan ID."""
        return self._daftar.get(id_tiket)

    def saring(self, status: Optional[str] = None, min_prioritas: int = 1) -> List[Tiket]:
        """Menyaring tiket berdasarkan status dan prioritas minimum."""
        hasil: List[Tiket] = []
        for tiket in self._daftar.values():
            if status is not None and tiket.status != status:
                continue
            if tiket.prioritas < min_prioritas:
                continue
            hasil.append(tiket)
        return sorted(hasil, key=lambda t: (-t.prioritas, t.id_tiket))

    def ringkasan(self) -> Dict[str, int]:
        """Menghitung jumlah tiket per status."""
        hitung: Dict[str, int] = {"open": 0, "closed": 0}
        for tiket in self._daftar.values():
            hitung[tiket.status] = hitung.get(tiket.status, 0) + 1
        return hitung


def buat_data_awal() -> AntreanTiket:
    """Membuat antrean contoh untuk pengujian."""
    antrean = AntreanTiket()
    antrean.tambah("Gagal login SSO", "andi", prioritas=4)
    antrean.tambah("Lampiran PDF tidak muncul", "budi", prioritas=2)
    t3 = antrean.tambah("Timeout pada laporan bulanan", "citra", prioritas=5)
    t3.eskalasi()
    return antrean


def cetak_laporan(antrean: AntreanTiket) -> None:
    """Mencetak daftar tiket aktif ke terminal."""
    print("=== RINGKASAN TIKET ===")
    for status, total in antrean.ringkasan().items():
        print(f"- {status}: {total}")

    print("\n=== TIKET PRIORITAS TINGGI ===")
    for tiket in antrean.saring(status="open", min_prioritas=3):
        print(f"#{tiket.id_tiket} [{tiket.prioritas}] {tiket.judul} ({tiket.pelapor})")


if __name__ == "__main__":
    sistem = buat_data_awal()
    cetak_laporan(sistem)
