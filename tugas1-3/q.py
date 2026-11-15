import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)


def main():
    if len(sys.argv) < 3:
        print("Pemakaian: python q.py <file.py> <pola.scm> [--matches]")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        kode = f.read()
    with open(sys.argv[2], "r", encoding="utf-8") as f:
        pola = f.read()

    tree = parser.parse(kode)
    query = Query(PY, pola)
    cursor = QueryCursor(query)

    if "--matches" in sys.argv[3:]:
        for _, cap in cursor.matches(tree.root_node):
            if "nama" in cap and "params" in cap:
                nama = cap["nama"][0].text.decode()
                jumlah = cap["params"][0].named_child_count
                baris = cap["nama"][0].start_point[0] + 1
                print(f"baris {baris}: {nama} (parameter: {jumlah})")
            else:
                bagian = []
                for k, nodes in cap.items():
                    for n in nodes:
                        bagian.append(f"@{k}={n.text.decode().strip()}")
                print(", ".join(bagian))
    else:
        hasil = cursor.captures(tree.root_node)
        for nama, nodes in hasil.items():
            for n in nodes:
                print(f"@{nama}  baris {n.start_point[0] + 1}: {n.text.decode().strip()}")


if __name__ == "__main__":
    main()
