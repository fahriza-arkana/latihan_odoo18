# Arkademy Prasmul ELI 18.0 - Day 1

**Topik:** Development Odoo 18 EE — Fundamental to Intermediate

**Durasi:** 09.00 - 17.00 WIB

**Versi:** Odoo 18.0 Enterprise Edition.

---

## Tujuan Pembelajaran

Pada akhir sesi hari pertama, peserta diharapkan mampu:

1. **Menjelaskan** arsitektur three-tier Odoo serta peran masing-masing layer (Presentation, Application, Database) dalam alur request-response.
2. **Membuat** modul Odoo dari awal menggunakan perintah `scaffold`, lalu memodifikasi metadata modul pada `__manifest__.py` sesuai kebutuhan proyek.
3. **Mengimplementasikan** model ORM lengkap dengan berbagai tipe field (simple, relational, computed) serta menerapkan constraint (`_sql_constraints`, `@api.constrains`) untuk menjaga integritas data.
4. **Membangun** tampilan UI (list, form, search view) termasuk penggunaan elemen lanjutan seperti `<notebook>`, `<header>`, `widget`, `optional`, dan `decoration-*` attribute.
5. **Mengonfigurasi** action window, menu hierarchy, dan access rights (ACL) agar modul dapat diakses oleh group pengguna yang tepat.
6. **Menerapkan** ketiga jenis relasi ORM (Many2one, One2many, Many2many) antar model dan menampilkannya dengan widget yang sesuai di view.
7. **Menggunakan** model inheritance (`_inherit`) dan view inheritance (`xpath`) untuk memperluas fungsionalitas modul existing tanpa memodifikasi source code aslinya.
8. **Menulis** domain expression yang kompleks (termasuk operator `|`, `&`, dan nested condition) untuk memfilter data pada field relasional maupun action window.

---

## 1. Introduction Odoo

### 1.1. Apa itu Odoo?

Odoo adalah platform bisnis *all-in-one* yang menyediakan berbagai aplikasi terintegrasi untuk mengelola operasional perusahaan. Odoo awalnya dikenal dengan nama **OpenERP**, dan kini telah berkembang menjadi salah satu ERP open source paling populer di dunia.

Beberapa fitur utama Odoo:

- **Modular** — Anda dapat menginstal hanya modul yang dibutuhkan (Sales, Inventory, HR, dll).
- **Open Source** — Kode sumber tersedia untuk dikembangkan dan dikustomisasi.
- **Web-Based** — Antarmuka berbasis browser, dapat diakses dari mana saja.
- **ORM-Powered** — Menggunakan Object-Relational Mapping untuk interaksi dengan database PostgreSQL.
- **Extensible** — Mudah diperluas dengan modul kustom.

### 1.2. Arsitektur Odoo

Odoo menggunakan arsitektur **three-tier**:

```
+------------------+     +------------------+     +------------------+
|   Presentation   | <-> |   Application    | <-> |     Database     |
|     (Web UI)     |     |   (Python/ORM)   |     |   (PostgreSQL)   |
+------------------+     +------------------+     +------------------+
```

1. **Presentation Layer** — Antarmuka pengguna berbasis web (HTML, CSS, JavaScript/OWL). Di Odoo 18, framework frontend menggunakan **OWL (Odoo Web Library) 2.x** yang berbasis reactive component.
2. **Application Layer** — Logika bisnis ditulis dalam Python menggunakan framework ORM Odoo. Layer ini menangani routing HTTP, business logic, workflow, dan security.
3. **Database Layer** — PostgreSQL sebagai satu-satunya RDBMS yang didukung. Odoo tidak mendukung MySQL, SQLite, atau database lain.

**Alur Request-Response:**

```
Browser → HTTP Request → Werkzeug (WSGI) → Controller/RPC → ORM → PostgreSQL
                                                                      ↓
Browser ← HTTP Response ← Template Engine (QWeb) ← ORM Result ← PostgreSQL
```

### 1.3. Odoo Community vs Enterprise

| **Aspek**           | **Community Edition**   | **Enterprise Edition**     |
|---------------------|-------------------------|----------------------------|
| Lisensi             | LGPL (Open Source)      | Proprietary (Berbayar)     |
| Fitur Dasar         | Lengkap                 | Lengkap + Fitur Ekstra     |
| Studio (No-Code)    | Tidak tersedia          | Tersedia                   |
| Mobile App          | Terbatas                | Full Native App            |
| Support Resmi       | Komunitas               | Odoo SA Support            |
| Hosting             | Self-hosted             | Odoo.sh / Self-hosted      |
| IoT Box             | Tidak tersedia          | Tersedia                   |
| Barcode Scanner     | Tidak tersedia          | Tersedia                   |

Training ini menggunakan **Odoo 18.0 Enterprise Edition**.

### 1.4. Versi Odoo

Odoo merilis versi baru setiap tahun:

- **Odoo 18** (2024) — Versi terbaru dengan peningkatan UI/UX, performa, dan upgrade OWL 2.x.
- **Odoo 17** (2023) — Peningkatan OWL framework dan fitur AI.
- **Odoo 16** (2022) — Peningkatan performa dan Knowledge Management.
- **Odoo 15** (2021) — Pengenalan OWL (Odoo Web Library).

Setiap versi memiliki siklus Long-Term Support (LTS) selama beberapa tahun.

---

## Refreshment: Installation on Local Environment

Sebelum memulai development, pastikan environment Odoo sudah terinstal dengan benar.

---

## 2. Build an Odoo Module

### 2.1. Membuat Modul dengan Scaffold

Odoo menyediakan perintah `scaffold` untuk membuat struktur modul secara otomatis. Perintah ini sangat berguna untuk memulai development.

**Langkah-langkah:**

1. Pastikan Odoo dapat dijalankan dari terminal:

   ```bash
   ./odoo-bin --version
   ```

2. Arahkan ke folder repository custom Anda:

   ```bash
   cd ~/Workspace/dev/latihan_odoo18
   ```

3. Jalankan perintah scaffold:

   ```bash
   ./odoo-bin scaffold namadepan_library .
   ```

   Contoh (jika nama depan Anda adalah Fahriza):

   ```bash
   ./odoo-bin scaffold fahriza_library .
   ```

4. Setelah berhasil, akan muncul folder baru `fahriza_library/`.

### 2.2. Komposisi dan Struktur Modul

Setelah menjalankan perintah scaffold, Odoo otomatis membuat struktur dasar:

