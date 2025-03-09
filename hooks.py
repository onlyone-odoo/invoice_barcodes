# hooks.py
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Actualizar facturas existentes
    moves = env["account.move"].search(
        [("move_type", "in", ("out_invoice", "out_refund", "in_invoice", "in_refund"))]
    )
    moves._compute_barcode_image()

    # Actualizar líneas de factura existentes
    lines = env["account.move.line"].search(
        [("move_id", "in", moves.ids), ("product_id", "!=", False)]
    )
    lines._compute_line_barcode_image()
