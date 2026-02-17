# LAPORAN PROYEK  
# Sistem Manajemen Inventaris dan Prediksi Permintaan Berbasis Web

---

# Latar Belakang

Manajemen inventaris merupakan bagian penting dalam operasional bisnis, khususnya bagi usaha kecil dan menengah. Pengelolaan stok yang tidak efektif dapat menyebabkan dua masalah utama, yaitu kehabisan stok (stockout) yang mengakibatkan kehilangan potensi penjualan, dan kelebihan stok (overstock) yang menyebabkan pemborosan sumber daya dan biaya penyimpanan.

Banyak usaha kecil masih menggunakan metode manual atau spreadsheet sederhana untuk mencatat inventaris dan penjualan. Metode ini memiliki keterbatasan, terutama dalam hal otomatisasi, analisis data historis, dan kemampuan prediksi kebutuhan stok di masa depan.

Berdasarkan permasalahan tersebut, proyek ini dikembangkan untuk membangun sistem manajemen inventaris berbasis web dengan kemampuan pencatatan transaksi, pengelolaan stok otomatis, analisis data penjualan, serta prediksi permintaan menggunakan metode moving average.

---

# Tujuan Akhir dan Proyek

Tujuan utama proyek ini adalah mengembangkan sistem backend berbasis RESTful API yang mampu mengelola inventaris dan memberikan analisis serta prediksi permintaan secara otomatis.

Secara spesifik, tujuan proyek ini meliputi:

- Mengembangkan sistem untuk mengelola produk, inventaris, dan transaksi penjualan
- Mengimplementasikan autentikasi pengguna menggunakan JWT (JSON Web Token)
- Memastikan setiap pengguna memiliki data yang terisolasi dan aman
- Mengimplementasikan analisis data penjualan menggunakan Pandas
- Mengimplementasikan metode prediksi permintaan menggunakan Moving Average
- Menyediakan rekomendasi jumlah stok yang perlu ditambahkan berdasarkan hasil prediksi
- Mengembangkan arsitektur sistem yang modular dan mudah dikembangkan lebih lanjut

Proyek ini difokuskan pada pengembangan backend sebagai fondasi sistem yang kuat dan scalable.

---

# Area dan Kompetensi

Proyek ini mengintegrasikan berbagai kompetensi teknis dalam pengembangan perangkat lunak backend dan analisis data.

## Backend Development

- Pengembangan RESTful API menggunakan Flask
- Desain endpoint yang terstruktur dan konsisten
- Penggunaan Blueprint untuk modularisasi kode
- Implementasi validasi input dan error handling

## Database Management

- Perancangan database relasional menggunakan SQLite
- Penggunaan SQLAlchemy sebagai Object Relational Mapper (ORM)
- Implementasi relasi antar tabel (User, Product, Inventory, Sale, Forecast)
- Isolasi data berdasarkan pengguna

## Authentication dan Security

- Implementasi sistem registrasi dan login pengguna
- Penggunaan JWT untuk autentikasi berbasis token
- Proteksi endpoint menggunakan decorator
- Hashing password menggunakan Werkzeug

## Data Processing dan Analytics

- Penggunaan Pandas untuk analisis data penjualan
- Perhitungan agregasi penjualan
- Identifikasi pola penjualan historis

## Forecasting dan Decision Support

- Implementasi metode Moving Average untuk prediksi permintaan
- Pengembangan beberapa metode forecasting tambahan untuk eksperimen dan perbandingan
- Pembuatan rekomendasi reorder berdasarkan hasil prediksi dan stok saat ini

## Kompetensi SMM

 - Berkomitmen, Mandiri.
- Berwawasan, Berpikir Kritis, Inovatif
- Berprinsip

---

# Proses dan Dokumentasi

Pengembangan proyek dilakukan secara bertahap dengan pendekatan modular dan incremental.

## Tahap 1 – Perancangan Sistem

Pada tahap ini dilakukan perancangan arsitektur sistem dan database. Struktur database dirancang dengan tabel utama berikut:

- User
- Product
- Inventory
- Sale
- Forecast

Relasi antar tabel dirancang untuk memastikan integritas data dan isolasi data antar pengguna.