```
fahriza_library/
├── __manifest__.py          → Metadata modul (nama, versi, dependensi, dsb)
├── __init__.py              → Inisialisasi package Python
│
├── controllers/             → Berisi controller HTTP (opsional)
│   ├── __init__.py
│   └── controllers.py
│
├── demo/                    → Berisi data contoh (demo data)
│   └── demo.xml
│
├── models/                  → Definisi model dan field (ORM)
│   ├── __init__.py
│   └── models.py
│
├── security/                → Hak akses pengguna
│   └── ir.model.access.csv
│
└── views/                   → Tampilan (form, list, search)
    ├── templates.xml
    └── views.xml
```

**Penjelasan `__manifest__.py`:**

```python
{
    'name': 'Fahriza Library',
    'version': '18.0.1.0.0',
    'summary': 'Modul Latihan Perpustakaan',
    'description': 'Modul training untuk mengelola data perpustakaan.',
    'author': 'Fahriza',
    'category': 'Education',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

> **Catatan penting:** Field `version` mengikuti konvensi `odoo_version.module_major.module_minor.module_patch`. Field `depends` harus mencakup semua modul yang modelnya kita gunakan — jika lupa, modul akan error saat install.

**Latihan:**

Buka file `__manifest__.py` dan ubah bagian:
- `'name'` menjadi **"Fahriza Library"**
- `'summary'` menjadi **"Modul Latihan Perpustakaan"**
- `'application'` menjadi **True**

Kemudian restart Odoo dan update Apps List untuk melihat modul di daftar aplikasi.

### 2.3. Object-Relational Mapping (ORM)

ORM (*Object-Relational Mapping*) adalah **jembatan antara class Python dan tabel database**. Setiap *model* yang kita buat di Python akan otomatis diterjemahkan oleh Odoo menjadi tabel di PostgreSQL.

Dengan ORM, kita tidak perlu menulis perintah SQL secara manual seperti `CREATE TABLE`, `INSERT`, `UPDATE`, atau `DELETE`. Cukup dengan mendeklarasikan class dan field, Odoo akan:

- Membuat tabel baru di database.
- Membuat kolom sesuai field yang kita definisikan.
- Mengatur relasi antar tabel secara otomatis.
- Menyediakan fungsi CRUD (Create, Read, Update, Delete) yang bisa langsung dipakai di Python.

#### Perbandingan ORM vs SQL Langsung

| **Aksi**        | **SQL Manual (PostgreSQL)**                                      | **ORM (Odoo)**                                                         |
|-----------------|------------------------------------------------------------------|------------------------------------------------------------------------|
| Membuat tabel   | `CREATE TABLE library_book (id SERIAL PRIMARY KEY, name VARCHAR, author VARCHAR);` | `_name = 'library.book'` dan `name = fields.Char()`                  |
| Menambah data   | `INSERT INTO library_book (name, author) VALUES ('Belajar Odoo', 'Fahriza');`     | `self.env['library.book'].create({'name': 'Belajar Odoo', 'author': 'Fahriza'})` |
| Membaca data    | `SELECT * FROM library_book WHERE author='Fahriza';`              | `self.env['library.book'].search([('author','=','Fahriza')])`         |
| Mengubah data   | `UPDATE library_book SET price=120000 WHERE id=1;`                | `book.write({'price': 120000})`                                       |
| Menghapus data  | `DELETE FROM library_book WHERE id=1;`                            | `book.unlink()`                                                        |

Keunggulan ORM:

- **Lebih ringkas** dan mudah dibaca.
- **Lebih aman**, karena terhindar dari SQL Injection.
- **Terintegrasi penuh** dengan hak akses, log aktivitas, dan constraint Odoo.
- **Lebih mudah di-upgrade** karena perubahan field langsung ditangani oleh sistem Odoo.

#### Contoh Model Utama: `library.book`

```python
from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'
    _order = 'name asc, published_date desc'

    name = fields.Char("Judul Buku", required=True)
    isbn = fields.Char("ISBN")
    published_date = fields.Date("Tanggal Terbit")
    price = fields.Float("Harga", digits=(10, 2))
    available = fields.Boolean("Tersedia", default=True)
```

> **Catatan:** Atribut `_order` menentukan default sorting saat data ditampilkan. Atribut `digits=(10, 2)` pada `Float` mengatur presisi angka (10 digit total, 2 desimal).

#### Cara ORM Membuat Tabel di Database

Ketika modul dipasang (install), Odoo akan:

1. Membaca deklarasi `_name = 'library.book'`.
2. Membuat tabel baru dengan nama `library_book` di PostgreSQL (titik diganti underscore).
3. Menambahkan kolom sesuai field yang didefinisikan.
4. Menambahkan kolom bawaan (*magic fields*):

| **Kolom**      | **Tipe Data**    | **Keterangan**             |
|----------------|------------------|----------------------------|
| `id`           | integer          | Primary key (auto-increment)|
| `create_uid`   | integer          | FK ke user pembuat record  |
| `create_date`  | timestamp        | Tanggal record dibuat      |
| `write_uid`    | integer          | FK ke user terakhir ubah   |
| `write_date`   | timestamp        | Waktu terakhir diubah      |

#### Operasi CRUD dengan ORM

**1. Create (Tambah Data)**

```python
book = self.env['library.book'].create({
    'name': 'Odoo 18 Developer Guide',
    'isbn': 'ISBN-0001',
    'price': 150000,
    'available': True,
})
# book.id sekarang berisi ID record yang baru dibuat
```

**2. Search & Read (Baca Data)**

```python
# search() mengembalikan recordset
books = self.env['library.book'].search([('available', '=', True)])
for book in books:
    print(book.name, book.price)

# search() dengan limit dan order
recent_books = self.env['library.book'].search(
    [('available', '=', True)],
    limit=10,
    order='published_date desc',
)

# search_count() mengembalikan jumlah record
count = self.env['library.book'].search_count([('available', '=', True)])

# browse() mengambil record berdasarkan ID (tanpa filter)
book = self.env['library.book'].browse(1)

# search_read() mengembalikan list of dict (lebih efisien untuk data banyak)
data = self.env['library.book'].search_read(
    [('available', '=', True)],
    fields=['name', 'price'],
    limit=5,
)
```

**3. Update (Ubah Data)**

```python
book = self.env['library.book'].browse(1)
book.write({'price': 175000})

