from odoo import models, fields


class Enrollment(models.Model):
    _name = "op.enrollment"
    _description = "Enrollment"
    _rec_name = "student_id"

    student_id = fields.Many2one(
        "student.student",
        ondelete="restrict",
    )
    schelude_id = fields.Many2one(
        comodel_name="op.schedule",
        ondelete="restrict",
    )
    academic_year_id = fields.Many2one(
        "op.academic.year",
        ondelete="restrict",
    )
    academic_tearm_id = fields.Many2one(
        "op.academic.term",
        ondelete="restric",
    )
