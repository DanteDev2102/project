from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Schedule(models.Model):
    _name = "op.schedule"
    _description = "Schedule"
    _rec_name = "subject_id"

    enrollment_ids = fields.One2many(
        comodel_name="op.enrollment",
        inverse_name="schelude_id",
    )

    name = fields.Char("Name")
    start_time = fields.Datetime("Start Time")
    end_time = fields.Datetime("End Time")
    day_of_week = fields.Selection(
        [
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
            ("sunday", "Sunday"),
        ],
    )
    subject_id = fields.Many2one(
        "op.subject",
        ondelete="restric",
    )
    room_id = fields.Many2one(
        "op.classroom",
        ondelete="restric",
    )
    teacher_id = fields.Many2one(
        "op.student", "Teacher", domain="[('groups_id', 'in', user_group_id)]"
    )
    academic_year_id = fields.Many2one(
        "op.academic.year",
        ondelete="restrict",
    )
    academic_tearm_id = fields.Many2one(
        "op.academic.term",
        ondelete="restric",
    )
    max_students = fields.Integer("Maximum Students", default=30)
    current_students = fields.Integer(
        "Current Students", compute="_compute_current_students"
    )
    flr = fields.Boolean(string="La Floresta", default=False)
    alt = fields.Boolean(string="Altagracia", default=False)
    urb = fields.Boolean(string="La Urbina", default=False)
    gcy = fields.Boolean(string="La Guaira - Carayaca", default=False)

    @api.constrains("start_time", "end_time", "teacher_id", "academic_term_id")
    def _check_schedule_overlap(self):
        for schedule in self:
            conflicting_schedules = self.search(
                [
                    ("id", "!=", schedule.id),
                    ("teacher_id", "=", schedule.teacher_id),
                    ("academic_term_id", "=", schedule.academic_term_id),
                    ("start_time", "<", schedule.end_time),
                    ("end_time", ">", schedule.start_time),
                ]
            )
            if conflicting_schedules:
                raise ValidationError(
                    "The schedule overlaps with another schedule for the same teacher in the same academic term."
                )

    @api.depends("enrollment_ids")
    def _compute_current_students(self):
        for schedule in self:
            schedule.current_students = len(schedule.enrollment_ids)

    @api.constrains("schedule_id")
    def _check_schedule_capacity(self):
        for enrollment in self:
            if (
                len(enrollment.schedule_id.enrollment_ids)
                > enrollment.schedule_id.max_students
            ):
                raise ValidationError("The schedule has reached its maximum capacity.")