# Update multiple records sekaligus
books = self.env['library.book'].search([('price', '<', 50000)])
books.write({'available': False})
```

**4. Delete (Hapus Data)**

```python
book = self.env['library.book'].browse(1)
book.unlink()
```

**5. Recordset Operations (Lanjutan)**

```python
books = self.env['library.book'].search([])

# filtered() — filter recordset di memory (tanpa query SQL baru)
expensive = books.filtered(lambda b: b.price > 100000)

# mapped() — ambil nilai tertentu dari recordset
names = books.mapped('name')  # list of string

# sorted() — sort recordset di memory
by_price = books.sorted(key=lambda b: b.price, reverse=True)

# Operasi set pada recordset
books_a = self.env['library.book'].browse([1, 2, 3])
books_b = self.env['library.book'].browse([2, 3, 4])
union = books_a | books_b        # {1, 2, 3, 4}
intersection = books_a & books_b  # {2, 3}
difference = books_a - books_b    # {1}
```

#### Catatan Tambahan

- ORM Odoo sepenuhnya menggunakan **PostgreSQL** (tidak mendukung MySQL).
- Semua operasi CRUD dijalankan dalam konteks environment `self.env`.
- Odoo otomatis mengatur **transaksi (transaction)** dan **rollback** jika terjadi error.
- Model ORM juga terhubung dengan fitur keamanan seperti **Access Control List (ACL)** dan **Record Rules**.
- Penambahan field baru akan otomatis membuat kolom baru di tabel tanpa perlu perintah SQL tambahan.

### 2.4. Model Fields

#### 2.4.1. Common Attributes (Atribut Umum)

Setiap field dapat memiliki atribut berikut:

| Atribut      | Tipe     | Keterangan                                                  |
|--------------|----------|-------------------------------------------------------------|
| `string`     | `str`    | Label tampilan di UI                                        |
| `required`   | `bool`   | Field wajib diisi (default `False`)                         |
| `default`    | `any`    | Nilai awal (bisa callable: `default=lambda self: ...`)      |
| `readonly`   | `bool`   | Tidak dapat diubah dari UI                                  |
| `help`       | `str`    | Tooltip keterangan tambahan                                 |
| `index`      | `bool`   | Membuat index di database (untuk field yang sering di-search)|
| `copy`       | `bool`   | Apakah field ikut ter-copy saat record di-duplicate         |
| `groups`     | `str`    | Comma-separated XML ID group yang boleh melihat field ini   |
| `tracking`   | `bool`   | Aktifkan tracking perubahan di chatter (butuh `mail.thread`) |

#### 2.4.2. Simple Fields

```python
name = fields.Char("Judul Buku", required=True, index=True)
description = fields.Text("Deskripsi")
price = fields.Float("Harga", digits=(10, 2))
page_count = fields.Integer("Jumlah Halaman")
available = fields.Boolean("Tersedia", default=True)
published_date = fields.Date("Tanggal Terbit")
last_borrow_datetime = fields.Datetime("Terakhir Dipinjam")
cover_image = fields.Binary("Cover Buku")
state = fields.Selection([
    ('draft', 'Draft'),
    ('available', 'Tersedia'),
    ('borrowed', 'Dipinjam'),
    ('lost', 'Hilang'),
], string="Status", default='draft')
content = fields.Html("Konten")
```

#### 2.4.3. Reserved Fields (Magic Fields)

Field bawaan Odoo yang tersedia di semua model:

- `id` — Primary key
- `create_date`, `write_date` — Timestamp pembuatan dan modifikasi
- `create_uid`, `write_uid` — User pembuat dan pengubah
- `display_name` — Computed field yang mengambil representasi nama record (biasanya dari `_rec_name`)

#### 2.4.4. Computed Fields

Computed field adalah field yang nilainya dihitung secara otomatis oleh method Python, bukan diisi manual oleh user.

```python
from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'

    name = fields.Char("Judul Buku", required=True)
    price = fields.Float("Harga")
    discount_percent = fields.Float("Diskon (%)")

    final_price = fields.Float(
        "Harga Akhir",
        compute='_compute_final_price',
        store=True,  # simpan di database agar bisa di-search/group
    )

    @api.depends('price', 'discount_percent')
    def _compute_final_price(self):
        for record in self:
            record.final_price = record.price * (1 - record.discount_percent / 100)
```

**Poin penting computed field:**

- Gunakan decorator `@api.depends(...)` untuk mendeklarasikan field apa saja yang menjadi trigger rekomputasi.
- Jika `store=True`, nilai disimpan di database dan di-recompute saat dependency berubah.
- Jika `store=False` (default), nilai dihitung *on-the-fly* setiap kali diakses — tidak bisa digunakan untuk search/filter/group by.
- Method compute **harus** iterasi semua record dalam `self` (karena `self` bisa berisi multiple records).

#### 2.4.5. Constraints

Constraints digunakan untuk menjaga integritas data. Odoo mendukung dua jenis:

**SQL Constraints:**

```python
class LibraryBook(models.Model):
    _name = 'library.book'

    isbn = fields.Char("ISBN")
    price = fields.Float("Harga")

    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'ISBN harus unik! Tidak boleh ada dua buku dengan ISBN yang sama.'),
        ('price_positive', 'CHECK(price >= 0)', 'Harga tidak boleh negatif.'),
    ]
```

**Python Constraints:**

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'

    published_date = fields.Date("Tanggal Terbit")

    @api.constrains('published_date')
    def _check_published_date(self):
        for record in self:
            if record.published_date and record.published_date > fields.Date.today():
                raise ValidationError("Tanggal terbit tidak boleh di masa depan!")
```

#### 2.4.6. Special Fields (Relasional)

Special fields digunakan untuk membuat relasi antar model (dibahas detail di Bagian 4).

```python
category_id = fields.Many2one('library.category', string="Kategori")
book_ids = fields.One2many('library.book', 'category_id', string="Daftar Buku")
author_ids = fields.Many2many('library.author', string="Penulis")
```

### 2.5. Data Files

File XML digunakan untuk menambahkan data awal (initial data) atau konfigurasi. Data file biasanya disimpan di dalam folder `data/`.

**Contoh:** `data/fahriza_library_data.xml`

```xml
<odoo>
    <data>
        <record id="book_python" model="library.book">
            <field name="name">Python untuk Pemula</field>
            <field name="isbn">ISBN1234567</field>
            <field name="published_date">2023-06-01</field>
            <field name="price">120000</field>
            <field name="available">True</field>
        </record>
    </data>
</odoo>
```

