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

"""`from odoo import models, fields, api, _`: Importa las clases y funciones necesarias de Odoo.
   - `models`: Clase base para crear modelos en Odoo.
   - `fields`: Clase para definir campos en los modelos de Odoo.
   - `api`: Decoradores para controlar el comportamiento de los métodos en Odoo.
   - `_`: Función para la traducción de cadenas de texto en Odoo. """

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

#Lista constante para selección Si/No
YES_NOT = [
    ('y', 'Yes'),
    ('n', 'No')
]


#Lista constante para selección de Turno 
TURN = [
    ('m', 'Morning'),
    ('e', 'Evening'),
    ('n', 'Night'),
    ('me', 'Morning - Evening'),
    ('mn', 'Morning - Night'),
    ('en', 'Evening - Night'),
    ('men', 'Morning - Evening - Night')
]

"""Esta clase es una subclase del modelo models.Model de Odoo y se utiliza para definir una relación
many-to-many entre los modelos op.student y op.course.En resumen, la clase OpStudentCourse se utiliza para registrar 
la información de los cursos que un estudiante está tomando en una institución educativa. En otras palabras, 
se utiliza para crear una relación entre un estudiante y los cursos en los que está matriculado. """

class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "Student Course Details"
    _inherit = "mail.thread"
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'Student', ondelete="cascade", tracking=True)
    course_id = fields.Many2one('op.course', 'Course', required=True, tracking=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True, tracking=True)
    roll_number = fields.Char('Roll Number', tracking=True)
    subject_ids = fields.Many2many('op.subject', string='Subjects')
    academic_years_id = fields.Many2one('op.academic.year', 'Academic Year')
    academic_term_id = fields.Many2one('op.academic.term', 'Terms')
    state = fields.Selection([('running', 'Running'),
                              ('finished', 'Finished')],
                             string="Status", default="running")

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(roll_number,course_id,batch_id,student_id)',
         'Roll Number & Student must be unique per Batch!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,batch_id)',
         'Roll Number must be unique per Batch!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Student Course Details'),
            'template': '/openeducat_core/static/xls/op_student_course.xls'
        }]
        
""" La siguiente clase OpStudent es una subclase del modelo models.Model de Odoo y se utiliza para definir el modelo op.student, 
que se utiliza para almacenar la información de los estudiantes en una institución educativa.
La clase OpStudent define varios campos para almacenar información personal del estudiante, 
como el nombre, apellido, fecha de nacimiento, género,sexo, dirección, correo electrónico, número de teléfono, etc. 
Además, también se definen campos para almacenar información adicional, como la foto del estudiante, la cédula
del estudiante y el núcleo al que pertenece. """

class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}

    def _set_default_country_id(self):
        return self.env.ref('base.ve').id

    country_id = fields.Many2one('res.country', default=_set_default_country_id)
    first_name = fields.Char(size=128, translate=True)
    middle_name = fields.Char(size=128, translate=True)
    last_name = fields.Char(size=128, translate=True)
    second_last_name = fields.Char(size=128, translate=True)
    birth_date = fields.Date()
    mobile = fields.Char(size=15, translate=True)
    email = fields.Char(size=128, translate=True)
    nro_folio = fields.Char(size=15, translate=True)
    nro_registro = fields.Char(size=15, translate=True)

    headquarters = fields.Selection([
        ('FLR', 'La Floresta'),    
        ('ALT', 'Altagracia'),
        ('URB', 'La Urbina'),
        ('GCY', 'La Guaira - Carayaca')
    ], 'Headquarters', required=True)

    registration_date = fields.Date()

    pnf = fields.Selection([
        ('PA', 'PNF en Administración'),    
        ('PCP', 'PNF en Contaduría Pública'),
        ('PDL', 'PNF en Distribución y Logística'),
        ('PE', 'PNF en Educación Especial'),
        ('PET', 'PNF en Educación Especial (Técnica)'),
        ('PINF', 'PNF en Informática'),
        ('PT', 'PNF en Turismo'),
        ('PEI', 'PNF en Educación Inicial'),
        ('PTS', 'PNF en Trabajo Social')
    ], 'PNF', required=True)

    inscrito = fields.Selection(YES_NOT, 'Inscrito', required=True)
    prosecucion = fields.Selection(YES_NOT, 'Prosecución', required=False)

    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')

    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('h', 'Hermaphrodite')
    ], 'Gender', required=False)

    disability = fields.Selection(YES_NOT, 'Disability', required=True)

    indigena = fields.Selection(YES_NOT, 'Población Indígena', required=False)
       
    id_number_pdf = fields.Selection(YES_NOT, required=False, default='n')
#    id_number_pdf_binary = fields.Binary()
    passport_type_photo = fields.Selection(YES_NOT, required=False, default='n')
#    passport_type_photo_binary = fields.Binary()
    birth_certificate = fields.Selection(YES_NOT, required=False, default='n')
#    birth_certificate_binary = fields.Binary()
    high_school_diploma = fields.Selection(YES_NOT, required=False, default='n')
#    high_school_diploma_binary = fields.Binary()
    certificate_note = fields.Selection(YES_NOT, required=False, default='n')
#    certificate_note_binary = fields.Binary()
    opsu = fields.Selection(YES_NOT, required=False, default='n')
#    opsu_binary = fields.Binary()
    rif = fields.Selection(YES_NOT, required=False, default='n')
#    rif_binary = fields.Binary()
    planilla_inscripcion = fields.Selection(YES_NOT, required=False, default='n')
#    planilla_inscripcion_binary = fields.Binary()
    const_trabajo = fields.Selection(YES_NOT, required=False, default='n')
#    const_trabajo_binary = fields.Binary()
    carnet_conapdis = fields.Selection(YES_NOT, required=False, default='n')
#    carnet_conapdis_binary = fields.Binary()
    autori_representante = fields.Selection(YES_NOT, required=False, default='n')
#    autori_representante_binary = fields.Binary()
    resma = fields.Selection(YES_NOT, required=True, default='n')
    marcadores = fields.Selection(YES_NOT, required=True, default='n')
    

    nationality = fields.Many2one('res.country')
    emergency_contact = fields.Many2one('res.partner')
    visa_info = fields.Char(size=64)
    id_number = fields.Char('Identity Card', size=64)
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    gr_no = fields.Char("GR Number", size=20)
    category_id = fields.Many2one('op.category', 'Category')
    course_detail_ids = fields.One2many('op.student.course', 'student_id',
                                        'Course Details',
                                        tracking=True)
    turn = fields.Selection(TURN)
    active = fields.Boolean(default=True)

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'GR Number must be unique per student!'
    )]

    @api.onchange('first_name', 'middle_name', 'last_name', 'second_last_name')
    def _onchange_name(self):
        self.name = f'{self.first_name} {self.last_name}'
        if self.middle_name and not self.second_last_name:
            self.name = f'{self.first_name} {self.middle_name} {self.last_name}'
        elif self.second_last_name and not self.middle_name:
            self.name = f'{self.first_name} {self.last_name} {self.second_last_name}'
        elif self.second_last_name and self.middle_name:
            self.name = f'{self.first_name} {self.middle_name} {self.last_name} {self.second_last_name}'

    @api.onchange('state_id')
    def clear_state(self):
        """Clear fields of municipality and parish when changing the state"""
        for rec in self:
            rec.municipality_id = False
            rec.parish_id = False

    @api.onchange('municipality_id')
    def clear_municipality(self):
        """Clear fields of parish when changing the municipality"""
        for rec in self:
            rec.parish_id = False

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/openeducat_core/static/xls/op_student.xls'
        }]

    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id
