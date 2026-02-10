# Arkademy Prasmul ELI 18.0 - Day 2

**Topik:** Development Odoo 18 EE — Reporting, API & Repository Management

**Durasi:** 09.00 - 17.00 WIB

**Versi:** Odoo 18.0 Enterprise Edition

---

## Tujuan Pembelajaran

Pada akhir sesi hari kedua, peserta diharapkan mampu:

1. **Mendefinisikan** paper format kustom untuk mengatur ukuran kertas, margin, dan orientasi pada laporan PDF.
2. **Membangun** report template menggunakan QWeb dengan data dinamis dari model ORM, termasuk penggunaan directive `t-foreach`, `t-if`, `t-esc`, dan `t-field`.
3. **Mendaftarkan** report action (`ir.actions.report`) agar laporan PDF dapat diakses dari tombol Print pada form view.
4. **Membuat** pivot view untuk analisis data dan meng-enhance pivot view bawaan Sales Analysis (`sale.report`) dengan field kustom.
5. **Mengintegrasikan** aplikasi eksternal dengan Odoo melalui JSON-RPC API untuk melakukan operasi CRUD (`create`, `write`, `unlink`, `search_read`, `browse`).
6. **Mengimplementasikan** custom method pada model Odoo dan memanggilnya melalui JSON-RPC dari aplikasi eksternal.
7. **Mengelola** repository Git dengan strategi branching yang terstruktur dan membuat Pull Request untuk code review.

---

## 10. Reporting

Odoo menyediakan engine reporting berbasis **QWeb** untuk menghasilkan laporan dalam format PDF (melalui `wkhtmltopdf`) maupun HTML. Selain itu, Odoo juga memiliki **pivot view** untuk analisis data secara interaktif.

### 10.1. New Report (PDF)

Membuat laporan PDF kustom memerlukan tiga komponen utama:

1. **Paper Format** — Mengatur ukuran kertas, margin, dan orientasi.
2. **Report Template** — QWeb template yang mendefinisikan layout dan konten laporan.
3. **Report Action** — Mendaftarkan laporan agar bisa dipanggil dari UI (tombol Print).

#### 10.1.1. Paper Format

Paper format mengontrol properti fisik cetakan laporan. Odoo sudah menyediakan beberapa format bawaan, namun kita bisa membuat format kustom.

**File:** `data/report_paperformat.xml`

```xml
<odoo>
    <record id="paperformat_library_report" model="report.paperformat">
        <field name="name">Library Report Format</field>
        <field name="default" eval="False"/>
        <field name="format">A4</field>
        <field name="orientation">Portrait</field>
        <field name="margin_top">40</field>
        <field name="margin_bottom">28</field>
        <field name="margin_left">7</field>
        <field name="margin_right">7</field>
        <field name="header_line" eval="False"/>
        <field name="header_spacing">35</field>
        <field name="dpi">90</field>
    </record>
</odoo>
```

**Penjelasan field `report.paperformat`:**

| Field             | Tipe      | Keterangan                                                    |
|-------------------|-----------|---------------------------------------------------------------|
| `name`            | Char      | Nama deskriptif paper format                                  |
| `default`         | Boolean   | Jika `True`, menjadi default untuk semua report di database   |
| `format`          | Selection | Ukuran kertas: `A0`-`A9`, `B0`-`B10`, `Letter`, `Legal`, `Ledger`, `custom` |
| `orientation`     | Selection | `Portrait` atau `Landscape`                                   |
| `margin_top`      | Integer   | Margin atas dalam mm                                          |
| `margin_bottom`   | Integer   | Margin bawah dalam mm                                         |
| `margin_left`     | Integer   | Margin kiri dalam mm                                          |
| `margin_right`    | Integer   | Margin kanan dalam mm                                         |
| `header_line`     | Boolean   | Tampilkan garis di bawah header                               |
| `header_spacing`  | Integer   | Jarak header ke konten dalam mm                               |
| `dpi`             | Integer   | Resolusi output (default 90)                                  |
| `page_width`      | Integer   | Lebar halaman dalam mm (hanya jika `format='custom'`)         |
| `page_height`     | Integer   | Tinggi halaman dalam mm (hanya jika `format='custom'`)        |

> **Tips:** Jika ingin membuat format khusus (misal kartu, label, atau struk), gunakan `format='custom'` lalu isi `page_width` dan `page_height` secara manual.

#### 10.1.2. Report Template (QWeb)

QWeb adalah template engine XML milik Odoo. Report template ditulis sebagai QWeb template dan dirender menjadi HTML, lalu dikonversi ke PDF oleh `wkhtmltopdf`.

**File:** `report/library_book_report_template.xml`

