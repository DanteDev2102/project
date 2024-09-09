import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)


class OpStudentInscription(models.Model):
    _name = "sigu.student.inscription"
    _description = "Student Course Details"
    _rec_name = "student_id"

    student_id = fields.Many2one(
        "op.student", "Student", ondelete="cascade", tracking=True
    )
    academic_years_id = fields.Many2one("op.academic.year", "Academic Year")  #
    academic_term_id = fields.Many2one("op.academic.term", "Terms")
    state = fields.Selection(
        [("running", "Running"), ("finished", "Finished")],
        string="Status",
        default="running",
    )
    inscription_ids = fields.One2many(
        comodel_name="sigu.student.inscription.line",
        inverse_name="inscription_id",
    )
