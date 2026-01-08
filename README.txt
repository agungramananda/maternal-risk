================================================================================
                  LAPORAN PROYEK KLASIFIKASI RISIKO KESEHATAN MATERNAL
================================================================================

INFORMASI PROYEK
--------------------------------------------------------------------------------
Nama Proyek     : Sistem Klasifikasi Risiko Kesehatan Maternal
Deskripsi       : Aplikasi berbasis web untuk mengklasifikasikan tingkat 
                  risiko kesehatan ibu hamil menggunakan algoritma Machine 
                  Learning (Decision Tree dan Random Forest)
Teknologi       : Python, Streamlit, PostgreSQL, Docker
Tanggal         : Desember 2025


TUJUAN PROYEK
--------------------------------------------------------------------------------
1. Membangun sistem prediksi risiko kesehatan maternal menggunakan data medis
2. Menyediakan interface yang mudah digunakan untuk tenaga medis
3. Menyimpan riwayat pasien dan hasil prediksi dalam database
4. Membandingkan performa model Decision Tree dan Random Forest
5. Memudahkan deployment menggunakan Docker


FITUR UTAMA
--------------------------------------------------------------------------------
1. Input Data Pasien
   - Nama lengkap pasien
   - Nomor telepon
   - Email
   - Alamat lengkap

2. Input Data Medis
   - Usia pasien
   - Tekanan darah sistolik
   - Tekanan darah diastolik
   - Kadar gula darah (BS)
   - Suhu tubuh
   - Detak jantung

3. Prediksi Risiko
   - Menggunakan model Decision Tree
   - Menggunakan model Random Forest
   - Menampilkan tingkat risiko: Low Risk, Mid Risk, High Risk

4. Manajemen Database
   - Penyimpanan data pasien
   - Penyimpanan riwayat rekam medis
   - Relasi antar tabel menggunakan Foreign Key

5. Riwayat Data
   - Melihat semua data pasien
   - Melihat riwayat rekam medis
   - Filter dan pencarian data


STRUKTUR PROYEK
--------------------------------------------------------------------------------
maternal-risk/
  |
  +-- app.py                          : Aplikasi Streamlit utama
  +-- start.py                        : Script untuk menjalankan migrasi & app
  +-- database.py                     : Konfigurasi koneksi database
  +-- models.py                       : Model database SQLAlchemy
  +-- requirements.txt                : Dependencies Python
  +-- Dockerfile                      : Konfigurasi Docker image
  +-- docker-compose.yml              : Konfigurasi Docker Compose
  +-- alembic.ini                     : Konfigurasi Alembic
  |
  +-- alembic/                        : Folder migrasi database
  |    +-- env.py                     : Environment migrasi
  |    +-- script.py.mako             : Template script migrasi
  |    +-- versions/                  : Versi migrasi
  |         +-- 001_initial_migration.py
  |
  +-- model/                          : Folder model Machine Learning
       +-- maternal_health_dt_model.pkl
       +-- maternal_health_dt_model_fix.pkl
       +-- maternal_health_rf_model.pkl
       +-- maternal_health_rf_fix.pkl


TEKNOLOGI YANG DIGUNAKAN
--------------------------------------------------------------------------------
1. Framework dan Library:
   - Streamlit 1.29.0           : Framework web interface
   - Pandas 2.1.4               : Manipulasi dan analisis data
   - Scikit-learn 1.3.2         : Machine Learning algorithms
   - NumPy                      : Komputasi numerik

2. Database:
   - PostgreSQL                 : Database relational
   - SQLAlchemy 2.0.23          : ORM (Object-Relational Mapping)
   - Alembic 1.13.1             : Database migration tool
   - psycopg2-binary 2.9.9      : PostgreSQL adapter

3. Deployment:
   - Docker                     : Containerization
   - Docker Compose             : Multi-container orchestration

4. Utilities:
   - python-dotenv 1.0.0        : Environment variable management
   - joblib 1.3.2               : Model serialization


ALGORITMA MACHINE LEARNING
--------------------------------------------------------------------------------
1. Decision Tree (Pohon Keputusan)
   - Implementasi dari scratch
   - Mendukung parameter: max_depth, min_samples_split, min_samples_leaf
   - Digunakan untuk klasifikasi risiko maternal

2. Random Forest
   - Implementasi dari scratch
   - Ensemble dari multiple decision trees
   - Parameter: n_estimators, max_depth, min_samples_split, bootstrap
   - Memberikan prediksi yang lebih robust


MODEL DATABASE
--------------------------------------------------------------------------------
1. Tabel: patients
   - id              : Primary Key (Integer)
   - name            : Nama pasien (String)
   - phone_number    : Nomor telepon (String)
   - email           : Email (String)
   - address         : Alamat (String)
   - created_at      : Tanggal dibuat (DateTime)

2. Tabel: maternal_records
   - id              : Primary Key (Integer)
   - patient_id      : Foreign Key ke patients (Integer)
   - age             : Usia pasien (Integer)
   - systolic_bp     : Tekanan darah sistolik (Integer)
   - diastolic_bp    : Tekanan darah diastolik (Integer)
   - bs              : Blood Sugar/Gula darah (Float)
   - body_temp       : Suhu tubuh (Float)
   - heart_rate      : Detak jantung (Integer)
   - risk_level      : Tingkat risiko hasil prediksi (String)
   - model_used      : Model yang digunakan (String)
   - created_at      : Tanggal dibuat (DateTime)

