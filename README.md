EXE TOOLS - README

EXE Tools adalah sebuah simulasi framework buatan lokal Indonesia yang ditujukan untuk edukasi dan pembelajaran dasar keamanan siber.

⚠️ Peringatan: Tools ini bukan untuk digunakan dalam aktivitas ilegal. Segala penyalahgunaan di luar tujuan edukatif bukan tanggung jawab pembuat.

---
📦 Fitur Utama
1. Simulasi Serangan DDoS (Web Flood Request)
Menampilkan cara kerja flood request berbasis HTTP dengan visualisasi RPS (Requests per Second). Untuk pembelajaran saja.

2. Scanner Website 🔍
Mendeteksi:
DNS Record
Informasi WHOIS
Server & Header Response
Deteksi CMS umum: WordPress, Joomla, Drupal
Panel Admin
Subdomain umum
3. Animasi Loading Terminal
Matrix Rain
Proses pemasangan tool (progress bar dinamis)
4. Login Sistem dengan 3 percobaan akses.
5. Menu Interaktif dengan tampilan terminal khas EXE.

---
🔐 Username X 
Password EXE
---
✅ Yang Harus Diinstall
💡 Langsung install dengan:
<div>
  <pre><code id="install">pip install colorama requests python-whois dnspython</code></pre>
  <button onclick="copyText('install')">📋 Salin Perintah</button>
</div>🧾 Atau buat requirements.txt:

<div>
  <pre><code id="reqs">colorama
requests
python-whois
dnspython</code></pre>
  <button onclick="copyText('reqs')">📋 Salin Isi</button>
</div>Lalu jalankan:

---
🛠 Instalasi & Menjalankan
<div>
  <pre><code id="run">
git clone https://github.com/Pandagz25/Ddos.git
cd Ddos
python main.py
  </code></pre>
  <button onclick="copyText('run')">📋 Salin Perintah</button>
</div>

---
🧪 Penggunaan
Masukkan username & password saat login
Pilih menu:
Info EXE
Simulasi DDoS (educational only)
Cek Info Website

---
🤖 Author
Creator: X
Version: 2.0 EXE RILIS INDONESIA
Status: Aktif dan Terproteksi

---
❗ Disclaimer
Tools ini hanya untuk edukasi, simulasi, dan pembelajaran. Jangan digunakan pada target yang tidak memiliki izin. Selalu praktikkan etika digital.

---
📸 Preview
╔══════════════════════════════════════════════╗
║ ███████╗██╗  ██╗███████╗  ███████╗██╗  ██╗ ║
║ ██╔════╝╚██╗██╔╝██╔════╝  ╚════██║╚██╗██╔╝ ║
║ █████╗   ╚███╔╝ █████╗      ███╔═╝ ╚███╔╝  ║
║ ██╔══╝   ██╔██╗ ██╔══╝     ██╔══╝  ██╔██╗  ║
║ ███████╗██╔╝ ██╗███████╗  ███████╗██╔╝ ██╗ ║
║ ╚══════╝╚═╝  ╚═╝╚══════╝  ╚══════╝╚═╝  ╚═╝ ║
╚══════════════════════════════════════════════╝

---
<script>
function copyText(id) {
  const el = document.getElementById(id);
  navigator.clipboard.writeText(el.textContent);
  alert("✅ Teks berhasil disalin!");
}
</script>Selamat belajar & eksplorasi keamanan dunia maya! 💻