```xml
<odoo>
    <!-- Template Report Daftar Buku -->
    <template id="report_library_book_document">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <h2>Detail Buku</h2>

                        <div class="row mt-3">
                            <div class="col-6">
                                <table class="table table-sm table-bordered">
                                    <tr>
                                        <th style="width: 40%;">Judul</th>
                                        <td><t t-esc="doc.name"/></td>
                                    </tr>
                                    <tr>
                                        <th>ISBN</th>
                                        <td><t t-esc="doc.isbn or '-'"/></td>
                                    </tr>
                                    <tr>
                                        <th>Kategori</th>
                                        <td><t t-esc="doc.category_id.name or '-'"/></td>
                                    </tr>
                                    <tr>
                                        <th>Tanggal Terbit</th>
                                        <td>
                                            <t t-if="doc.published_date">
                                                <span t-field="doc.published_date"/>
                                            </t>
                                            <t t-else="">-</t>
                                        </td>
                                    </tr>
                                    <tr>
                                        <th>Harga</th>
                                        <td>
                                            Rp <t t-esc="'{:,.0f}'.format(doc.price)"/>
                                        </td>
                                    </tr>
                                    <tr>
                                        <th>Status</th>
                                        <td>
                                            <t t-if="doc.available">
                                                <span class="badge bg-success">Tersedia</span>
                                            </t>
                                            <t t-else="">
                                                <span class="badge bg-danger">Tidak Tersedia</span>
                                            </t>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </div>

                        <!-- Daftar Penulis -->
                        <t t-if="doc.author_ids">
                            <h4 class="mt-4">Penulis</h4>
                            <ul>
                                <t t-foreach="doc.author_ids" t-as="author">
                                    <li><t t-esc="author.name"/></li>
                                </t>
                            </ul>
                        </t>

                    </div>
                </t>
            </t>
        </t>
    </template>

    <!-- Template Report Katalog (semua buku dalam satu halaman) -->
    <template id="report_library_catalog_document">
        <t t-call="web.html_container">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2 class="text-center">Katalog Perpustakaan</h2>
                    <p class="text-center text-muted">
                        Dicetak pada: <t t-esc="context_timestamp(datetime.datetime.now()).strftime('%d/%m/%Y %H:%M')"/>
                    </p>

                    <table class="table table-sm table-bordered mt-4">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Judul</th>
                                <th>ISBN</th>
                                <th>Kategori</th>
                                <th>Penulis</th>
                                <th class="text-end">Harga</th>
                                <th class="text-center">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-foreach="docs" t-as="doc">
                                <tr>
                                    <td><t t-esc="doc_index + 1"/></td>
                                    <td><strong><t t-esc="doc.name"/></strong></td>
                                    <td><t t-esc="doc.isbn or '-'"/></td>
                                    <td><t t-esc="doc.category_id.name or '-'"/></td>
                                    <td>
                                        <t t-esc="', '.join(doc.author_ids.mapped('name')) or '-'"/>
                                    </td>
                                    <td class="text-end">
                                        Rp <t t-esc="'{:,.0f}'.format(doc.price)"/>
                                    </td>
                                    <td class="text-center">
                                        <t t-if="doc.available">Tersedia</t>
                                        <t t-else="">Tidak</t>
                                    </td>
                                </tr>
                            </t>
                        </tbody>
                    </table>

                    <div class="mt-3">
                        <strong>Total Buku:</strong> <t t-esc="len(docs)"/>
                    </div>
                </div>
            </t>
        </t>
    </template>
</odoo>
```

**QWeb Directive yang sering digunakan:**

| Directive          | Keterangan                                                   | Contoh                                         |
|--------------------|--------------------------------------------------------------|-------------------------------------------------|
| `t-esc`            | Output value sebagai text (escaped)                          | `<t t-esc="doc.name"/>`                        |
| `t-field`          | Output field dengan format sesuai tipe (tanggal, angka, dll) | `<span t-field="doc.published_date"/>`          |
| `t-raw`            | Output HTML tanpa escape (hati-hati XSS)                     | `<t t-raw="doc.description"/>`                  |
| `t-if` / `t-else`  | Conditional rendering                                        | `<t t-if="doc.available">...</t>`               |
| `t-foreach`/`t-as` | Loop iterasi                                                 | `<t t-foreach="docs" t-as="doc">...</t>`        |
| `t-set`            | Set variabel                                                 | `<t t-set="total" t-value="0"/>`                |
| `t-att-*`          | Dynamic attribute                                            | `<div t-att-class="'badge ' + badge_class"/>`   |
| `t-call`           | Panggil template lain                                        | `<t t-call="web.external_layout">...</t>`       |

**Template penting dari Odoo:**

- `web.html_container` — Wrapper HTML dasar (doctype, head, body).
- `web.basic_layout` — Layout dasar dengan struktur halaman minimal (tanpa branding).
- `web.external_layout` — Layout dengan header & footer perusahaan (logo, alamat, dll).
- `web.internal_layout` — Layout minimalis tanpa header/footer perusahaan.

**Kapan menggunakan template mana?**

| Template             | Use Case                                          |
|----------------------|---------------------------------------------------|
| `web.html_container` | Kontrol penuh HTML, custom design dari awal      |
| `web.basic_layout`   | Laporan sederhana, butuh Bootstrap styling only   |
| `web.external_layout`| **Laporan resmi** untuk customer/vendor (default)|
| `web.internal_layout`| Memo internal, dokumen untuk kalangan sendiri     |

#### 10.1.3. Report Action

Report action mendaftarkan template sebagai laporan resmi yang bisa dipanggil dari tombol **Print** di form/list view.

**File:** `report/library_book_report_action.xml`

```xml
<odoo>
    <!-- Report per-Buku (satu halaman per record) -->
    <record id="action_report_library_book" model="ir.actions.report">
        <field name="name">Detail Buku</field>
        <field name="model">library.book</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">fahriza_library.report_library_book_document</field>
        <field name="report_file">fahriza_library.report_library_book_document</field>
        <field name="print_report_name">'Detail Buku - %s' % object.name</field>
        <field name="binding_model_id" ref="fahriza_library.model_library_book"/>
        <field name="binding_type">report</field>
        <field name="paperformat_id" ref="fahriza_library.paperformat_library_report"/>
    </record>

    <!-- Report Katalog (semua buku terpilih dalam satu dokumen) -->
    <record id="action_report_library_catalog" model="ir.actions.report">
        <field name="name">Katalog Perpustakaan</field>
        <field name="model">library.book</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">fahriza_library.report_library_catalog_document</field>
        <field name="report_file">fahriza_library.report_library_catalog_document</field>
        <field name="print_report_name">'Katalog Perpustakaan'</field>
        <field name="binding_model_id" ref="fahriza_library.model_library_book"/>
        <field name="binding_type">report</field>
        <field name="paperformat_id" ref="fahriza_library.paperformat_library_report"/>
    </record>
</odoo>
```