Tambahkan file ini ke `__manifest__.py`:

```python
'data': [
    'data/fahriza_library_data.xml',
],
```

> **Catatan:** Untuk data yang hanya diinstal pada mode demo, gunakan key `'demo'` alih-alih `'data'` di manifest. Data di `'data'` selalu diinstal, sedangkan data di `'demo'` hanya diinstal jika database dibuat dengan opsi *"Load demonstration data"*.

**Latihan:**

1. Buat model `library.book` di file `models/models.py`.
2. Tambahkan field:
   - `name` (Char, required)
   - `isbn` (Char)
   - `published_date` (Date)
   - `price` (Float)
   - `available` (Boolean, default True)
3. Tambahkan `_sql_constraints` untuk memastikan ISBN unik.
4. Buat file data XML di `data/fahriza_library_data.xml` dan tambahkan 3 record buku.
5. Daftarkan file data di `__manifest__.py`.
6. Restart Odoo, kemudian install atau upgrade modul `fahriza_library`.
7. Cek di database PostgreSQL apakah tabel `library_book` sudah dibuat dan data sudah masuk.

---

## 3. Basic Views

Setelah model `library.book` dibuat, langkah berikutnya adalah menampilkan datanya di antarmuka Odoo. Tampilan atau *view* dalam Odoo ditulis menggunakan XML, dan setiap view terhubung ke sebuah model.

Jenis view utama:

| View Type     | Kegunaan                                  |
|---------------|-------------------------------------------|
| **List**      | Menampilkan banyak record dalam bentuk tabel |
| **Form**      | Menampilkan detail satu record            |
| **Search**    | Menyediakan kolom pencarian dan filter    |
| **Kanban**    | Tampilan kartu (dibahas di tingkat lanjut)|
| **Calendar**  | Tampilan kalender                         |
| **Pivot**     | Tampilan pivot table untuk analisis       |
| **Graph**     | Tampilan grafik / chart                   |

### 3.1. Generic View Declaration

Setiap view di Odoo dideklarasikan dalam model `ir.ui.view` melalui XML:

```xml
<record id="view_id_unik" model="ir.ui.view">
    <field name="name">nama_view</field>
    <field name="model">nama_model</field>
    <field name="arch" type="xml">
        <!-- struktur tampilan disini -->
    </field>
</record>
```

- `id` — identitas unik view (XML ID), digunakan untuk referensi.
- `name` — nama view (disarankan deskriptif, format: `model.name.view_type`).
- `model` — model yang digunakan (contoh: `library.book`).
- `arch` — isi struktur XML dari tampilan (form, list, dsb.).

### 3.2. List Views

List view menampilkan **daftar data** seperti tabel. Biasanya berisi beberapa kolom utama.

```xml
<record id="view_library_book_list" model="ir.ui.view">
    <field name="name">library.book.list</field>
    <field name="model">library.book</field>
    <field name="arch" type="xml">
        <list string="Daftar Buku" decoration-danger="available == False"
              decoration-success="available == True">
            <field name="name"/>
            <field name="isbn"/>
            <field name="published_date"/>
            <field name="price" widget="monetary" optional="show"/>
            <field name="available"/>
        </list>
    </field>
</record>
```

**Fitur lanjutan pada list view:**

- `decoration-danger`, `decoration-success`, `decoration-warning` — Pewarnaan baris berdasarkan kondisi.
- `optional="show"` / `optional="hide"` — Kolom bisa ditampilkan atau disembunyikan oleh user melalui toggle.
- `default_order` — Menentukan default sorting langsung dari view.
- `editable="bottom"` / `editable="top"` — Memungkinkan edit inline langsung di list tanpa membuka form.

### 3.3. Form Views

Form view menampilkan **detail satu record** — digunakan saat membuat atau mengedit data.

```xml
<record id="view_library_book_form" model="ir.ui.view">
    <field name="name">library.book.form</field>
    <field name="model">library.book</field>
    <field name="arch" type="xml">
        <form string="Data Buku">
            <header>
                <!-- Tempat untuk status bar dan button -->
            </header>
            <sheet>
                <div class="oe_title">
                    <label for="name"/>
                    <h1>
                        <field name="name" placeholder="Judul Buku"/>
                    </h1>
                </div>
                <group>
                    <group string="Informasi Umum">
                        <field name="isbn"/>
                        <field name="published_date"/>
                        <field name="available"/>
                    </group>
                    <group string="Harga">
                        <field name="price"/>
                    </group>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

**Penjelasan elemen form:**

- `<header>` — Area di atas sheet untuk status bar dan button action.
- `<sheet>` — Area utama isi form (dengan margin & padding yang rapi).
- `<div class="oe_title">` — Pola umum untuk menampilkan judul/nama record dengan font besar.
- `<group>` — Mengelompokkan field. Dua `<group>` di dalam `<group>` akan menghasilkan layout dua kolom.
- `<notebook>` dan `<page>` — Membuat tab di form (contoh di bagian relasi nanti).

### 3.4. Search Views

Search view mendefinisikan **kolom pencarian, filter, dan group by** di bagian atas list view.

```xml
<record id="view_library_book_search" model="ir.ui.view">
    <field name="name">library.book.search</field>
    <field name="model">library.book</field>
    <field name="arch" type="xml">
        <search string="Cari Buku">
            <field name="name" string="Judul Buku"
                   filter_domain="['|', ('name', 'ilike', self), ('isbn', 'ilike', self)]"/>
            <field name="isbn"/>
            <separator/>
            <filter string="Tersedia" name="filter_available"
                    domain="[('available', '=', True)]"/>
            <filter string="Tidak Tersedia" name="filter_unavailable"
                    domain="[('available', '=', False)]"/>
            <separator/>
            <group expand="0" string="Group By">
                <filter string="Status Ketersediaan" name="groupby_available"
                        context="{'group_by': 'available'}"/>
                <filter string="Tanggal Terbit" name="groupby_date"
                        context="{'group_by': 'published_date:month'}"/>
            </group>
        </search>
    </field>
</record>
```

**Fitur lanjutan search view:**

- `filter_domain` — Custom domain untuk pencarian (contoh: search di multiple field sekaligus).
- `<filter>` dengan `domain` — Filter cepat yang bisa diklik user.
- `<filter>` dengan `context={'group_by': ...}` — Pengelompokan data.
- `<separator/>` — Pemisah visual antar group filter.

### 3.5. Actions dan Menus

Agar view dapat diakses dari UI, kita perlu mendefinisikan **Action Window** dan **Menu**.

```xml
<!-- Menu Root -->
<menuitem id="menu_library_root" name="Perpustakaan"/>

