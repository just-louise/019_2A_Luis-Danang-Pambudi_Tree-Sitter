"""CLI pendeteksi TODO/FIXME, fungsi panjang (>30 baris), dan error sintaks.

Mendukung file Python (.py) dan JavaScript (.js) menggunakan Tree-sitter.
"""

import sys
from pathlib import Path

import tree_sitter_javascript as tsjavascript
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

BATAS_BARIS_FUNGSI = 30
FOLDER_DILEWATI = {".git", "venv", ".venv", "node_modules", "__pycache__", "build"}

PY_LANG = Language(tspython.language())
JS_LANG = Language(tsjavascript.language())

CONFIG_BAHASA = {
    ".py": {
        "parser": Parser(PY_LANG),
        "q_todo": Query(PY_LANG, '((comment) @c (#match? @c "TODO|FIXME"))'),
        "q_fungsi": Query(
            PY_LANG,
            "(function_definition name: (identifier) @nama) @fungsi",
        ),
    },
    ".js": {
        "parser": Parser(JS_LANG),
        "q_todo": Query(JS_LANG, '((comment) @c (#match? @c "TODO|FIXME"))'),
        "q_fungsi": Query(
            JS_LANG,
            """
            (function_declaration name: (identifier) @nama) @fungsi
            (method_definition name: (property_identifier) @nama) @fungsi
            """,
        ),
    },
}


def cari_error_pertama(node):
    """Cari node ERROR/MISSING paling spesifik pertama secara rekursif (DFS)."""
    for child in node.children:
        if child.has_error or child.is_error or child.is_missing:
            hasil = cari_error_pertama(child)
            if hasil is not None:
                return hasil
    if node.is_error or node.is_missing:
        return node
    return None


def cek_file(path: Path, cfg: dict) -> dict:
    """Jalankan ketiga pemeriksaan pada satu file dan kembalikan ringkasan."""
    tree = cfg["parser"].parse(path.read_bytes())
    root = tree.root_node

    temuan = {"todo": 0, "fungsi_panjang": 0, "error": 0}

    # Fitur 1: komentar TODO / FIXME
    for node in QueryCursor(cfg["q_todo"]).captures(root).get("c", []):
        baris = node.start_point[0] + 1
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO] {path}:{baris}: {teks}")
        temuan["todo"] += 1

    # Fitur 2: fungsi lebih dari BATAS_BARIS_FUNGSI baris
    for _, cap in QueryCursor(cfg["q_fungsi"]).matches(root):
        fungsi_node = cap["fungsi"][0]
        nama_node = cap["nama"][0]
        jumlah_baris = fungsi_node.end_point[0] - fungsi_node.start_point[0] + 1
        if jumlah_baris > BATAS_BARIS_FUNGSI:
            baris = fungsi_node.start_point[0] + 1
            nama = nama_node.text.decode(errors="replace")
            print(f"[LONG] {path}:{baris}: fungsi '{nama}' ({jumlah_baris} baris)")
            temuan["fungsi_panjang"] += 1

    # Fitur 3: file dengan error sintaks
    if root.has_error:
        err_node = cari_error_pertama(root)
        if err_node is not None:
            baris = err_node.start_point[0] + 1
            kolom = err_node.start_point[1]
            jenis = "MISSING" if err_node.is_missing else "ERROR"
            print(f"[ERR ] {path}:{baris}:{kolom}: sintaks {jenis} ({err_node.type})")
        else:
            print(f"[ERR ] {path}: pohon mengandung error sintaks")
        temuan["error"] += 1

    return temuan


def harus_dilewati(path: Path) -> bool:
    return any(bagian in FOLDER_DILEWATI for bagian in path.parts)


def main():
    if len(sys.argv) < 2:
        print("Pemakaian: python cek.py <folder>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Folder tidak ditemukan: {target}")
        sys.exit(1)

    total_file = 0
    total = {"todo": 0, "fungsi_panjang": 0, "error": 0}

    daftar_file = [target] if target.is_file() else sorted(target.rglob("*"))
    for path in daftar_file:
        if not path.is_file() or harus_dilewati(path):
            continue
        cfg = CONFIG_BAHASA.get(path.suffix.lower())
        if cfg is None:
            continue
        total_file += 1
        hasil = cek_file(path, cfg)
        for k in total:
            total[k] += hasil[k]

    print(
        f"\nRingkasan ({total_file} file diperiksa): "
        f"{total['todo']} TODO/FIXME, "
        f"{total['fungsi_panjang']} fungsi >{BATAS_BARIS_FUNGSI} baris, "
        f"{total['error']} file error."
    )


if __name__ == "__main__":
    main()
