from odoo import models, fields


class OpStudent(models.Model):
    _inherit = "op.student"

    charge_note_ids = fields.One2many("note.charge", "student_id", "Notas")