<!-- Submenu Buku -->
<menuitem id="menu_library_book" name="Data Buku" parent="menu_library_root"/>

<!-- Action Window -->
<record id="action_library_book" model="ir.actions.act_window">
    <field name="name">Daftar Buku</field>
    <field name="res_model">library.book</field>
    <field name="view_mode">list,form</field>
    <field name="context">{'search_default_filter_available': 1}</field>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">
            Buat Buku Pertama Anda!
        </p>
        <p>
            Klik tombol "New" untuk menambahkan buku baru ke perpustakaan.
        </p>
    </field>
</record>

<!-- Hubungan Action Window dengan View -->
<record id="action_library_book_list" model="ir.actions.act_window.view">
    <field name="sequence" eval="1"/>
    <field name="view_mode">list</field>
    <field name="view_id" ref="fahriza_library.view_library_book_list"/>
    <field name="act_window_id" ref="action_library_book"/>
</record>

<record id="action_library_book_form" model="ir.actions.act_window.view">
    <field name="sequence" eval="2"/>
    <field name="view_mode">form</field>
    <field name="view_id" ref="fahriza_library.view_library_book_form"/>
    <field name="act_window_id" ref="action_library_book"/>
</record>

<!-- Menu Item -->
<menuitem id="menu_library_book_list"
          name="Buku"
          parent="menu_library_book"
          action="action_library_book"/>
```

**Penjelasan:**

- `ir.actions.act_window` — Menentukan model dan mode tampilan default.
- `context` — Bisa digunakan untuk mengaktifkan filter default (`search_default_*`) atau mengirim nilai default saat create.
- `help` — Pesan yang ditampilkan saat tidak ada data (empty state).
- `ir.actions.act_window.view` — Mendefinisikan urutan dan view spesifik.
- `menuitem` — Membuat menu di UI Odoo.

#### Menggabungkan Semua View

Semua deklarasi view, menu dan action dapat dimasukkan ke dalam satu file XML, misalnya di `views/library_book_views.xml`:

```xml
<odoo>
    <record id="view_library_book_list" model="ir.ui.view">
        <field name="name">library.book.list</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <list string="Daftar Buku">
                <field name="name"/>
                <field name="isbn"/>
                <field name="published_date"/>
                <field name="price"/>
                <field name="available"/>
            </list>
        </field>
    </record>

    <record id="view_library_book_form" model="ir.ui.view">
        <field name="name">library.book.form</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <form string="Data Buku">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="published_date"/>
                        <field name="isbn"/>
                        <field name="price"/>
                        <field name="available"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_library_book_search" model="ir.ui.view">
        <field name="name">library.book.search</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <search>
                <field name="name" string="Judul Buku"/>
                <field name="isbn"/>
            </search>
        </field>
    </record>

    <!-- Menu Root -->
    <menuitem id="menu_library_root" name="Perpustakaan"/>

    <!-- Submenu Buku -->
    <menuitem id="menu_library_book" name="Data Buku" parent="menu_library_root"/>

    <!-- Action Window -->
    <record id="action_library_book" model="ir.actions.act_window">
        <field name="name">Daftar Buku</field>
        <field name="res_model">library.book</field>
        <field name="view_mode">list,form</field>
    </record>

    <!-- Hubungan Action Window dengan View -->
    <record id="action_library_book_list" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">list</field>
        <field name="view_id" ref="fahriza_library.view_library_book_list"/>
        <field name="act_window_id" ref="action_library_book"/>
    </record>

    <record id="action_library_book_form" model="ir.actions.act_window.view">
        <field name="sequence" eval="2"/>
        <field name="view_mode">form</field>
        <field name="view_id" ref="fahriza_library.view_library_book_form"/>
        <field name="act_window_id" ref="action_library_book"/>
    </record>

    <!-- Menu Item -->
    <menuitem id="menu_library_book_list"
        name="Buku"
        parent="menu_library_book"
        action="action_library_book"/>
</odoo>
```

Setelah file ini dimuat, menu **Perpustakaan > Data Buku > Buku** akan muncul di modul.

### 3.6. Security (Access Rights)

Sebelum model `library.book` dapat digunakan dari antarmuka Odoo, kita perlu memberikan hak akses (permissions).

#### 3.6.1. File `ir.model.access.csv`

File hak akses disimpan di:

```
fahriza_library/
└── security/
    └── ir.model.access.csv
```

Isinya:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_library_book_user,access.library.book,model_library_book,base.group_user,1,1,1,1
```

#### 3.6.2. Penjelasan Kolom

| Kolom           | Keterangan                                                              |
|-----------------|-------------------------------------------------------------------------|
| `id`            | Identitas unik record hak akses (tidak boleh sama antar modul)         |
| `name`          | Nama deskriptif untuk rule ini                                         |
| `model_id:id`   | XML ID model (`model_` + `_name` dengan titik diganti underscore)      |
| `group_id:id`   | Grup pengguna yang diberi izin (kosongkan untuk semua user)             |
| `perm_read`     | Izin membaca data (1 = ya, 0 = tidak)                                  |
| `perm_write`    | Izin mengubah data                                                     |
| `perm_create`   | Izin membuat data                                                      |
| `perm_unlink`   | Izin menghapus data                                                    |

#### 3.6.3. Registrasi File di Manifest

```python
'data': [
    'security/ir.model.access.csv',  # HARUS sebelum views
    'data/fahriza_library_data.xml',
    'views/library_book_views.xml',
],
```

> **Penting:** File security **harus** didaftarkan sebelum file views dan data yang menggunakan model terkait, karena Odoo memproses file secara berurutan. Jika views dimuat sebelum ACL, akan muncul access error saat install.

#### Tips Security

- Tanpa file ini, Odoo menampilkan error: `Access Error: You are not allowed to access 'library.book' records.`
- Untuk akses **khusus admin**, gunakan `base.group_system`.
- Group umum: `base.group_user` (internal user), `base.group_portal` (portal user), `base.group_public` (public user).
- Hak akses lanjutan seperti *record rules* dibahas pada bab selanjutnya.

---

## 4. Relations Between Models

