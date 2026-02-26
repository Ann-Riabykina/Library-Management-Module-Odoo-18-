from odoo import fields, models


class LibraryBook(models.Model):
    """
    Model: library.book

    This model represents a book in the library.

    According to the task requirements it must contain:
      - name (Char) – required title of the book
      - author (Char) – author name
      - published_date (Date) – publication date
      - is_available (Boolean) – indicates if the book is available for renting
    """

    _name = "library.book"
    _description = "Library Book"

    # Required field – the title of the book
    # 'required=True' ensures the record cannot be created without it
    name = fields.Char(string="Book Title", required=True)

    # Optional author name
    author = fields.Char(string="Author")

    # Date of publication
    published_date = fields.Date(string="Published Date")

    # Indicates whether the book is available
    # By default every new book is available
    is_available = fields.Boolean(string="Is Available", default=True)
