# `cek.py` — Pendeteksi TODO/FIXME, Fungsi Panjang, dan Error Sintaks

CLI kecil berbasis Tree-sitter untuk memeriksa folder kode Python (`.py`) dan JavaScript (`.js`).

## Fitur

1. **Deteksi `TODO` / `FIXME`** — mencari komentar yang mengandung kata `TODO` atau `FIXME` menggunakan query Tree-sitter dan predikat `#match?`.
2. **Deteksi Fungsi Panjang (> 30 baris)** — menghitung panjang definisi fungsi berdasarkan `end_point[0] - start_point[0] + 1`. Semua fungsi dihitung, termasuk method di dalam kelas dan fungsi bersarang.
3. **Deteksi Error Sintaks** — memeriksa `tree.root_node.has_error` dan melaporkan posisi (`baris:kolom`) node `ERROR` / `MISSING` paling spesifik pertama.
4. **Dukungan JavaScript (Pengayaan)** — otomatis memeriksa file `.js` menggunakan `tree-sitter-javascript`.

Folder `venv/`, `.venv/`, `.git/`, `node_modules/`, `__pycache__/`, dan `build/` dilewati secara otomatis.

## Instalasi Dependensi

```bash
pip install tree-sitter tree-sitter-python tree-sitter-javascript
```

## Cara Menjalankan

```bash
python cek/cek.py <folder_atau_file>
```

Contoh pada folder uji lokal:

```bash
python cek/cek.py cek/uji
```

## Contoh Output

### 1. Pada Folder `cek/uji/`

```text
[TODO] cek\uji\contoh.js:1: // TODO: tambahkan validasi input di sisi client
[LONG] cek\uji\fungsi_panjang.py:8: fungsi 'fungsi_sangat_panjang' (34 baris)
[ERR ] cek\uji\sintaks_rusak.py:4:0: sintaks ERROR (ERROR)
[TODO] cek\uji\todo_contoh.py:5: # TODO: validasi agar persen tidak lebih dari 100
[TODO] cek\uji\todo_contoh.py:7: # FIXME: tangani kasus harga negatif

Ringkasan (4 file diperiksa): 3 TODO/FIXME, 1 fungsi >30 baris, 1 file error.
```

### 2. Pada Repositori Nyata (`pallets/itsdangerous`)

```text
[LONG] repo-uji\itsdangerous\src\itsdangerous\serializer.py:190: fungsi '__init__' (45 baris)
[LONG] repo-uji\itsdangerous\src\itsdangerous\signer.py:129: fungsi '__init__' (45 baris)
[LONG] repo-uji\itsdangerous\src\itsdangerous\signer.py:182: fungsi 'derive_key' (32 baris)
[TODO] repo-uji\itsdangerous\src\itsdangerous\timed.py:182: # TODO: Signature is incompatible because parameters were added
[LONG] repo-uji\itsdangerous\src\itsdangerous\timed.py:72: fungsi 'unsign' (87 baris)
[LONG] repo-uji\itsdangerous\src\itsdangerous\timed.py:185: fungsi 'loads' (36 baris)
[LONG] repo-uji\itsdangerous\src\itsdangerous\url_safe.py:23: fungsi 'load_payload' (31 baris)

Ringkasan (15 file diperiksa): 1 TODO/FIXME, 6 fungsi >30 baris, 0 file error.
```

Verifikasi manual pada 2 file (`url_safe.py` dan `timed.py`):
- `url_safe.py`: `load_payload` dimulai baris 23 dan berakhir baris 53 ($53 - 23 + 1 = 31$ baris) — cocok.
- `timed.py`: komentar `# TODO` tepat di baris 182, dan `loads` dimulai baris 185 sampai baris 220 ($220 - 185 + 1 = 36$ baris) — cocok.