Relasi digunakan untuk menghubungkan satu model dengan model lainnya. Di Odoo, relasi dikelola sepenuhnya oleh ORM.

### 4.1. Jenis Relasi di Odoo

| Jenis Relasi   | Arah Relasi       | Kolom di DB?  | Contoh Logika                                       |
|----------------|-------------------|---------------|-----------------------------------------------------|
| `Many2one`     | Banyak → Satu     | Ya (FK)       | Banyak buku memiliki satu kategori                  |
| `One2many`     | Satu → Banyak     | Tidak (virtual)| Satu kategori memiliki banyak buku                  |
| `Many2many`    | Banyak ↔ Banyak   | Tabel relasi  | Satu buku punya banyak penulis, dan sebaliknya      |

### 4.2. Many2one (Buku → Kategori)

Setiap buku hanya memiliki satu kategori. Relasi ini seperti *foreign key* di PostgreSQL.

```python
from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Kategori Buku'

    name = fields.Char("Nama Kategori", required=True)
    description = fields.Text("Deskripsi")

class LibraryBook(models.Model):
    _name = 'library.book'

    category_id = fields.Many2one(
        'library.category',
        string="Kategori",
        ondelete='set null',  # atau 'restrict', 'cascade'
        index=True,
    )
```

**Opsi `ondelete`:**

| Nilai        | Perilaku saat record parent dihapus            |
|--------------|------------------------------------------------|
| `'set null'` | Field diset ke null (default)                  |
| `'restrict'` | Tolak penghapusan jika masih ada child record  |
| `'cascade'`  | Hapus semua child record juga                  |

### 4.3. One2many (Kategori → Buku)

Kebalikan dari Many2one — menampilkan semua buku dalam satu kategori.

```python
class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Kategori Buku'

    name = fields.Char("Nama Kategori", required=True)
    description = fields.Text("Deskripsi")

    book_ids = fields.One2many(
        'library.book',       # model tujuan (comodel)
        'category_id',        # field Many2one di comodel (inverse field)
        string="Daftar Buku",
    )
```

> **Catatan:** `One2many` tidak membuat kolom baru di database. Field ini bersifat virtual — digunakan hanya untuk navigasi dan tampilan. Setiap `One2many` **harus** memiliki pasangan `Many2one` di model tujuan.

### 4.4. Many2many (Buku ↔ Penulis)

Satu buku bisa memiliki banyak penulis, dan satu penulis bisa menulis banyak buku.

```python
class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Penulis Buku'

    name = fields.Char("Nama Penulis", required=True)
    biography = fields.Text("Biografi")

class LibraryBook(models.Model):
    _name = 'library.book'

    author_ids = fields.Many2many(
        'library.author',
        'library_book_author_rel',   # nama tabel relasi (opsional)
        'book_id',                   # kolom FK ke buku
        'author_id',                 # kolom FK ke penulis
        string="Penulis",
    )
```

ORM otomatis membuat tabel relasi `library_book_author_rel` dengan dua kolom: `book_id` dan `author_id`.

**Operasi Many2many menggunakan special command tuples:**

```python
# Menambah relasi (link) — command (4, id)
book.write({'author_ids': [(4, author_id)]})

# Menghapus relasi (unlink) tanpa menghapus record — command (3, id)
book.write({'author_ids': [(3, author_id)]})

# Mengganti semua relasi — command (6, 0, [ids])
book.write({'author_ids': [(6, 0, [1, 2, 3])]})

# Membuat record baru sekaligus link — command (0, 0, {values})
book.write({'author_ids': [(0, 0, {'name': 'Penulis Baru'})]})
```

### 4.5. Implementasi Lengkap Relasi dalam Modul Library

#### 4.5.1. Definisi Model dan Field

```python
from odoo import models, fields

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Kategori Buku'

    name = fields.Char("Nama Kategori", required=True)
    book_ids = fields.One2many('library.book', 'category_id', string="Daftar Buku")
    book_count = fields.Integer("Jumlah Buku", compute='_compute_book_count')

    def _compute_book_count(self):
        for category in self:
            category.book_count = len(category.book_ids)


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Penulis Buku'

    name = fields.Char("Nama Penulis", required=True)
    biography = fields.Text("Biografi")
    book_ids = fields.Many2many('library.book', string="Buku Ditulis")


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'

    name = fields.Char("Judul Buku", required=True)
    isbn = fields.Char("ISBN")
    published_date = fields.Date("Tanggal Terbit")
    price = fields.Float("Harga")
    available = fields.Boolean("Tersedia", default=True)

    category_id = fields.Many2one('library.category', string="Kategori")
    author_ids = fields.Many2many('library.author', string="Penulis")
```

#### 4.5.2. View Buku (`views/library_book_views.xml`)

```xml
<odoo>
    <record id="view_library_book_list" model="ir.ui.view">
        <field name="name">library.book.list</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <list string="Daftar Buku">
                <field name="name"/>
                <field name="isbn"/>
                <field name="category_id"/>
                <field name="published_date"/>
                <field name="price"/>
                <field name="available"/>
            </list>
        </field>
    </record>

    <record id="view_library_book_form" model="ir.ui.view">
        <field name="name">library.book.form</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <form string="Data Buku">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="category_id"/>
                        <field name="author_ids" widget="many2many_tags"/>
                        <field name="published_date"/>
                        <field name="isbn"/>
                        <field name="price"/>
                        <field name="available"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_library_book_search" model="ir.ui.view">
        <field name="name">library.book.search</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <search>
                <field name="name" string="Judul Buku"/>
                <field name="isbn"/>
                <field name="category_id"/>
            </search>
        </field>
    </record>

    <!-- Menu Root -->
    <menuitem id="menu_library_root" name="Perpustakaan"/>

    <!-- Submenu Buku -->
    <menuitem id="menu_library_book" name="Data Buku" parent="menu_library_root"/>

    <!-- Action Window -->
    <record id="action_library_book" model="ir.actions.act_window">
        <field name="name">Daftar Buku</field>
        <field name="res_model">library.book</field>
        <field name="view_mode">list,form</field>
    </record>

    <!-- Hubungan Action Window dengan View -->
    <record id="action_library_book_list" model="ir.actions.act_window.view">
        <field name="sequence" eval="1"/>
        <field name="view_mode">list</field>
        <field name="view_id" ref="fahriza_library.view_library_book_list"/>
        <field name="act_window_id" ref="action_library_book"/>
    </record>

    <record id="action_library_book_form" model="ir.actions.act_window.view">
        <field name="sequence" eval="2"/>
        <field name="view_mode">form</field>
        <field name="view_id" ref="fahriza_library.view_library_book_form"/>
        <field name="act_window_id" ref="action_library_book"/>
    </record>

    <!-- Menu Item -->
    <menuitem id="menu_library_book_list"
        name="Buku"
        parent="menu_library_book"
        action="action_library_book"/>
</odoo>
```