## Tahap 2 – Implementasi Fitur Inti

Tahap ini mencakup implementasi fitur dasar sistem, yaitu:

- CRUD produk
- Pencatatan inventaris
- Pencatatan transaksi penjualan
- Pengurangan stok otomatis saat terjadi penjualan
- Validasi untuk mencegah stok menjadi negatif

## Tahap 3 – Implementasi RESTful API

Sistem dikembangkan menggunakan arsitektur RESTful API dengan endpoint untuk:

- Manajemen pengguna (register dan login)
- Manajemen produk
- Manajemen inventaris
- Manajemen transaksi penjualan
- Akses data forecasting

Setiap endpoint dirancang sesuai dengan standar HTTP method seperti GET, POST, PUT, dan DELETE.

## Tahap 4 – Implementasi Authentication

Authentication diimplementasikan menggunakan JWT, dengan fitur:

- Registrasi pengguna baru
- Login pengguna
- Pembuatan access token
- Proteksi endpoint menggunakan JWT decorator
- Isolasi data berdasarkan user identity

## Tahap 5 – Implementasi Analisis dan Forecasting

Pada tahap ini, sistem analisis data dikembangkan menggunakan Pandas untuk memproses data penjualan historis.

Metode Moving Average digunakan untuk memprediksi permintaan masa depan. Selain itu, beberapa metode forecasting tambahan juga diimplementasikan untuk eksplorasi dan pengembangan lebih lanjut.

Hasil prediksi digunakan untuk memberikan rekomendasi jumlah stok yang perlu ditambahkan.

## Tahap 6 – Finalisasi dan Dokumentasi

Tahap akhir mencakup:

- Refactoring dan pembersihan kode
- Penambahan validasi input
- Penanganan error
- Dokumentasi endpoint API
- Dokumentasi arsitektur sistem

---

# Evaluasi dan Refleksi

## Kelebihan Sistem

- Arsitektur modular dan terstruktur dengan baik
- Implementasi autentikasi berbasis JWT yang aman
- Isolasi data antar pengguna
- Integrasi analisis data dan forecasting
- Pemisahan yang jelas antara layer database, logic, dan API

## Tantangan yang Dihadapi

Beberapa tantangan utama selama pengembangan proyek ini meliputi:

- Mendesain struktur database yang fleksibel dan konsisten
- Mengimplementasikan autentikasi berbasis token
- Mengintegrasikan analisis Pandas ke dalam sistem backend
- Mengembangkan sistem forecasting yang dapat digunakan dalam konteks inventaris

## Pembelajaran yang Diperoleh

Melalui proyek ini, diperoleh pemahaman mendalam mengenai:

- Pengembangan RESTful API secara end-to-end
- Perancangan database relasional
- Implementasi autentikasi dan keamanan backend
- Pengolahan dan analisis data menggunakan Pandas
- Pengembangan sistem backend yang modular dan scalable

Proyek ini juga meningkatkan pemahaman mengenai bagaimana sistem backend digunakan dalam aplikasi nyata.

---

# Kesimpulan

Proyek ini berhasil mengembangkan sistem manajemen inventaris berbasis web dengan kemampuan autentikasi pengguna, pengelolaan inventaris, pencatatan transaksi penjualan, analisis data, dan prediksi permintaan menggunakan metode Moving Average.

Sistem yang dikembangkan memiliki arsitektur yang modular, aman, dan siap untuk dikembangkan lebih lanjut, termasuk penambahan frontend, deployment ke server produksi, dan integrasi metode forecasting yang lebih kompleks.

Proyek ini memberikan pengalaman praktis dalam pengembangan backend modern dan menunjukkan kemampuan dalam mengintegrasikan database, API, autentikasi, dan analisis data dalam satu sistem yang lengkap.

---

# Status Proyek Saat Ini

- Deployment: Belum dilakukan
- Database: SQLite
- Authentication: JWT
- Forecasting Method: Moving Average dan metode tambahan
- Multi-user support: Ya (data terpisah per user)
- Role system: Belum diimplementasikan
- Performance measurement: Belum dilakukan

---

