from odoo import models, fields, api
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    line_barcode_image = fields.Binary(
        "Line Barcode Image", compute="_compute_line_barcode_image", store=True
    )

    @api.depends("move_id.name", "product_id.default_code", "quantity")
    def _compute_line_barcode_image(self):
        for line in self:
            if line.move_id.name and line.product_id:
                invoice_number = line.move_id.name.replace("/", "")
                product_ref = line.product_id.default_code or "0000"
                quantity = "{:.2f}".format(line.quantity)
                barcode_data = f"{invoice_number}{product_ref}{quantity}"
                EAN128 = barcode.get_barcode_class("ean128")
                ean = EAN128(barcode_data, writer=ImageWriter())
                buffer = BytesIO()
                ean.write(buffer)
                line.line_barcode_image = base64.b64encode(buffer.getvalue())
                buffer.close()
