from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class OpSession(models.Model):
    _inherit = "op.session"

    student_inscription_ids = fields.Many2many(
        comodel_name="op.inscription",
    )
    subject_credits = fields.Integer(
        related="subject_id.grade_weightage",
        readonly=True,
    )
    subject_semester = fields.Selection(
        related="subject_id.semester",
        readonly=True,
    )
    subject_duration_semester = fields.Selection(
        related="subject_id.duration_semester",
        readonly=True,
    )
    subject_traject = fields.Selection(
        related="subject_id.traject",
        readonly=True,
    )
    start_hour = fields.Char(
        compute="_compute_start_hour",
    )
    end_hour = fields.Char(
        compute="_compute_end_hour",
    )

    n_student = fields.Integer(
        compute="_compute_student_register",
    )

    @api.depends("student_inscription_ids")
    def _compute_student_register(self):
        for record in self:
            record.n_student = len(record.student_inscription_ids)

    @api.depends("start_datetime")
    def _compute_start_hour(self):
        for record in self:
            if record.start_datetime:
                # Formatear la hora y los minutos en formato HH:MM
                hora_minutos = datetime.strftime(record.start_datetime, "%H:%M")
                record.start_hour = hora_minutos

    @api.depends("end_datetime")
    def _compute_end_hour(self):
        for record in self:
            if record.end_datetime:
                # Formatear la hora y los minutos en formato HH:MM
                hora_minutos = datetime.strftime(record.end_datetime, "%H:%M")
                record.end_hour = hora_minutos

    @api.constrains("student_inscription_ids")
    def _check_limit_student(self):
        for rec in self:
            if len(rec.student_inscription_ids) >= 30:
                raise ValidationError(
                    _("This section has reached the maximum number of students")
                )

    # se envian el id del registro al wizard
    def action_excel_data(self):
        return {
            "type": "ir.actions.act_window",
            "name": "My Wizard",
            "res_model": "op.session.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_session_id": self.id},
        }
