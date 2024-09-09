from odoo import models, fields


class OpStudentCourse(models.Model):
    _name = "sigu.student.inscription.line"
    _description = "Student Course Details"
    _rec_name = "subject_id"

    course_id = fields.Many2one(
        "op.course",
        "Course",
    )
    subject_id = fields.Many2one(
        "op.subject",
        string="Subjects",
    )
    batch_id = fields.Many2one(
        "op.batch",
        "Batch",
    )  # lote
    teacher_id = fields.Many2one(
        "op.faculty",
        "Teacher",
    )
    inscription_id = fields.Many2one(
        comodel_name="sigu.student.inscription",
        ondelete="restrict",
    )
