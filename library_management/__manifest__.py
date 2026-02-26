{
    "name": "Library Management",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "summary": "Manage library books and rents",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/library_rent_wizard_views.xml",
        "views/library_book_views.xml",
        "views/library_rent_views.xml",
    ],
    "application": True,
    "installable": True,
}
