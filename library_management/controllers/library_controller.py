import json

from odoo import http
from odoo.http import request


class LibraryController(http.Controller):
    """
    Simple REST endpoint for the test task.

    URL:
      GET /library/books

    Returns:
      JSON array with all books and their availability status.

    Notes:
    - We use auth="public" so it works without login (as a real public API).
      If you want to require Odoo login, change auth="user".
    - We use sudo() because public users have no access rights by default.
      In real projects you would usually add authentication (API key, token, etc.)
      instead of sudo() + public access.
    """

    @http.route("/library/books",
                type="http",
                auth="public",
                methods=["GET"],
                csrf=False)
    def get_books(self, **kwargs):
        """
        Fetch all library.book records and return JSON response.

        type="http" + methods=["GET"] = classic REST-like controller.
        """
        books = request.env["library.book"].sudo().search([])

        payload = []
        for book in books:
            payload.append({
                "id": book.id,
                "name": book.name,
                "author": book.author or "",
                "published_date": book.published_date.isoformat()
                if book.published_date else None,
                "is_available": bool(book.is_available),
            })

        body = json.dumps(payload, ensure_ascii=False)

        return request.make_response(
            body,
            headers=[
                ("Content-Type", "application/json; charset=utf-8"),
            ],
        )
