import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Inisialisasi parser Python (API tree-sitter >= 0.25)
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

potongan_kode = {
    "0_dasar": b"x = 1\n",
    "1_fungsi": (
        b'def sapa(nama):\n'
        b'    return "Halo " + nama\n'
    ),
    "2_if_else": (
        b'if nilai >= 75:\n'
        b'    status = "Lulus"\n'
        b'else:\n'
        b'    status = "Ulang"\n'
    ),
    "3_kelas": (
        b"class Mahasiswa:\n"
        b"    def info(self):\n"
        b"        return self.nama\n"
    ),
}

print("=== 1. HASIL PARSE S-EXPRESSION ===")
for judul, kode in potongan_kode.items():
    tree = parser.parse(kode)
    print(f"\n[{judul}]")
    print("Kode:")
    print(kode.decode().rstrip())
    print("Pohon:")
    print(tree.root_node)

print("\n=== 2. NODE BERNAMA VS NODE ANONIM (POTONGAN FUNGSI) ===")
tree_fungsi = parser.parse(potongan_kode["1_fungsi"])
func_node = tree_fungsi.root_node.children[0]

print(f"\nchildren dari '{func_node.type}' (total {len(func_node.children)}):")
for child in func_node.children:
    status = "bernama" if child.is_named else "anonim"
    print(f"  - {child.type!r:20} -> {status}")

print(f"\nnamed_children dari '{func_node.type}' (total {len(func_node.named_children)}):")
for child in func_node.named_children:
    print(f"  - {child.type!r}")

params_node = func_node.child_by_field_name("parameters")
print(f"\nchildren dari '{params_node.type}' (total {len(params_node.children)}):")
for child in params_node.children:
    status = "bernama" if child.is_named else "anonim"
    print(f"  - {child.type!r:20} -> {status}")

print("\n=== 3. ERROR RECOVERY (SINTAKS RUSAK) ===")
kode_rusak_titik_dua = (
    b'def sapa(nama)\n'
    b'    return "Halo " + nama\n'
)
kode_rusak_kurung = (
    b'def sapa(nama:\n'
    b'    return "Halo " + nama\n'
)

for label, kode_rusak in [
    ("Tanpa ':'", kode_rusak_titik_dua),
    ("Tanpa ')'", kode_rusak_kurung),
]:
    tree_err = parser.parse(kode_rusak)
    print(f"\n[{label}] has_error={tree_err.root_node.has_error}")
    print("Kode:")
    print(kode_rusak.decode().rstrip())
    print("Pohon:")
    print(tree_err.root_node)
