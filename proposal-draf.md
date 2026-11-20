# Draf Proposal Proyek Tree-sitter

### 1. Judul
**ExpressGuard: Pemeriksa Otomatis Kebocoran Data Sensitif di Log dan Larangan `console.log` pada Backend Express.js Berbasis Tree-sitter**

### 2. Masalah
Pada pengembangan aplikasi web enterprise berbasis Node.js/Express.js dengan banyak developer, dua kesalahan sering lolos saat code review: (1) pemanggilan `console.log(...)` bekas debugging tertinggal di kode produksi, dan (2) field sensitif seperti `password`, `token`, atau `secret` tercetak ke log melalui `logger.info(user.password)` atau `console.error(req.headers.authorization)`. Masalah ini dialami oleh tim backend developer, code reviewer, dan tim keamanan (AppSec) karena berisiko membocorkan kredensial pelanggan ke sistem agregasi log.

### 3. Kenapa Tidak Cukup dengan AI Saja
Meminta AI coding agent me-review setiap pull request bersifat probabilistik (hasil bisa berubah antar-eksekusi), memakan biaya token per file, dan lambat jika dijalankan pada repositori enterprise berisi ribuan file. Sebaliknya, tool berbasis Tree-sitter bersifat **deterministik** (hasil selalu konsisten), berbiaya hampir nol, berjalan dalam milidetik di pipeline CI/CD pada setiap commit, dan memahami struktur sintaks—berbeda dengan `grep`/regex yang mudah tertipu oleh komentar atau literal string.

### 4. Bahasa, Framework Target, dan Grammar
- **Bahasa & Framework:** JavaScript / Node.js (Express.js).
- **Grammar Tree-sitter:** `tree-sitter-javascript` (tersedia resmi di PyPI).

### 5. Contoh Kode

**Harus terdeteksi:**
```javascript
console.log("debug user:", req.body);          // aturan 1: console.log di produksi
logger.info("login gagal", user.password);     // aturan 2: properti sensitif di log
```

**Tidak boleh terdeteksi (regex biasa sering salah tangkap):**
```javascript
// console.log("hanya contoh di komentar")
const pesan = "Jangan pakai console.log atau user.password di log";
logger.info("login berhasil", user.id);        // bukan properti sensitif
```

### 6. Rancangan Query (S-Expression)
Query untuk mendeteksi pemanggilan `console.log(...)` (mengabaikan komentar dan string secara otomatis karena hanya mencocokkan node `call_expression`):

```scheme
(call_expression
  function: (member_expression
    object: (identifier) @obj
    property: (property_identifier) @prop)
  arguments: (arguments) @args
  (#eq? @obj "console")
  (#eq? @prop "log")) @temuan
```

### 7. Bentuk Output
Laporan terstruktur di terminal (`[RULE] file:baris:kolom — pesan`) beserta opsi ekspor `--json` agar mudah dibaca oleh pipeline CI (GitHub Actions) dan mengembalikan exit code non-zero bila ditemukan pelanggaran.

### 8. Cara Evaluasi
Tool akan diuji pada repositori backend Express.js open source (misalnya *realworld-express* atau proyek backend kuliah). Evaluasi dilakukan dengan memeriksa manual minimal **20 temuan** untuk menghitung jumlah *true positive* dan *false positive*, serta menambahkan unit test khusus kasus tepi (komentar, string, destructuring).

### 9. Rencana Kerja & Risiko
- **Minggu 1:** Finalisasi spesifikasi 3 aturan (`console.log`, field sensitif di `logger.*`, dan route handler `async` tanpa `try/catch`) serta koleksi file uji.
- **Minggu 2:** Implementasi parser & query S-expression untuk aturan 1 dan 2.
- **Minggu 3:** Implementasi aturan 3, filter direktori (`node_modules/`), dan output JSON.
- **Minggu 4:** Pengujian pada repositori Express.js nyata dan evaluasi manual 20 temuan.
- **Minggu 5:** Perbaikan *false positive*, dokumentasi `README.md`, dan finalisasi laporan/demo.
- **Risiko utama:** Pemanggilan logger lewat alias variabel (misal `const log = console.log`) tidak terdeteksi oleh analisis sintaks murni; dimitigasi dengan mendokumentasikan batasan skop secara jelas.