**Penjelasan field `ir.actions.report`:**

| Field                | Keterangan                                                       |
|----------------------|------------------------------------------------------------------|
| `name`               | Nama laporan (muncul di dropdown Print)                          |
| `model`              | Model sumber data                                                |
| `report_type`        | `qweb-pdf` (PDF) atau `qweb-html` (HTML langsung di browser)    |
| `report_name`        | XML ID dari QWeb template (format: `module.template_id`)         |
| `report_file`        | Biasanya sama dengan `report_name`                               |
| `print_report_name`  | Nama file PDF yang diunduh (bisa pakai ekspresi Python)          |
| `binding_model_id`   | Model yang akan menampilkan tombol Print                         |
| `binding_type`       | `report` agar muncul di dropdown Print                           |
| `paperformat_id`     | Referensi ke paper format kustom (opsional)                      |

#### 10.1.4. Registrasi di Manifest

```python
'data': [
    'security/ir.model.access.csv',
    'data/report_paperformat.xml',
    'report/library_book_report_action.xml',
    'report/library_book_report_template.xml',
    'views/library_book_views.xml',
    'views/library_category_views.xml',
    'views/library_author_views.xml',
],
```

> **Catatan:** Paper format harus dimuat sebelum report action, karena report action mereferensi paper format.

#### 10.1.5. Pivot View

Pivot view memungkinkan analisis data secara interaktif dalam format tabel pivot (seperti Pivot Table di Excel).

**Tambahkan di `views/library_book_views.xml`:**

```xml
<!-- Pivot View -->
<record id="view_library_book_pivot" model="ir.ui.view">
    <field name="name">library.book.pivot</field>
    <field name="model">library.book</field>
    <field name="arch" type="xml">
        <pivot string="Analisis Buku">
            <field name="category_id" type="row"/>
            <field name="available" type="col"/>
            <field name="price" type="measure"/>
        </pivot>
    </field>
</record>
```

Update `view_mode` pada action window:

```xml
<record id="action_library_book" model="ir.actions.act_window">
    <field name="name">Daftar Buku</field>
    <field name="res_model">library.book</field>
    <field name="view_mode">list,form,pivot</field>
</record>
```

**Atribut Pivot View:**

| Atribut           | Keterangan                                     |
|-------------------|-------------------------------------------------|
| `type="row"`      | Field digunakan sebagai baris (pengelompokan)   |
| `type="col"`      | Field digunakan sebagai kolom                   |
| `type="measure"`  | Field digunakan sebagai nilai yang diagregasi   |

### 10.2. Enhance Report (Sales Analysis — Pivot View)

Bagian ini membahas studi kasus nyata dari proyek ELI. Peserta akan memahami limitasi teknis pivot view Odoo dan cara mengatasinya.

#### 10.2.1. Permasalahan: Drill-Down Pivot Tidak Sesuai Ekspektasi

**Latar belakang:** Pada proyek ELI, setiap Sales Order memiliki daftar peserta (participant) yang tersimpan sebagai field `One2many` ke model `sale.participant`. Developer sudah berhasil menambahkan field **Total Participant** ke pivot view Sales Analysis (`sale.report`). Field ini menampilkan jumlah peserta per Sales Order.

**Masalah:** Saat user mengklik angka Total Participant di pivot view, yang muncul adalah list `sale.report` (Sales Analysis) — bukan list peserta. User mengharapkan dapat melihat daftar nama-nama peserta.

**Penyebab:** Ini adalah limitasi by-design dari pivot view di Odoo. Pivot view **selalu** melakukan drill-down ke model yang menjadi basis pivot view tersebut. Karena pivot view ini berbasis model `sale.report`, maka klik pada cell mana pun akan membuka list view `sale.report` dengan filter sesuai group-by yang aktif.

**Ilustrasi:**

```
Pivot View berbasis sale.report:
    │
    ├─ Klik "Total Revenue"      → List sale.report ✓ Sesuai harapan
    ├─ Klik "Quantity"           → List sale.report ✓ Sesuai harapan
    └─ Klik "Total Participant"  → List sale.report ✗ Harapan: list peserta!
```

Perilaku drill-down dihandle oleh OWL framework di frontend. Tidak ada konfigurasi atau hook untuk mengarahkan drill-down ke model berbeda per-measure.

**Kesimpulan 10.2.1:** Menambahkan field dari model lain (via JOIN SQL) ke `sale.report` memang bisa dilakukan, tapi drill-down akan tetap membuka list `sale.report`. Jika butuh drill-down ke detail data dari model lain, dibutuhkan solusi berbeda.

#### 10.2.2. Solusi: Reporting Model Terpisah untuk Analisis Peserta

Solusi yang tepat adalah membuat **reporting model terpisah** yang basis datanya sudah berada di level peserta (bukan level Sales Order). Dengan cara ini, drill-down dari pivot akan membuka list yang menampilkan data per-peserta.

**Langkah 1 — Definisi Model `sale.report.participant`:**

