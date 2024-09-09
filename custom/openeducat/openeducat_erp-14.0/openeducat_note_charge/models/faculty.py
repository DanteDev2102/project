from odoo import models, fields


class OpFaculty(models.Model):
    _inherit = "op.faculty"

    charge_note_ids = fields.One2many("note.charge", "faculty_id", "Notas")
