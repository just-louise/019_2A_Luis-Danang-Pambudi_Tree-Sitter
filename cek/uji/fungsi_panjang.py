"""Contoh file uji untuk deteksi fungsi panjang (>30 baris)."""


def fungsi_pendek(x):
    return x + 1


def fungsi_sangat_panjang(data):
    hasil = []
    total = 0
    for item in data:
        if item is None:
            continue
        nilai = int(item)
        if nilai < 0:
            nilai = 0
        elif nilai > 100:
            nilai = 100
        total += nilai
        if nilai >= 90:
            grade = "A"
        elif nilai >= 80:
            grade = "B"
        elif nilai >= 70:
            grade = "C"
        elif nilai >= 60:
            grade = "D"
        else:
            grade = "E"
        ringkas = {
            "nilai": nilai,
            "grade": grade,
            "lulus": nilai >= 70,
        }
        hasil.append(ringkas)
    rata_rata = total / len(hasil) if hasil else 0
    return {
        "jumlah": len(hasil),
        "rata_rata": rata_rata,
        "detail": hasil,
    }