```python
# models/sale_report_participant.py
from odoo import fields, models


class SaleReportParticipant(models.Model):
    _name = "sale.report.participant"
    _description = "Sales Participant Analysis"
    _auto = False
    _rec_name = "participant_name"
    _order = "date desc"

    # Dimensi dari Sale Order
    order_id = fields.Many2one("sale.order", string="Sales Order", readonly=True)
    date = fields.Datetime(string="Order Date", readonly=True)
    customer_id = fields.Many2one("res.partner", string="Customer", readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)
    product_id = fields.Many2one("product.product", string="Product", readonly=True)
    team_id = fields.Many2one("crm.team", string="Sales Team", readonly=True)
    project_id = fields.Many2one("project.project", string="Project", readonly=True)

    # Dimensi Participant (nama peserta untuk ditampilkan)
    participant_partner_id = fields.Many2one("res.partner", string="Participant", readonly=True)
    participant_name = fields.Char(string="Participant Name", readonly=True)

    # Measure
    participant_count = fields.Integer(string="Jumlah Peserta", readonly=True)

    @property
    def _table_query(self):
        return """
            SELECT
                sp.id                           AS id,
                sp.sale_order_id                AS order_id,
                s.date_order                    AS date,
                s.partner_id                    AS customer_id,
                s.company_id                    AS company_id,
                s.team_id                       AS team_id,
                s.project_id                    AS project_id,
                sp.product_id                   AS product_id,
                sp.partner_id                   AS participant_partner_id,
                rp.name                         AS participant_name,
                1                               AS participant_count
            FROM sale_participant sp
                INNER JOIN sale_order s ON s.id = sp.sale_order_id
                INNER JOIN res_partner rp ON rp.id = sp.partner_id
        """
```

**Catatan penting terkait SQL query:**

- `_auto = False` → Odoo tidak membuat TABLE fisik, melainkan membuat **SQL VIEW**; data berasal dari SQL query (lihat perbandingan TABLE vs SQL VIEW di bawah).
- `_table_query` → Property yang mengembalikan SQL SELECT.
- **Setiap baris = 1 peserta** → Satu Sales Order dengan 5 peserta menghasilkan 5 baris.
- `participant_count = 1` per baris → Saat diagregasi (SUM), totalnya = jumlah peserta.
- **Tidak JOIN ke `sale_order_line`** → Jika di-JOIN, akan terjadi duplikasi. Contoh: 1 peserta × 3 order lines = 3 baris untuk peserta yang sama → angka jadi salah. Field `product_id` diambil langsung dari `sale_participant` (yang sudah menyimpan `product_id`).

---

**📌 Perbedaan TABLE vs SQL VIEW**

Memahami perbedaan ini penting karena `_auto = False` membuat Odoo **tidak** membuat TABLE, melainkan **SQL VIEW**.

| Aspek | TABLE | SQL VIEW |
|---|---|---|
| **Penyimpanan data** | ✅ Ya — data disimpan secara fisik di disk | ❌ Tidak — hanya menyimpan definisi query (SQL SELECT) |
| **Data di disk** | ✅ Ada file fisik di storage PostgreSQL | ❌ Tidak ada — data "virtual", dibaca dari tabel lain saat diakses |
| **INSERT / UPDATE / DELETE** | ✅ Bisa langsung | ❌ Tidak bisa secara default (kecuali menggunakan `INSTEAD OF` trigger atau `RULE`, jarang dipakai di Odoo) |
| **Sumber data** | Disimpan sendiri (self-contained) | Diambil dari satu atau lebih tabel lain melalui query |
| **Isi data** | Tetap (persistent) — data bertahan setelah restart | Selalu hasil query real-time — berubah otomatis mengikuti data sumber |
| **Performa** | Cepat untuk read/write karena data sudah tersimpan | Tergantung kompleksitas query yang mendasarinya. Query berat = akses lambat |
| **Penggunaan di Odoo** | Model dengan `_auto = True` (default) → `library.book`, `sale.order`, dll | Model dengan `_auto = False` + `_table_query` → `sale.report`, `sale.report.participant`, dll |
| **Cocok untuk** | Data transaksional, master data (CRUD) | Reporting, analisis, agregasi (read-only) |

**Analogi sederhana:**
- **TABLE** = buku catatan fisik. Data ditulis di kertas dan bisa dibaca kapan saja.
- **VIEW** = jendela kaca yang melihat ke buku catatan orang lain. Tidak menyimpan apa pun, tapi bisa "melihat" data dari tabel lain secara real-time.

**Di PostgreSQL**, saat Odoo menjalankan model `_auto = False` dengan `_table_query`, yang terjadi di database kurang lebih adalah:

```sql
-- Odoo TIDAK menjalankan ini:
CREATE TABLE sale_report_participant (...);

-- Odoo menjalankan ini:
CREATE OR REPLACE VIEW sale_report_participant AS
    SELECT sp.id AS id, ...
    FROM sale_participant sp
    INNER JOIN sale_order s ON s.id = sp.sale_order_id
    ...;
```

---

**Langkah 2 — Definisi Views (Pivot, List, Search):**

