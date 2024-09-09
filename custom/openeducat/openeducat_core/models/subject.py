# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api, _


class OpSubject(models.Model):
    _name = "op.subject"
    _inherit = "mail.thread"
    _description = "Subject"

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    grade_weightage = fields.Integer('Grade Weightage', required=True)

    type = fields.Selection(
        [('theory', 'Theory'), ('practical', 'Practical'),
         ('both', 'Both'), ('other', 'Other')],
        'Type', default="theory")

    semester = fields.Selection(
        [('one', 'One'), ('two', 'Two')],
        'Semester', default="one", required=True)

    duration_semester = fields.Selection(
        [('one', 'One'), ('two', 'Two')],
        'Duration Semester', default="one", required=True)

    traject = fields.Selection(
        [('initial', 'Initial'),('one', 'One'), ('two', 'Two'), ('three', 'Three'), ('four', 'Four')],
        'Traject', default="initial", required=True)

    semanal_hour = fields.Integer('Semanal hour', required=True)

    subject_type = fields.Selection(
        [('regular', 'Regular'), ('elective', 'Elective'), ('project', 'Project'), ('creditable', 'Creditable'),('community_service', 'Community service'),('professional_practice', 'Professional Practice')],
        'Subject Type', default="regular", required=True)

    department_id = fields.Many2one(
        'op.department', 'Department',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)

    course_ids = fields.Many2many('op.course', string='Course(s)')

    _sql_constraints = [
        ('unique_subject_code',
         'unique(code)', 'Code should be unique per subject!'),
    ]

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Subjects'),
            'template': '/openeducat_core/static/xls/op_subject.xls'
        }]
