# 🎨 Panduan Desain UI/UX: Aplikasi Forensik Digital & Deteksi Deepfake

Dokumen ini berisi panduan perancangan antarmuka (Mockup Guidelines) untuk proyek aplikasi forensik digital berbasis web. Desain ini dirancang dengan pendekatan **Profesional, Terpercaya (Trustworthy), Aman (Secure), dan High-Tech (Analytical)**.

---

## 1. User Flow Utama (Main User Flow)
Fokus pada kelancaran pengguna dari awal hingga mendapatkan hasil analisis tanpa hambatan (frictionless).

1. **Start:** Pengguna masuk ke Halaman Utama (Homepage).
2. **Action:** Pengguna melihat area *Drag & Drop* dan mengunggah file (Video/Audio).
3. **Validation:** Sistem secara instan memvalidasi format (MP4, WAV, dll) dan ukuran file (< 500MB).
   - *Jika gagal:* Muncul pesan *Error Toast*.
   - *Jika sukses:* File masuk ke antrean tampilan (UI menampilkan nama & ukuran file).
4. **Trigger:** Pengguna menekan tombol **"Start Analysis"**.
5. **Processing State:** Pengguna dialihkan ke state *Loading* dengan animasi pemindaian (scanning) yang informatif (misal: "Extracting metadata...", "Running AI Model...").
6. **Result:** Pengguna tiba di Halaman Laporan (Report Page) yang menampilkan *Verdict* (Asli/Palsu) secara mencolok, diikuti detail teknis di bawahnya.
7. **End/Loop:** Pengguna dapat menekan tombol "Download PDF Report" atau "Analyze Another File".

---

## 2. Daftar Halaman & State (Screen List)
Berikut adalah daftar halaman dan state interaktif yang perlu dibuat:

* **Screen 1: Landing / Upload Dashboard (`index.html`)** - Halaman utama untuk memasukkan file.
* **Screen 2: Analysis Processing (State)** - State interaktif saat model AI dan ekstraksi di backend sedang bekerja (mencegah pengguna menutup tab).
* **Screen 3: Analysis Report (`result.html`)** - Halaman hasil detail forensik.
* **Modal / Overlays:**
  - *Error/Alert Modal* (misal: File terlalu besar, format tidak didukung).
  - *Info Tooltip* (Penjelasan istilah forensik saat icon tanda tanya `(?)` di-hover).

---

## 3. Anatomi & Komponen per Halaman

### A. Landing / Upload Dashboard (`index.html`)
* **Top Navigation Bar:** Logo aplikasi (kiri), Link dokumentasi/tentang (kanan).
* **Hero Section:**
  - *Heading:* Singkat dan jelas (contoh: "Verify Media Authenticity with AI").
  - *Sub-heading:* Penjelasan singkat (contoh: "Upload audio or video to detect deepfakes, manipulations, and hidden metadata.")
* **Upload Component (Fokus Utama):**
  - Kotak besar bergaya *Dash border* (garis putus-putus) dengan efek *hover*.
  - Ikon Cloud/Upload besar di tengah.
  - Teks instruksi: "Drag & drop your file here or Browse".
  - Teks bantuan (microcopy): "Supported formats: MP4, AVI, WAV, MP3. Max: 500MB".
* **Uploaded File Card (Muncul setelah file dipilih):**
  - Ikon format file (🎵 atau 🎬).
  - Nama file & Ukuran file.
  - Tombol ikon `X` untuk membatalkan (Remove).
* **CTA Button:** Tombol utama **"Analyze Media"** yang hanya aktif (*enabled*) setelah file diunggah.

### B. Processing State
* **Visual Animation:** Animasi *radar scanning* atau *progress bar* melingkar.
* **Dynamic Text:** Teks yang berubah setiap beberapa detik untuk memberi tahu backend sedang bekerja:
  1. *Uploading securely...*
  2. *Extracting EXIF & Metadata...*
  3. *Running Deepfake Neural Network...*
  4. *Finalizing report...*

