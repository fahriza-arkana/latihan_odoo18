from odoo import models, fields, api

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
    _name = 'library.book' # ini akan menjadi tabel dgn nama library_book
    _description = 'Data Buku Perpustakaan'
    _inherit = ['mail.thread']
    _order = 'name asc, published_date desc'
    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'ISBN harus unik! Tidak boleh ada dua buku dengan ISBN yang sama.'),
        ('price_positive', 'CHECK(price >= 0)', 'Harga tidak boleh negatif.'),
    ]

    # active = fields.Boolean("Active", default=True)
    name = fields.Char("Judul Buku", required=True, tracking=True)
    isbn = fields.Char("ISBN")
    published_date = fields.Date("Tanggal Terbit")
    price = fields.Float("Harga", digits=(10, 2))
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