// TODO: tambahkan validasi input di sisi client
function prosesPesanan(daftar) {
  let total = 0;
  for (const item of daftar) {
    if (!item) continue;
    const harga = Number(item.harga) || 0;
    const qty = Number(item.qty) || 1;
    let subtotal = harga * qty;
    if (subtotal > 100000) {
      subtotal *= 0.9;
    }
    total += subtotal;
  }
  return total;
}
