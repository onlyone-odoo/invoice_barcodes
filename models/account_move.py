from odoo import models, fields, api
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64


class AccountMove(models.Model):
    _inherit = "account.move"

    barcode_image = fields.Binary(
        "Barcode Image", compute="_compute_barcode_image", store=True
    )

    @api.depends("name", "invoice_date")
    def _compute_barcode_image(self):
        for record in self:
            if record.name and record.invoice_date:
                invoice_number = record.name.replace("/", "")  # Ejemplo: 07032025
                date_str = record.invoice_date.strftime(
                    "%d/%m/%Y"
                )  # Ejemplo: 07/03/2025
                barcode_data = f"{invoice_number}{date_str}"
                EAN128 = barcode.get_barcode_class("ean128")
                ean = EAN128(barcode_data, writer=ImageWriter())
                buffer = BytesIO()
                ean.write(buffer)
                record.barcode_image = base64.b64encode(buffer.getvalue())
                buffer.close()
