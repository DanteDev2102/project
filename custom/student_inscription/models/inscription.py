from odoo import fields, models


class OpInscription(models.Model):
    _name = "op.inscription"
    _description = " Student Inscription"
    _rec_name = "student_id"

    student_id = fields.Many2one(
        comodel_name="op.student",
        ondelete="restrict",
    )

    academic_year_id = fields.Many2one(
        "op.academic.year",
        ondelete="restrict",
    )
    academic_term_id = fields.Many2one(
        "op.academic.term",
        ondelete="restrict",
    )
    session_ids = fields.Many2many(
        "op.session",
    )

    student_id_number = fields.Char(
        related="student_id.id_number",
        readonly=True,
    )
