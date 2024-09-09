from odoo import models, fields

class Subject(models.Model):

    _inherit = "op.subject"

    inscription_line_id = fields.One2many(
        "sigu.student.inscription.line",
        "subject_id",
    )