```xml
<!-- views/sale_report_participant_views.xml -->
<odoo>
    <!-- Pivot View -->
    <record id="view_sale_report_participant_pivot" model="ir.ui.view">
        <field name="name">sale.report.participant.pivot</field>
        <field name="model">sale.report.participant</field>
        <field name="arch" type="xml">
            <pivot string="Analisis Peserta">
                <field name="product_id" type="row" />
                <field name="team_id" type="row" />
                <field name="project_id" type="row" />
                <field name="participant_count" type="measure" />
            </pivot>
        </field>
    </record>

    <!-- List View -->
    <record id="view_sale_report_participant_list" model="ir.ui.view">
        <field name="name">sale.report.participant.list</field>
        <field name="model">sale.report.participant</field>
        <field name="arch" type="xml">
            <list string="Daftar Peserta" create="false" edit="false" delete="false">
                <field name="order_id" />
                <field name="date" />
                <field name="customer_id" />
                <field name="product_id" />
                <field name="team_id" />
                <field name="participant_name" />
            </list>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_sale_report_participant_search" model="ir.ui.view">
        <field name="name">sale.report.participant.search</field>
        <field name="model">sale.report.participant</field>
        <field name="arch" type="xml">
            <search string="Cari Peserta">
                <field name="participant_name" />
                <field name="customer_id" />
                <field name="product_id" />
                <field name="team_id" />
                <field name="project_id" />
                <field name="order_id" />   
                <separator />
                <group expand="0" string="Group By">
                    <filter string="Customer" name="groupby_customer"
                        context="{'group_by': 'customer_id'}" />
                    <filter string="Product" name="groupby_product"
                        context="{'group_by': 'product_id'}" />
                    <filter string="Sales Team" name="groupby_team"
                        context="{'group_by': 'team_id'}" />
                    <filter string="Project" name="groupby_project"
                        context="{'group_by': 'project_id'}" />
                        <filter string="Order Date" name="groupby_date"
                        context="{'group_by': 'date:month'}" />
                </group>
            </search>
        </field>
    </record>

    <!-- Action Window -->
    <record id="action_sale_report_participant" model="ir.actions.act_window">
        <field name="name">Participant Analysis</field>
        <field name="res_model">sale.report.participant</field>
        <field name="view_mode">pivot,list</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Tidak ada data peserta.
            </p>
            <p>
                Data peserta akan muncul setelah Sales Order memiliki participant.
            </p>
        </field>
    </record>

    <!-- Menu di bawah Sales > Reporting -->
    <menuitem
        id="menu_sale_report_participant"
        name="Participant Analysis"
        parent="sale.menu_sale_report"
        action="action_sale_report_participant"
        sequence="50" />
</odoo>
```

**Langkah 3 — Registrasi di `__init__.py` dan Manifest:**

File `models/__init__.py`:

```python
from . import sale_report_participant
```

File `__manifest__.py`:

```python
{
    'name': 'ELI Integration',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_report_participant_views.xml',
    ],
}
```

**Langkah 4 — Access Rights (`security/ir.model.access.csv`):**

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sale_report_participant_user,access.sale.report.participant,model_sale_report_participant,sales_team.group_sale_salesman,1,0,0,0
access_sale_report_participant_manager,access.sale.report.participant.manager,model_sale_report_participant,sales_team.group_sale_manager,1,0,0,0
```

Setelah upgrade modul, menu **Sales > Reporting > Participant Analysis** akan tersedia. Di pivot view ini:

- User dapat mengelompokkan peserta berdasarkan Product, Customer, atau tanggal.
- Saat mengklik angka peserta di pivot, drill-down akan membuka **list view `sale.report.participant`** yang menampilkan nama-nama peserta per baris.

> **Pelajaran utama:** Jika membutuhkan drill-down ke data detail dari model berbeda, **jangan** menambahkan field ke reporting model existing. Buat reporting model terpisah (`_auto = False`) yang basis datanya sudah pada level detail yang diinginkan.

## 11. API JSON-RPC

Odoo menyediakan **JSON-RPC** sebagai protokol untuk berkomunikasi dengan sistem eksternal. Semua operasi yang bisa dilakukan di UI Odoo juga bisa dilakukan melalui API ini — mulai dari autentikasi, CRUD, hingga memanggil custom method.

### 11.1. Konsep JSON-RPC di Odoo

JSON-RPC (Remote Procedure Call) menggunakan format JSON untuk mengirim request dan menerima response melalui HTTP POST.

**Endpoint utama:**

| Endpoint               | Kegunaan                                           |
|------------------------|----------------------------------------------------|
| `/web/session/authenticate` | Login dan mendapatkan session                  |
| `/web/dataset/call_kw`     | Memanggil method ORM (CRUD, custom method)     |
| `/web/dataset/search_read` | Search + Read dalam satu panggilan             |
| `/jsonrpc`                  | Generic JSON-RPC 2.0 endpoint                 |

**Struktur Request:**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 1,
    "params": {
        // parameter sesuai endpoint
    }
}
```

**Struktur Response (sukses):**

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        // data hasil
    }
}
```

**Struktur Response (error):**

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": 200,
        "message": "Odoo Server Error",
        "data": {
            "name": "odoo.exceptions.AccessError",
            "message": "Access Denied",
            ...
        }
    }
}
```

### 11.2. Authentication

Sebelum melakukan operasi apa pun, kita harus melakukan autentikasi untuk mendapatkan session ID.

**Request:**

```
POST {{base_url}}/web/session/authenticate
Content-Type: application/json
```

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 1,
    "params": {
        "db": "odoo18_training",
        "login": "admin",
        "password": "admin"
    }
}
```

**Response (sukses):**

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "uid": 2,
        "is_admin": true,
        "name": "Mitchell Admin",
        "username": "admin",
        "partner_id": 3,
        "db": "odoo18_training",
        ...
    }
}
```

> **Penting:** Session ID disimpan di cookie `session_id`. Postman otomatis mengelola cookie ini. Untuk aplikasi kustom, pastikan cookie dikirim di setiap request berikutnya.

### 11.3. Create

Membuat record baru menggunakan method `create`.

**Request:**

```
POST {{base_url}}/web/dataset/call_kw
```

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 2,
    "params": {
        "model": "library.book",
        "method": "create",
        "args": [
            {
                "name": "Belajar Odoo 18",
                "isbn": "ISBN-API-001",
                "price": 150000,
                "available": true
            }
        ],
        "kwargs": {}
    }
}
```

**Response:**

```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "result": 5
}
```

> `result` berisi ID record yang baru dibuat.

**Create Multiple Records:**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 2,
    "params": {
        "model": "library.book",
        "method": "create",
        "args": [
            [
                {
                    "name": "Buku Pertama via API",
                    "isbn": "ISBN-API-002",
                    "price": 85000
                },
                {
                    "name": "Buku Kedua via API",
                    "isbn": "ISBN-API-003",
                    "price": 120000
                }
            ]
        ],
        "kwargs": {}
    }
}
```