### C. Analysis Report (`result.html`)
* **Top Header:** Tombol "⬅ Back to Home", Nama File Asli, dan UUID Analisis (sebagai nomor referensi/ID Laporan).
* **The Verdict Card (Hero Komponen Halaman Ini):**
  - Skor Keaslian (Misal: 98% Authentic atau 85% Fake).
  - Badge Status besar: **✅ AUTHENTIC**, **⚠️ SUSPICIOUS**, atau **🚨 MANIPULATED**.
* **Content Area (Menggunakan sistem *Tabs* untuk merapikan informasi):**
  - **Tab 1: Overview:** Ringkasan visual (Thumbnail video/waveform audio), resolusi/durasi, dan kesimpulan singkat model AI.
  - **Tab 2: Metadata:** Tabel berisi data mentah dari metadata (Creation date, Codec, Bitrate, Software pengedit yang terdeteksi).
  - **Tab 3: AI Analysis:** Menampilkan output dari analisis AI (Misal: Grafik anomali frekuensi, deteksi inkonsistensi frame wajah).
* **Action Footer:**
  - Tombol sekunder (Outline): "Analyze Another File".
  - Tombol primer (Solid): "Download Full Report (PDF)".

---

## 4. Mini Design System

Untuk platform forensik dan keamanan, **Dark Mode (Mode Gelap)** sangat direkomendasikan. Ini mengurangi ketegangan mata, memberi kontras tinggi pada data, dan memancarkan aura teknologi canggih.

### 🎨 Color Palette (Dark Forensic Theme)
* **Background (Base):** `#0F172A` (Slate 900) - Warna dasar yang dalam, memberikan fokus.
* **Surface / Cards:** `#1E293B` (Slate 800) - Untuk latar kotak/kartu informasi agar menonjol dari *background*.
* **Primary / Brand:** `#3B82F6` (Blue 500) - Mewakili kepercayaan, kecerdasan buatan, dan teknologi. Digunakan untuk tombol utama dan *tab aktif*.
* **Text (High Emphasis):** `#F8FAFC` (Slate 50) - Untuk Heading dan teks utama (Putih pudar agar tidak terlalu silau).
* **Text (Secondary/Microcopy):** `#94A3B8` (Slate 400) - Untuk deskripsi dan label.

**Semantic Colors (Sangat krusial untuk aplikasi ini):**
* **Success (Authentic):** `#10B981` (Emerald) - Mengindikasikan aman / asli.
* **Warning (Suspicious):** `#F59E0B` (Amber) - Mengindikasikan adanya anomali.
* **Danger (Fake/Manipulated):** `#EF4444` (Red 500) - Tanda bahaya/manipulasi terdeteksi.

### 🔤 Typography Pairing
* **Heading Font:** **Plus Jakarta Sans** atau **Inter**
  - *Karakter:* Geometris, bersih, profesional. Sangat modern untuk antarmuka tech/AI.
* **Body Text Font:** **Inter** atau **Roboto**
  - *Karakter:* Keterbacaan (legibility) tingkat tinggi untuk membaca paragraf dan tabel data.
* **Monospace Font (Khusus Data Teknis):** **JetBrains Mono** atau **Fira Code**
  - *Penggunaan:* Hanya digunakan untuk menampilkan nilai Metadata (seperti UUID, Hash SHA-256, ukuran Byte) agar terlihat seperti *code/log* asli.

### 📐 Visual Style & UI Element
* **Borders:** Gunakan garis tepi tipis (`1px solid #334155`) untuk memisahkan data di dalam tabel agar terlihat seperti *dashboard* analitik.
* **Corners (Border-radius):** Sedang (`8px` atau `12px`). 8px adalah *sweet spot* untuk gaya modern-profesional.
* **Shadows / Glow:** Karena ini dark mode, hindari shadow hitam (drop shadow). Gunakan efek *Glow* (bayangan berwarna redup) khusus pada tombol Primary dan indikator Verdict (misal: *glow* merah tipis jika statusnya Fake).
