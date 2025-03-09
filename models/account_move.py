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
            if record.name and record.invoice_date and record.name != "/":
                invoice_number = record.name.replace("/", "")
                date_str = record.invoice_date.strftime("%d/%m/%Y")
                barcode_data = f"{invoice_number}{date_str}"
                GS1_128 = barcode.get_barcode_class(
                    "gs1_128"
                )  # Cambiado de "ean128" a "gs1_128"
                ean = GS1_128(barcode_data, writer=ImageWriter())
                buffer = BytesIO()
                ean.write(buffer)
                record.barcode_image = base64.b64encode(buffer.getvalue())
                buffer.close()

    def action_regenerate_barcodes(self):
        self._compute_barcode_image()
        self.invoice_line_ids._compute_line_barcode_image()
        return True
