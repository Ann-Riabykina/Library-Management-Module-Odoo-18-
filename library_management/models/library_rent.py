from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LibraryRent(models.Model):
    """
    Model: library.rent

    This model represents the process of renting a book by a partner.

    Fields required by the task:
      - partner_id (Many2one -> res.partner)
      - book_id (Many2one -> library.book)
      - rent_date (Date, automatically filled on creation)
      - return_date (Date, optional)

    Business rules implemented:
      1. A book cannot be rented twice simultaneously
         if it has not been returned yet.
      2. When a book is rented → library.book.is_available becomes False.
      3. When a book is returned → library.book.is_available becomes True.
    """

    _name = "library.rent"
    _description = "Library Rent"
    _order = "rent_date desc, id desc"

    # Partner (reader) who takes the book.
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Reader",
        required=True,
        ondelete="restrict",
        help="Partner who rents the book.",
    )

    # Book being rented.
    book_id = fields.Many2one(
        comodel_name="library.book",
        string="Book",
        required=True,
        ondelete="restrict",
        help="The book being rented.",
    )

    # Automatically set to today's date when record is created.
    rent_date = fields.Date(
        string="Rent Date",
        default=fields.Date.today,
        required=True,
        readonly=True,
        help="Date when the book was issued.",
    )

    # Empty means the book is still rented.
    return_date = fields.Date(
        string="Return Date",
        help="Date when the book was returned.",
    )

    # -------------------------------------------------------------------------
    # CONSTRAINT: Prevent double renting of the same book
    # -------------------------------------------------------------------------
    @api.constrains("book_id", "return_date")
    def _check_book_not_double_rented(self):
        """
        Ensure that the same book cannot be rented more than once
        at the same time.

        Active rent = record where return_date is False.

        For each record:
          - search another rent with the same book
          - exclude current record (id != self.id)
          - check if another active rent exists
        """
        for rent in self:
            if not rent.book_id:
                continue

            # If this rent is already closed, skip validation.
            if rent.return_date:
                continue

            conflict_count = self.search_count([
                ("id", "!=", rent.id),
                ("book_id", "=", rent.book_id.id),
                ("return_date", "=", False),
            ])

            if conflict_count:
                raise ValidationError(
                    _("This book is already rented and has not been returned yet.")
                )

    # -------------------------------------------------------------------------
    # CREATE override: mark book unavailable when rented
    # -------------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create() to update book availability.

        When a rent record is created:
          → the related book must become unavailable.
        """
        rents = super().create(vals_list)

        for rent in rents:
            if rent.book_id:
                rent.book_id.is_available = False

        return rents

    # -------------------------------------------------------------------------
    # WRITE override: restore availability when returned
    # -------------------------------------------------------------------------
    def write(self, vals):
        """
        Override write() to handle book return.

        If return_date is set:
          → book becomes available again.

        If return_date is cleared:
          → book becomes unavailable again (edge case but logically correct).
        """
        res = super().write(vals)

        if "return_date" in vals:
            for rent in self:
                if rent.book_id:
                    rent.book_id.is_available = bool(rent.return_date)

        return res

    def action_return_book(self):
        """
        UI action: return the book.

        This method is called from the 'Return Book' button on the rent form.
        It simply sets return_date to today (if not set yet).
        """
        for rent in self:
            # If already returned -> do nothing (idempotent action).
            if rent.return_date:
                continue

            rent.return_date = fields.Date.today()