#### 4.5.3. View Kategori (`views/library_category_views.xml`)

```xml
<odoo>
    <!-- List View Kategori -->
    <record id="view_library_category_list" model="ir.ui.view">
        <field name="name">library.category.list</field>
        <field name="model">library.category</field>
        <field name="arch" type="xml">
            <list string="Daftar Kategori">
                <field name="name"/>
            </list>
        </field>
    </record>

    <!-- Form View Kategori -->
    <record id="view_library_category_form" model="ir.ui.view">
        <field name="name">library.category.form</field>
        <field name="model">library.category</field>
        <field name="arch" type="xml">
            <form string="Data Kategori">
                <sheet>
                    <group>
                        <field name="name"/>
                    </group>
                    <notebook>
                        <page string="Buku dalam Kategori">
                            <field name="book_ids">
                                <list>
                                    <field name="name"/>
                                    <field name="isbn"/>
                                    <field name="published_date"/>
                                </list>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Search View Kategori -->
    <record id="view_library_category_search" model="ir.ui.view">
        <field name="name">library.category.search</field>
        <field name="model">library.category</field>
        <field name="arch" type="xml">
            <search string="Cari Kategori">
                <field name="name" string="Nama Kategori"/>
            </search>
        </field>
    </record>

    <!-- Action Window Kategori -->
    <record id="action_library_category" model="ir.actions.act_window">
        <field name="name">Daftar Kategori</field>
        <field name="res_model">library.category</field>
        <field name="view_mode">list,form</field>
    </record>

    <!-- Menu Item Kategori -->
    <menuitem id="menu_library_category"
              name="Kategori"
              parent="menu_library_root"
              action="action_library_category"/>
</odoo>
```

#### 4.5.4. View Penulis (`views/library_author_views.xml`)

```xml
<odoo>
    <!-- List View Penulis -->
    <record id="view_library_author_list" model="ir.ui.view">
        <field name="name">library.author.list</field>
        <field name="model">library.author</field>
        <field name="arch" type="xml">
            <list string="Daftar Penulis">
                <field name="name"/>
                <field name="book_ids" widget="many2many_tags"/>
            </list>
        </field>
    </record>

    <!-- Form View Penulis -->
    <record id="view_library_author_form" model="ir.ui.view">
        <field name="name">library.author.form</field>
        <field name="model">library.author</field>
        <field name="arch" type="xml">
            <form string="Data Penulis">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="biography"/>
                        <field name="book_ids" widget="many2many_tags"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Search View Penulis -->
    <record id="view_library_author_search" model="ir.ui.view">
        <field name="name">library.author.search</field>
        <field name="model">library.author</field>
        <field name="arch" type="xml">
            <search string="Cari Penulis">
                <field name="name" string="Nama Penulis"/>
            </search>
        </field>
    </record>

    <!-- Action Window Penulis -->
    <record id="action_library_author" model="ir.actions.act_window">
        <field name="name">Daftar Penulis</field>
        <field name="res_model">library.author</field>
        <field name="view_mode">list,form</field>
    </record>

    <!-- Menu Item Penulis -->
    <menuitem id="menu_library_author"
              name="Penulis"
              parent="menu_library_root"
              action="action_library_author"/>
</odoo>
```

#### 4.5.5. Access Rights (`security/ir.model.access.csv`)

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_library_book_user,access.library.book,model_library_book,base.group_user,1,1,1,1
access_library_category_user,access.library.category,model_library_category,base.group_user,1,1,1,1
access_library_author_user,access.library.author,model_library_author,base.group_user,1,1,1,1
```

#### 4.5.6. Registrasi Semua File di Manifest

```python
'data': [
    'security/ir.model.access.csv',
    'data/fahriza_library_data.xml',
    'views/library_book_views.xml',
    'views/library_category_views.xml',
    'views/library_author_views.xml',
],
```

**Latihan:**

1. Buat model `library.category` dan `library.author`.
2. Tambahkan relasi:
   - `Many2one` dari `library.book` ke `library.category`
   - `Many2many` antara `library.book` dan `library.author`
   - `One2many` dari `library.category` ke `library.book`
3. Buat menu, action dan view untuk model `library.category` dan `library.author`.
4. Tambahkan field relasi ke form view masing-masing.
5. Coba input data kategori dan penulis dari UI, lalu hubungkan dengan buku.
6. Perhatikan bagaimana field relasi otomatis membuat dropdown dan tabel relasi di antarmuka Odoo.

---

## 5. Inheritance

Inheritance (pewarisan) dalam Odoo digunakan untuk **memperluas atau memodifikasi perilaku** dari model atau view yang sudah ada, tanpa harus menyalin seluruh kodenya.

Ada dua jenis inheritance utama di Odoo:

1. **Model Inheritance** — memperluas model Python.
2. **View Inheritance** — memperluas tampilan XML.

### 5.1. Model Inheritance

Model inheritance digunakan untuk **menambahkan atau mengubah field serta method** dari model yang sudah ada.

#### Jenis-jenis Model Inheritance

| Tipe                   | `_name`           | `_inherit`          | Efek                                           |
|------------------------|-------------------|---------------------|-------------------------------------------------|
| **Class Inheritance**  | Tidak diisi       | Model existing      | Menambah field/method ke model existing         |
| **Prototype Inheritance** | Diisi (baru)  | Model existing      | Membuat model baru dengan copy field dari parent |
| **Delegation Inheritance** | Diisi (baru) | -                   | Menggunakan `_inherits` (dict) — delegasi field |

Yang paling umum digunakan di day-to-day development adalah **Class Inheritance**.

**Contoh Class Inheritance:** menambahkan field ke model `res.partner`

```python
# File: models/res_partner.py
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean("Anggota Perpustakaan", default=False)
    library_card_number = fields.Char("Nomor Kartu Perpustakaan")
    membership_date = fields.Date("Tanggal Bergabung")