### 11.4. Write (Update)

Mengubah data record yang sudah ada menggunakan method `write`.

**Request:**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 3,
    "params": {
        "model": "library.book",
        "method": "write",
        "args": [
            [5],
            {
                "price": 175000,
                "available": false
            }
        ],
        "kwargs": {}
    }
}
```

> `args[0]` adalah list of IDs yang akan diupdate, `args[1]` adalah dict values.

**Response:**

```json
{
    "jsonrpc": "2.0",
    "id": 3,
    "result": true
}
```

### 11.5. Delete (Unlink)

Menghapus record menggunakan method `unlink`.

**Request:**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 4,
    "params": {
        "model": "library.book",
        "method": "unlink",
        "args": [[5]],
        "kwargs": {}
    }
}
```

**Response:**

```json
{
    "jsonrpc": "2.0",
    "id": 4,
    "result": true
}
```

### 11.6. Search

Mencari record berdasarkan domain filter menggunakan method `search`.

**Request:**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 5,
    "params": {
        "model": "library.book",
        "method": "search",
        "args": [
            [["available", "=", true]]
        ],
        "kwargs": {
            "limit": 10,
            "offset": 0,
            "order": "name asc"
        }
    }
}
```

**Response:**

```json
{
    "jsonrpc": "2.0",
    "id": 5,
    "result": [1, 2, 3]
}
```

> `result` berisi list of IDs yang cocok dengan domain.

#### Search + Read (search_read)

Cara paling efisien — search dan read dalam satu panggilan:

**Request:**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 6,
    "params": {
        "model": "library.book",
        "method": "search_read",
        "args": [
            [["available", "=", true]]
        ],
        "kwargs": {
            "fields": ["name", "isbn", "price", "category_id", "author_ids"],
            "limit": 10,
            "offset": 0,
            "order": "name asc"
        }
    }
}
```

**Response:**

```json
{
    "jsonrpc": "2.0",
    "id": 6,
    "result": [
        {
            "id": 1,
            "name": "Python untuk Pemula",
            "isbn": "ISBN1234567",
            "price": 120000,
            "category_id": [1, "Teknologi"],
            "author_ids": [1, 2]
        },
        ...
    ]
}
```

> **Catatan:** Field `Many2one` dikembalikan sebagai `[id, display_name]`. Field `Many2many`/`One2many` dikembalikan sebagai list of IDs.

### 11.7. Browse (Read)

Membaca detail record berdasarkan ID menggunakan method `read`.

**Request:**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 7,
    "params": {
        "model": "library.book",
        "method": "read",
        "args": [[1, 2]],
        "kwargs": {
            "fields": ["name", "isbn", "price", "available", "category_id"]
        }
    }
}
```

**Response:**

```json
{
    "jsonrpc": "2.0",
    "id": 7,
    "result": [
        {
            "id": 1,
            "name": "Python untuk Pemula",
            "isbn": "ISBN1234567",
            "price": 120000,
            "available": true,
            "category_id": [1, "Teknologi"]
        },
        {
            "id": 2,
            "name": "Odoo Developer Guide",
            "isbn": "ISBN7654321",
            "price": 150000,
            "available": true,
            "category_id": [2, "Pemrograman"]
        }
    ]
}
```

### 11.8. Custom Method & Response

Kita bisa membuat method kustom di model Odoo dan memanggilnya melalui JSON-RPC.

#### 11.8.1. Definisi Custom Method di Python

```python
# models/models.py
from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Data Buku Perpustakaan'

    name = fields.Char("Judul Buku", required=True)
    isbn = fields.Char("ISBN")
    price = fields.Float("Harga")
    available = fields.Boolean("Tersedia", default=True)
    category_id = fields.Many2one('library.category', string="Kategori")
    author_ids = fields.Many2many('library.author', string="Penulis")

    @api.model
    def get_available_books_summary(self):
        """Custom method: mengembalikan ringkasan buku tersedia."""
        books = self.search([('available', '=', True)])
        return {
            'total_books': len(books),
            'total_value': sum(books.mapped('price')),
            'books': [
                {
                    'id': book.id,
                    'name': book.name,
                    'isbn': book.isbn or '',
                    'price': book.price,
                    'category': book.category_id.name or '',
                    'authors': book.author_ids.mapped('name'),
                }
                for book in books
            ],
        }

    def toggle_availability(self):
        """Custom method: toggle status ketersediaan buku (dipanggil pada recordset)."""
        for book in self:
            book.available = not book.available
        return {
            'status': 'success',
            'updated_books': [
                {'id': book.id, 'name': book.name, 'available': book.available}
                for book in self
            ],
        }
```

#### 11.8.2. Memanggil Custom Method via JSON-RPC

**Method `@api.model` (tanpa record spesifik):**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 8,
    "params": {
        "model": "library.book",
        "method": "get_available_books_summary",
        "args": [],
        "kwargs": {}
    }
}
```

**Method pada recordset (dengan ID):**

```json
{
    "jsonrpc": "2.0",
    "method": "call",
    "id": 9,
    "params": {
        "model": "library.book",
        "method": "toggle_availability",
        "args": [[1, 2]],
        "kwargs": {}
    }
}
```

> `args[0]` berisi list of IDs. Odoo akan memanggil method pada recordset yang berisi record dengan ID tersebut.

**Response:**

```json
{
    "jsonrpc": "2.0",
    "id": 9,
    "result": {
        "status": "success",
        "updated_books": [
            {"id": 1, "name": "Python untuk Pemula", "available": false},
            {"id": 2, "name": "Odoo Developer Guide", "available": false}
        ]
    }
}
```

