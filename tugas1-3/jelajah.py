import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah(node, kedalaman=0, field=None):
    """Telusuri pohon sintaks secara rekursif dan cetak node bernama."""
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    for i, child in enumerate(node.children):
        if not child.is_named:
            continue
        jelajah(child, kedalaman + 1, node.field_name_for_child(i))


def jelajah_cursor(tree):
    """Telusuri pohon sintaks memakai TreeCursor (lebih hemat memori)."""
    cursor = tree.walk()
    kedalaman = 0
    kembali_dari_child = False

    while True:
        node = cursor.node
        if not kembali_dari_child:
            if node.is_named:
                baris, kolom = node.start_point
                field = cursor.field_name
                label = f"{field}: " if field else ""
                print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
            if cursor.goto_first_child():
                if node.is_named:
                    kedalaman += 1
                continue

        if cursor.goto_next_sibling():
            kembali_dari_child = False
            continue

        if cursor.goto_parent():
            if cursor.node.is_named:
                kedalaman -= 1
            kembali_dari_child = True
        else:
            break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Pemakaian: python jelajah.py <file.py> [--cursor]")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        tree = parser.parse(f.read())

    if "--cursor" in sys.argv[2:]:
        jelajah_cursor(tree)
    else:
        jelajah(tree.root_node)
