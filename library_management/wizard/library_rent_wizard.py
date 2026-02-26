from odoo import fields, models, _
from odoo.exceptions import UserError


class LibraryRentWizard(models.TransientModel):
    """
    TransientModel = temporary model used for wizards.

    This wizard allows the user to:
      1. Select a partner (reader)
      2. Confirm renting a selected book
      3. Create a library.rent record
    """

    _name = "library.rent.wizard"
    _description = "Library Rent Wizard"

    # User who takes the book
    partner_id = fields.Many2one(
        "res.partner",
        string="Reader",
        required=True,
    )

    def action_confirm(self):
        """
        Called when user clicks "Confirm" in wizard.

        Steps:
          - get active book from context
          - create rent record
          - book availability is updated by library.rent.create()
        """

        self.ensure_one()

        # active_id = ID of the book from which wizard was opened
        book_id = self.env.context.get("active_id")
        if not book_id:
            raise UserError(_("No active book found."))

        book = self.env["library.book"].browse(book_id)

        if not book.is_available:
            raise UserError(_("This book is already rented."))

        # Create rent record
        self.env["library.rent"].create({
            "partner_id": self.partner_id.id,
            "book_id": book.id,
        })

        return {"type": "ir.actions.act_window_close"}