#### 11.8.3. Perbedaan `@api.model` vs Method Biasa

| Aspek              | `@api.model`                        | Method Biasa (tanpa decorator)       |
|--------------------|-------------------------------------|--------------------------------------|
| `self`             | Empty recordset                     | Recordset berisi record spesifik     |
| `args` di JSON-RPC | `[]` (kosong)                      | `[[id1, id2, ...]]`                 |
| Use case           | Operasi global, tidak perlu record  | Operasi pada record tertentu         |
| Contoh             | `get_available_books_summary()`     | `toggle_availability()`              |

**Latihan:**

1. Import koleksi Postman yang disediakan (lihat file `postman_collection.json`).
2. Ubah variabel `base_url`, `db_name`, `login`, dan `password` sesuai environment Anda.
3. Jalankan request Authenticate untuk mendapatkan session.
4. Coba semua operasi CRUD (Create, Read, Search, Write, Unlink).
5. Buat custom method `get_books_by_category(category_name)` yang menerima nama kategori dan mengembalikan daftar buku dalam kategori tersebut.
6. Panggil custom method tersebut melalui Postman.

---

## 12. Repository Management

Pengelolaan repository yang baik sangat penting dalam development Odoo, terutama saat bekerja dalam tim. Bagian ini membahas strategi branching dan workflow Pull Request.

### 12.1. Branching

#### 12.1.1. Branching Strategy

Training ini menggunakan strategi **main — staging — branch kerja** untuk mengelola alur development:

```
main                          → Production-ready code (protected branch)
 │
staging                       → Testing & integration sebelum ke main
 │
 ├── dev/fahriza/library      → Branch kerja developer Fahriza
 ├── dev/budi/sales-report    → Branch kerja developer Budi
 └── fix/book-price-bug       → Branch kerja bugfix
```

**Penjelasan setiap branch:**

| Branch           | Fungsi                                                                 | Siapa yang merge?     |
|------------------|------------------------------------------------------------------------|-----------------------|
| `main`           | Kode final yang sudah teruji dan siap production/deploy                | Lead / Reviewer       |
| `staging`        | Tempat integrasi dan testing semua branch kerja sebelum masuk `main`   | Developer (via PR)    |
| `Branch kerja`     | Development aktif per-developer atau per-fitur                        | Developer             |

**Alur kerja:**

```
              ┌──────────────────────────────────────────────────┐
              │                    main                          │
              │         (production-ready, protected)            │
              └──────────────────┬───────────────────────────────┘
                                 ▲
                                 │  PR #2: branch kerja → main
                                 │  (setelah staging OK)
              ┌──────────────────┴───────────────────────────────┐
              │                  staging                         │
              │          (testing & integration)                 │
              └──────────────────┬───────────────────────────────┘
                                 ▲
                                 │  PR #1: branch kerja → staging
                                 │  (review & testing)
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
  dev/fahriza/library    dev/budi/report     fix/book-price-bug
    (branch kerja)       (branch kerja)        (branch kerja)
```

**Aturan penting:**

1. **Branch kerja selalu dibuat dari `main`** — agar baseline-nya bersih.
2. **PR pertama ke `staging`** — untuk testing dan integrasi dengan branch developer lain.
3. **Jika staging OK, PR kedua ke `main`** — dari branch kerja langsung ke `main` (bukan dari staging).
4. **Jangan commit langsung ke `main` atau `staging`** — semua perubahan harus melalui PR.

#### 12.1.2. Setup Branch Awal

```bash
# Pastikan main sudah up-to-date
git checkout main
git pull origin main

# Buat branch staging dari main (hanya dilakukan sekali oleh lead)
git checkout -b staging main
git push -u origin staging
```

#### 12.1.3. Workflow Harian Developer

```bash
# 1. Buat branch kerja dari main
git checkout main
git pull origin main
git checkout -b dev/fahriza/library-module

# 2. Kerjakan fitur, commit berkala
git add models/models.py views/library_book_views.xml
git commit -m "[ADD] fahriza_library: add book model and views"

# ... lanjut development ...
git add report/library_book_report_template.xml
git commit -m "[IMP] fahriza_library: add PDF report for books"

# 3. Push branch kerja ke remote
git push -u origin dev/fahriza/library-module

# 4. Buat PR ke staging (lihat bagian 12.2)

# 5. Setelah staging OK dan approved, buat PR ke main
```

**Jika perlu sync dengan perubahan terbaru dari `main`:**

```bash
git checkout dev/fahriza/library-module
git fetch origin
git rebase origin/main
# Resolve conflict jika ada, lalu:
git push --force-with-lease origin dev/fahriza/library-module
```

#### 12.1.4. Konvensi Penamaan Branch

| Prefix       | Kegunaan                          | Contoh                            |
|--------------|-----------------------------------|-----------------------------------|
| `dev/`       | Development per-developer         | `dev/fahriza/library-module`      |
| `feature/`   | Fitur baru (lintas developer)    | `feature/library-reporting`       |
| `fix/`       | Perbaikan bug                    | `fix/book-price-validation`       |

#### 12.1.5. Konvensi Commit Message Odoo

Odoo memiliki konvensi commit message yang khas:

```
[TAG] module_name: short description

Optional longer description explaining the change in detail.
```

**Tag yang umum digunakan:**

| Tag     | Keterangan                                          |
|---------|-----------------------------------------------------|
| `[IMP]` | Improvement — peningkatan fitur existing            |
| `[FIX]` | Fix — perbaikan bug                                |
| `[ADD]` | Add — penambahan fitur/modul baru                  |
| `[REM]` | Remove — penghapusan fitur/kode                    |
| `[REF]` | Refactor — perubahan kode tanpa mengubah behavior  |
| `[MOV]` | Move — pemindahan file/kode                        |
| `[MRG]` | Merge — merge branch                               |