```

**Penjelasan:**

- `_inherit` (tanpa `_name`) mewarisi model existing — field baru ditambahkan langsung ke model `res.partner`.
- Tidak ada tabel baru yang dibuat; kolom baru ditambahkan ke tabel `res_partner`.
- Model ini otomatis digabung dengan model induknya saat Odoo memproses registry.

**Struktur folder:**

```
fahriza_library/
├── models/
│   ├── __init__.py
│   ├── models.py
│   └── res_partner.py
└── __manifest__.py
```

File `models/__init__.py`:

```python
from . import models
from . import res_partner
```

### 5.2. View Inheritance

View inheritance digunakan untuk **menambahkan atau memodifikasi elemen tampilan** dari view existing tanpa menduplikasi seluruh XML.

**Contoh:** menambahkan field `is_library_member` ke form `res.partner`.

```xml
<!-- File: views/res_partner_views.xml -->
<odoo>
    <record id="view_partner_form_inherit_library" model="ir.ui.view">
        <field name="name">res.partner.form.inherit.library</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_form"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='function']" position="before">
                <field name="is_library_member"/>
                <field name="library_card_number"
                       invisible="not is_library_member"/>
                <field name="membership_date"
                       invisible="not is_library_member"/>
            </xpath>
        </field>
    </record>
</odoo>
```

**Penjelasan:**

- `inherit_id` — Menunjuk ke view asli yang ingin diperluas.
- `xpath` — Menentukan lokasi di mana elemen baru akan disisipkan.
- `invisible="not is_library_member"` — Field hanya tampil jika checkbox di-centang (dynamic visibility di Odoo 18).

**Opsi `position` pada xpath:**

| Position    | Efek                                         |
|-------------|----------------------------------------------|
| `before`    | Sisipkan sebelum elemen target               |
| `after`     | Sisipkan setelah elemen target               |
| `inside`    | Sisipkan di dalam elemen target (sebagai child) |
| `replace`   | Ganti elemen target sepenuhnya               |
| `attributes`| Ubah atribut dari elemen target              |

**Contoh mengubah atribut:**

```xml
<xpath expr="//field[@name='phone']" position="attributes">
    <attribute name="string">Telepon Kantor</attribute>
</xpath>
```

**Shortcut tanpa xpath** — Jika target adalah field, bisa langsung tulis:

```xml
<field name="function" position="before">
    <field name="is_library_member"/>
</field>
```

Pastikan file XML didaftarkan di `__manifest__.py`:

```python
'data': [
    'security/ir.model.access.csv',
    'data/fahriza_library_data.xml',
    'views/library_book_views.xml',
    'views/res_partner_views.xml',
],
```

> **Catatan:** Karena view `view_partner_form` berasal dari modul `Contacts`, pastikan modul tersebut sudah terinstal. Tambahkan `'contacts'` ke `depends` di manifest jika perlu.

### 5.3. Domains

**Domain** digunakan untuk **membatasi atau memfilter data** yang ditampilkan pada field relasi, view, atau action.

#### Sintaks Domain

Domain adalah list of tuples, di mana setiap tuple berisi `(field, operator, value)`:

```python
# Domain sederhana
[('available', '=', True)]

# Multiple conditions (implicit AND)
[('available', '=', True), ('price', '>', 50000)]

# OR condition — gunakan operator '|' (prefix notation / Polish notation)
['|', ('name', 'ilike', 'python'), ('name', 'ilike', 'odoo')]

# Kombinasi AND dan OR
['|', ('price', '>', 100000), '&', ('available', '=', True), ('category_id.name', '=', 'Teknologi')]
```

#### Operator Domain yang Tersedia

| Operator     | Keterangan                          | Contoh                                   |
|--------------|-------------------------------------|------------------------------------------|
| `=`          | Sama dengan                         | `('state', '=', 'draft')`               |
| `!=`         | Tidak sama dengan                   | `('state', '!=', 'done')`               |
| `>`          | Lebih besar                         | `('price', '>', 100000)`                |
| `>=`         | Lebih besar atau sama               | `('price', '>=', 100000)`               |
| `<`          | Lebih kecil                         | `('price', '<', 50000)`                 |
| `<=`         | Lebih kecil atau sama               | `('price', '<=', 50000)`                |
| `like`       | Pattern match (case sensitive)      | `('name', 'like', 'Odoo%')`             |
| `ilike`      | Pattern match (case insensitive)    | `('name', 'ilike', 'odoo')`             |
| `in`         | Ada di dalam list                   | `('state', 'in', ['draft', 'confirm'])` |
| `not in`     | Tidak ada di dalam list             | `('state', 'not in', ['cancel'])`       |
| `child_of`   | Termasuk child di hierarchy         | `('category_id', 'child_of', 5)`        |
| `parent_of`  | Termasuk parent di hierarchy        | `('category_id', 'parent_of', 5)`       |

#### Penggunaan Domain

**Pada field Many2one (membatasi pilihan dropdown):**

```python
category_id = fields.Many2one(
    'library.category',
    string="Kategori",
    domain="[('name', '!=', 'Arsip')]",  # string → evaluated client-side
)
```

**Pada action window (filter data yang ditampilkan):**

```xml
<record id="action_available_books" model="ir.actions.act_window">
    <field name="name">Buku Tersedia</field>
    <field name="res_model">library.book</field>
    <field name="view_mode">list,form</field>
    <field name="domain">[('available', '=', True)]</field>
</record>
```

**Pada search view (filter predefined):**

```xml
<filter string="Harga > 100rb" name="expensive"
        domain="[('price', '>', 100000)]"/>
```

---

## Ringkasan Hari Pertama

| Topik                    | Konsep Utama                                                   |
|--------------------------|----------------------------------------------------------------|
| **Arsitektur Odoo**      | Three-tier: Presentation (OWL), Application (Python/ORM), Database (PostgreSQL) |
| **Struktur Modul**       | `__manifest__.py`, `models/`, `views/`, `security/`, `data/`   |
| **ORM**                  | Model, Fields, CRUD, `search`, `browse`, `filtered`, `mapped`  |
| **Fields**               | Simple, Relational, Computed, Constraints                      |
| **Views**                | List, Form, Search — deklarasi XML dengan `ir.ui.view`         |
| **Security**             | `ir.model.access.csv` — ACL per group                         |
| **Relasi**               | `Many2one`, `One2many`, `Many2many`                            |
| **Inheritance**          | Model (`_inherit`), View (`inherit_id` + `xpath`)              |
| **Domains**              | Filter expression `[(field, operator, value)]`                 |