Relasi: One-to-Many antara patients dan maternal_records


CARA INSTALASI DAN MENJALANKAN
--------------------------------------------------------------------------------

A. Menggunakan Python Langsung:

   1. Install dependencies:
      pip install -r requirements.txt

   2. Setup environment variables (.env):
      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=maternal_risk
      DB_USER=postgres
      DB_PASSWORD=your_password

   3. Jalankan aplikasi:
      python start.py

   Atau jalankan langsung:
      streamlit run app.py


B. Menggunakan Docker:

   1. Pastikan Docker dan Docker Compose terinstall

   2. Setup environment variables (.env)

   3. Build dan run container:
      docker-compose up --build

   4. Akses aplikasi di browser:
      http://localhost:8501


KONFIGURASI DATABASE
--------------------------------------------------------------------------------
- Database menggunakan PostgreSQL
- Koneksi melalui SQLAlchemy ORM
- Migrasi database menggunakan Alembic
- Environment variables untuk konfigurasi:
  * DB_HOST      : Host database server
  * DB_PORT      : Port database (default: 5432)
  * DB_NAME      : Nama database
  * DB_USER      : Username database
  * DB_PASSWORD  : Password database


FITUR MIGRASI DATABASE
--------------------------------------------------------------------------------
- Alembic digunakan untuk version control database schema
- Auto-generate migration scripts
- Command untuk migrasi:
  * alembic upgrade head     : Jalankan semua migrasi
  * alembic downgrade -1     : Rollback satu versi
  * alembic current          : Cek versi saat ini
  * alembic history          : Lihat riwayat migrasi


WORKFLOW APLIKASI
--------------------------------------------------------------------------------
1. User membuka aplikasi Streamlit
2. User memilih menu:
   - Input Data Pasien Baru
   - Lihat Riwayat Data Pasien
   - Lihat Riwayat Rekam Medis

3. Untuk Input Data Baru:
   a. Isi data identitas pasien
   b. Isi data medis (vital signs)
   c. Pilih model prediksi (Decision Tree / Random Forest)
   d. Klik tombol prediksi
   e. Sistem menampilkan hasil klasifikasi risiko
   f. Data tersimpan ke database

4. Untuk Lihat Riwayat:
   a. Data ditampilkan dalam bentuk tabel
   b. Bisa melakukan filter dan pencarian
   c. Export data jika diperlukan


HASIL PREDIKSI
--------------------------------------------------------------------------------
Sistem mengklasifikasikan risiko kesehatan maternal ke dalam 3 kategori:

1. Low Risk (Risiko Rendah)
   - Kondisi kesehatan normal
   - Tidak memerlukan perhatian khusus

2. Mid Risk (Risiko Sedang)
   - Perlu monitoring lebih intensif
   - Konsultasi berkala dengan dokter

3. High Risk (Risiko Tinggi)
   - Memerlukan perhatian medis segera
   - Monitoring ketat dan penanganan khusus


KEUNGGULAN SISTEM
--------------------------------------------------------------------------------
1. User-friendly interface dengan Streamlit
2. Real-time prediction menggunakan ML models
3. Penyimpanan data terstruktur di database
4. Support multiple ML algorithms untuk perbandingan
5. Containerized dengan Docker untuk kemudahan deployment
6. Database migration management dengan Alembic
7. Scalable dan mudah dikembangkan


CATATAN PENGEMBANGAN
--------------------------------------------------------------------------------
- Model ML dilatih menggunakan dataset kesehatan maternal
- Implementasi Decision Tree dan Random Forest dari scratch
- Model disimpan dalam format pickle (.pkl)
- Terdapat versi fix untuk setiap model (improved version)
- Database schema dapat di-migrate dan rollback dengan mudah
- Environment variables untuk keamanan konfigurasi


PENGEMBANGAN SELANJUTNYA
--------------------------------------------------------------------------------
1. Penambahan algoritma ML lain (SVM, Neural Network)
2. Feature engineering untuk meningkatkan akurasi
3. Dashboard analytics untuk visualisasi data
4. API endpoint untuk integrasi dengan sistem lain
5. Export laporan dalam format PDF
6. Notifikasi otomatis untuk kasus high risk
7. User authentication dan authorization
8. Backup dan restore database otomatis


KONTRIBUTOR
--------------------------------------------------------------------------------
Proyek ini dikembangkan sebagai bagian dari sistem informasi kesehatan
untuk membantu tenaga medis dalam mengidentifikasi risiko kesehatan maternal.


LISENSI
--------------------------------------------------------------------------------
Proyek ini dibuat untuk tujuan edukasi dan penelitian.


KONTAK DAN DUKUNGAN
--------------------------------------------------------------------------------
Untuk pertanyaan, bug report, atau kontribusi, silakan hubungi
tim pengembang proyek.


================================================================================
                                   AKHIR LAPORAN
================================================================================
