from odoo import models, fields


class subject(models.Model):
    _inherit = "op.subject"

    schelude_ids = fields.One2many(
        comodel_name="op.schedule",
        inverse_name="inverse_field",
    )
