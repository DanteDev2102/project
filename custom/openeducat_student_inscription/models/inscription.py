from odoo import fields, models, _, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


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

    # validacion de la isncripcion tanto del limite como de que no exista duplicidad
    @api.constrains("session_ids")
    def _check_limit_student(self):
        for rec in self:
            for session in rec.session_ids:
                # se llama a la session a ver si no esta llena
                if len(session.student_inscription_ids) > session.max_student:
                    raise ValidationError(
                        _("This section has reached the maximum number of students")
                    )
                # se valida que no se repita el estudiante en el salon
                for student in session.student_inscription_ids:
                    if student.student_id.id_number == rec.student_id.id_number:
                        raise ValidationError(
                            _(
                                "This student has alredy inscripted in this subject: %s"
                                % session.name
                            )
                        )