**Contoh:**

```bash
git commit -m "[ADD] fahriza_library: initial library module with book model"
git commit -m "[IMP] fahriza_library: add pivot view and PDF report for books"
git commit -m "[FIX] fahriza_library: fix price validation allowing negative values"
```

### 12.2. Pull Request

Pull Request (PR) adalah mekanisme untuk meminta review dan approval sebelum menggabungkan kode. Dalam workflow kita, setiap branch kerja melewati **dua tahap PR**.

#### 12.2.1. Workflow Pull Request (Dua Tahap)

```
1. Buat branch kerja dari main
         ↓
2. Develop dan commit di branch kerja
         ↓
3. Push branch kerja ke remote
         ↓
4. ┌─────────────────────────────────────────────┐
   │  PR #1: branch kerja → staging              │
   │  - Code review oleh rekan tim               │
   │  - Testing di environment staging           │
   │  - Pastikan tidak ada conflict dengan        │
   │    branch developer lain                    │
   └──────────────────┬──────────────────────────┘
                      ↓
5. Review, perbaiki jika ada feedback
                      ↓
6. Merge PR #1 ke staging → Test di staging
                      ↓
7. ┌─────────────────────────────────────────────┐
   │  PR #2: branch kerja → main                 │
   │  - Final review oleh lead/reviewer          │
   │  - Pastikan sudah teruji di staging         │
   └──────────────────┬──────────────────────────┘
                      ↓
8. Merge PR #2 ke main → Done!
```

> **Kenapa PR kedua dari branch kerja ke main (bukan dari staging)?** Karena staging bisa berisi kode dari developer lain yang belum tentu siap masuk main. Dengan PR langsung dari branch kerja, kita bisa memilih fitur mana yang sudah siap di-merge ke production.

#### 12.2.2. PR #1 — Branch Kerja ke Staging

Setelah push branch, buat PR ke `staging`:

**Via GitHub CLI (`gh`):**

```bash
gh pr create \
    --title "[ADD] fahriza_library: library module with reporting" \
    --body "$(cat <<'EOF'
## Summary
- Menambahkan modul perpustakaan dengan model book, category, dan author
- Menambahkan PDF report dan pivot view
- Menambahkan JSON-RPC custom method

## Testing
- [ ] Install modul dan verifikasi semua menu muncul
- [ ] Buat data buku dan cetak PDF report
- [ ] Test JSON-RPC API menggunakan Postman collection

## Checklist
- [ ] Modul bisa diinstal tanpa error
- [ ] Modul bisa di-upgrade tanpa error
- [ ] Access rights sudah dikonfigurasi
- [ ] Commit message mengikuti konvensi Odoo
EOF
)" \
    --base staging
```

#### 12.2.3. PR #2 — Branch Kerja ke Main

Setelah PR #1 sudah di-merge ke staging dan testing berhasil:

```bash
gh pr create \
    --title "[MRG] fahriza_library: merge to main after staging OK" \
    --body "$(cat <<'EOF'
## Summary
Merge branch kerja ke main setelah berhasil diuji di staging.

## Staging Verification
- [x] PR ke staging sudah di-merge dan tested
- [x] Tidak ada regression di staging
- [x] Semua fitur berfungsi sesuai requirement
EOF
)" \
    --base main
```

#### 12.2.4. Checklist Sebelum PR

Sebelum membuat PR (baik ke staging maupun main), pastikan:

- [ ] Modul bisa diinstal tanpa error (`-i module_name`)
- [ ] Modul bisa di-upgrade tanpa error (`-u module_name`)
- [ ] Semua view bisa diakses dan berfungsi
- [ ] Tidak ada log warning/error di console Odoo
- [ ] Access rights sudah dikonfigurasi dengan benar
- [ ] Commit message mengikuti konvensi Odoo
- [ ] File `__manifest__.py` sudah lengkap (depends, data files)
- [ ] Tidak ada file yang tertinggal (cek `git status`)
- [ ] Branch sudah di-rebase ke `main` terbaru (tidak ada conflict)

**Latihan:**

1. Buat branch `staging` dari `main` (jika belum ada).
2. Buat branch kerja dengan nama `dev/namadepan/library-module` dari `main`.
3. Commit semua perubahan modul perpustakaan yang sudah dibuat dari Day 1 dan Day 2.
4. Push branch kerja ke remote repository.
5. Buat PR #1 dari branch kerja ke `staging`.
6. Review PR teman sekelompok dan berikan feedback.
7. Setelah staging OK, buat PR #2 dari branch kerja ke `main`.

---

## Ringkasan Hari Kedua

| Topik                    | Konsep Utama                                                          |
|--------------------------|-----------------------------------------------------------------------|
| **Paper Format**         | `report.paperformat` — ukuran, margin, orientasi, DPI                |
| **Report Template**      | QWeb directive (`t-esc`, `t-field`, `t-foreach`, `t-if`, `t-call`)   |
| **Report Action**        | `ir.actions.report` — `binding_model_id`, `report_type`, `paperformat_id` |
| **Pivot View**           | `type="row"`, `type="col"`, `type="measure"` — analisis interaktif   |
| **JSON-RPC Auth**        | `/web/session/authenticate` — login dan session management           |
| **JSON-RPC CRUD**        | `create`, `write`, `unlink`, `search`, `search_read`, `read`        |
| **Custom Method**        | `@api.model` vs method biasa — callable via JSON-RPC                 |
| **Git Branching**        | `main` → `staging` → branch kerja — commit message `[TAG]`          |
| **Pull Request**         | Dua tahap: branch kerja → staging → main, code review tiap tahap    |
