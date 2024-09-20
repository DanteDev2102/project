from odoo import models, fields


class OpStudent(models.Model):
    _inherit = "op.student"

    traject = fields.Selection(
        [
            ("initial", "Initial"),
            ("one", "One"),
            ("two", "Two"),
            ("three", "Three"),
            ("four", "Four"),
        ],
        default="initial",
        required=True,
    )
