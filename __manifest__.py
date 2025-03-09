# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Invoice Barcodes",
    "summary": "Add barcodes to invoices with number, date, and line details",
    "description": """
        This module adds EAN128 barcodes to invoices in Odoo 16:
        - A general barcode with invoice number and date next to the invoice number.
        - A barcode per invoice line with invoice number, product reference, and quantity.
        - Includes a button to regenerate barcodes for existing invoices.
    """,
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "17.0.3.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": ["barcode"]},
    "post_init_hook": "post_init_hook",
    "depends": ["account"],
    "data": [
        "views/report_invoice_document.xml",
        "views/invoice_barcode_views.xml",
    ],
}
