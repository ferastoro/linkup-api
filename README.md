# LinkUp — Platform Koneksi & Pertemanan Online

> Proyek UTS Pemrograman Web Lanjutan | Kode MK: 23H07121103

LinkUp adalah sistem **microservice RESTful API** yang dibangun menggunakan FastAPI untuk mengelola platform pertemanan online. Pengguna dapat membuat profil, mencari pengguna lain, dan mengelola koneksi pertemanan.

---

## Arsitektur

```
linkup/
├── auth-service/        → Autentikasi & JWT (port 8001)
├── profile-service/     → Manajemen profil pengguna (port 8002)
├── connection-service/  → Manajemen koneksi antar pengguna (port 8003)
└── README.md
```

Setiap service berjalan **independen** dengan database PostgreSQL masing-masing.

---

## Stack Teknologi

| Komponen | Teknologi |
|---|---|
| Framework | FastAPI (Python 3.11) |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Autentikasi | JWT (python-jose) |
| Password Hashing | bcrypt 4.0.1 + passlib |
| Server | Uvicorn |
| Testing | Postman |

---

## Prasyarat

- Python 3.11
- PostgreSQL 15
- Conda (environment manager)

---

## Setup & Instalasi

### 1. Clone repository

```bash
git clone <repo-url>
cd linkup
```

### 2. Buat conda environment

```bash
conda create -n linkup python=3.11
conda activate linkup
```

### 3. Buat database PostgreSQL

```bash
psql postgres
```

```sql
CREATE DATABASE linkup_auth;
CREATE DATABASE linkup_profile;
CREATE DATABASE linkup_connection;
\q
```

### 4. Install dependensi (lakukan di tiap service)

```bash
cd auth-service
pip install -r requirements.txt
pip install "bcrypt==4.0.1"

cd ../profile-service
pip install -r requirements.txt

cd ../connection-service
pip install -r requirements.txt
```

---

## Menjalankan Service

Buka **3 terminal terpisah**, jalankan masing-masing:

```bash
# Terminal 1 — Auth Service
conda activate linkup
cd auth-service
uvicorn main:app --reload --port 8001

# Terminal 2 — Profile Service
conda activate linkup
cd profile-service
uvicorn main:app --reload --port 8002

# Terminal 3 — Connection Service
conda activate linkup
cd connection-service
uvicorn main:app --reload --port 8003
```

---

## Swagger UI

Setelah semua service jalan, akses dokumentasi API di:

| Service | URL |
|---|---|
| Auth Service | http://localhost:8001/docs |
| Profile Service | http://localhost:8002/docs |
| Connection Service | http://localhost:8003/docs |

---

## Daftar Endpoint

### Auth Service (port 8001)

| Method | Endpoint | Deskripsi | Auth |
|---|---|---|---|
| POST | `/register` | Registrasi pengguna baru | - |
| POST | `/login` | Login & dapatkan JWT token | - |

### Profile Service (port 8002)

| Method | Endpoint | Deskripsi | Auth |
|---|---|---|---|
| POST | `/profiles/` | Buat profil baru | ✅ |
| GET | `/profiles/` | Lihat semua profil | - |
| GET | `/profiles/{id}` | Lihat profil by ID | - |
| PUT | `/profiles/{id}` | Update profil | ✅ |
| DELETE | `/profiles/{id}` | Hapus profil | ✅ |

### Connection Service (port 8003)

| Method | Endpoint | Deskripsi | Auth |
|---|---|---|---|
| POST | `/connections/` | Kirim permintaan koneksi | ✅ |
| GET | `/connections/` | Lihat semua koneksi | - |
| GET | `/connections/me` | Lihat koneksi milik saya | ✅ |
| GET | `/connections/{id}` | Lihat koneksi by ID | - |
| PUT | `/connections/{id}` | Terima/tolak koneksi | ✅ |
| DELETE | `/connections/{id}` | Hapus koneksi | ✅ |

---

## Cara Testing dengan Postman

1. **Register** — `POST /register` di port 8001
2. **Login** — `POST /login`, copy `access_token` dari response
3. **Set token** — di Postman, tab Authorization → Bearer Token → paste token
4. **Buat profil** — `POST /profiles/` di port 8002
5. **Kirim koneksi** — `POST /connections/` di port 8003
6. **Terima koneksi** — `PUT /connections/{id}` dengan body `{"status": "accepted"}`

Import file `linkup-api.json` ke Postman untuk koleksi lengkap.

---

## Status Koneksi

| Status | Keterangan |
|---|---|
| `pending` | Permintaan terkirim, menunggu respons |
| `accepted` | Koneksi diterima |
| `rejected` | Koneksi ditolak |

---

## Catatan

- Token JWT berlaku selama **60 menit**
- Satu pengguna hanya bisa memiliki **satu profil**
- Tidak bisa mengirim koneksi ke diri sendiri
- Hanya **penerima** yang bisa update status koneksi
- Hanya **pengirim** yang bisa hapus koneksi

---

## Author

**[Nama Lengkap]** — [NIM] | Universitas Hasanuddin
