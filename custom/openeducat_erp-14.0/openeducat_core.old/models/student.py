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

#Variable global para selección Si/No
YES_NOT = [
    ('y', 'Yes'),
    ('n', 'No')
]

#Variable global para selección Turno 
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

    """_sql_constraints es una variable en el modelo de Odoo que se utiliza para definir restricciones de integridad de datos en la base de datos. 
    Las restricciones se definen como una lista de tuplas, donde cada tupla contiene tres elementos:
        1-El nombre de la restricción
        2-Una expresión que describe la restricción
        3-Un mensaje de error que se mostrará si la restricción falla"""
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

    """el método get_import_templates se utiliza para proporcionar plantillas de importación para detalles de cursos de estudiantes en el módulo openeducat_core de Odoo.
    El decorador @api.model indica que el método es un método de clase que no tiene acceso a registros específicos, sino solo a la clase de modelo en sí"""
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

    """fields.Char es un tipo de campo en Odoo que se utiliza para almacenar cadenas de texto de longitud fija en un modelo de datos de Odoo"""
    first_name = fields.Char(size=255, translate=True)
    middle_name = fields.Char(size=255, translate=True)
    last_name = fields.Char(size=255, translate=True)
    second_last_name = fields.Char(size=255, translate=True)
    mobile = fields.Char(size=11, translate=True)
    email = fields.Char(translate=True)
    visa_info = fields.Char(size=64)
    id_number = fields.Char('Identity Card', size=64)
    gr_no = fields.Char("GR Number", size=20)

    """fields.Date es un tipo de campo en Odoo que se utiliza para almacenar fechas en un modelo de datos de Odoo"""
    birth_date = fields.Date()
    registration_date = fields.Date()

    """fields.Selection es un campo de selección que permite al usuario elegir una opción predefinida de una lista de opciones """
    headquarters = fields.Selection([
        ('FLR', 'La Floresta'),    
        ('ALT', 'Altagracia'),
        ('URB', 'La Urbina'),
        ('GCY', 'La Guaira - Carayaca')
    ], 'Headquarters', required=True)

    pnf = fields.Selection([
        ('PA', 'PNF en Administración'),    
        ('PCP', 'PNF en Contaduría Pública'),
        ('PDL', 'PNF en Distribución y Logística'),
        ('PE', 'PNF en Educación Especial'),
        ('PINF', 'PNF en Ingeniería Informática'),
        ('PT', 'PNF en Turismo')
    ], 'PNF', required=True)

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
        ('f', 'Female')
    ], 'Gender', required=True)

    disability = fields.Selection(YES_NOT, 'Disability', required=True)
    turn = fields.Selection(TURN, required=True)
    
    """fields.Boolean es un tipo de campo en Odoo que se utiliza para almacenar valores booleanos (verdadero o falso) en un modelo de datos de Odoo"""
    active = fields.Boolean(default=True)
    
    """fields.Binary es un tipo de campo en Odoo que se utiliza para almacenar datos binarios (como imágenes, archivos PDF, documentos de Word, archivos de audio, etc.) 
    en un modelo de datos de Odoo. Se puede utilizar para permitir a los usuarios cargar y descargar archivos adjuntos en los registros de la base de datos"""    
    id_number_pdf = fields.Selection(YES_NOT, required=True, default='n')
    id_number_pdf_binary = fields.Binary(required=False)
    passport_type_photo = fields.Selection(YES_NOT, required=True, default='n')
    passport_type_photo_binary = fields.Binary(required=False)
    birth_certificate = fields.Selection(YES_NOT, required=True, default='n')
    birth_certificate_binary = fields.Binary(required=False)
    high_school_diploma = fields.Selection(YES_NOT, required=True, default='n')
    high_school_diploma_binary = fields.Binary(required=False)
    certificate_note = fields.Selection(YES_NOT, required=True, default='n')
    certificate_note_binary = fields.Binary(required=False)
    opsu = fields.Selection(YES_NOT, required=True, default='n')
    opsu_binary = fields.Binary(required=False)
    rif = fields.Selection(YES_NOT, required=True, default='n')
    rif_binary = fields.Binary(required=False)

    """fields.Many2one es un tipo de campo en Odoo que se utiliza para establecer una relación de muchos a uno entre dos modelos de datos. 
    Se puede utilizar para permitir a los usuarios seleccionar un registro de otro modelo relacionado y establecer una relación entre ellos."""
    country_id = fields.Many2one('res.country', default=_set_default_country_id)
    nationality = fields.Many2one('res.country')
    emergency_contact = fields.Many2one('res.partner')
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    category_id = fields.Many2one('op.category', 'Category')
    course_detail_ids = fields.One2many('op.student.course', 'student_id',
                                        'Course Details',
                                        tracking=True)

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'GR Number must be unique per student!'
    )]

    """El decorador @api.onchange se puede aplicar a un método que se definirá en una clase de modelo de Odoo. 
    Cuando se aplica el decorador a un método, se especifica una lista de nombres de campos que se deben observar para detectar los cambios
    y desencadenar la ejecución del método"""
    @api.onchange('first_name', 'middle_name', 'last_name', 'second_last_name')
    def _onchange_name(self):
        """def _onchange_name(self): es una definición de método en Python que se utiliza para crear una función que se ejecutará automáticamente 
        cuando el valor del campo name cambie en un registro del modelo al que pertenece el método"""
        self.name = f'{self.first_name} {self.last_name}'
        if self.middle_name and not self.second_last_name:
            self.name = f'{self.first_name} {self.middle_name} {self.last_name}'
        elif self.second_last_name and not self.middle_name:
            self.name = f'{self.first_name} {self.last_name} {self.second_last_name}'
        elif self.second_last_name and self.middle_name:
            self.name = f'{self.first_name} {self.middle_name} {self.last_name} {self.second_last_name}'

    @api.onchange('state_id')
    def clear_state(self):
        """Limpiar los campos de Municipio y Parroquia al cambiar el Estado"""
        for rec in self:
            rec.municipality_id = False
            rec.parish_id = False

    @api.onchange('municipality_id')
    def clear_municipality(self):
        """Limpiar los campos de Parroquia al cambiar el Municipio"""
        for rec in self:
            rec.parish_id = False
            
    """@api.constrains('birth_date') es un decorador en Odoo que se utiliza para definir una restricción que se aplicará a un campo específico en un modelo de Odoo. 
    La restricción se ejecutará automáticamente cada vez que se intente guardar o actualizar un registro en el modelo que tenga un valor no válido en el campo especificado."""
    @api.constrains('birth_date')
    def _check_birthdate(self):
        """def _check_birthdate(self): es una definición de método en Python que se utiliza para crear una función personalizada que se puede llamar desde otros métodos en un modelo de Odoo"""
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.constrains('id_number_pdf', 'passport_type_photo', 'birth_certificate', 'high_school_diploma', 'certificate_note', 'opsu', 'rif')
    def _check_binary_fields(self):
        """_check_binary_fields es un método personalizado en un modelo de Odoo que se utiliza para verificar si los campos binarios en el registro actual cumplen con las condiciones de tamaño de archivo predefinidas"""
        for record in self:
            if self.id_number_pdf == 'y' and not self.id_number_pdf_binary:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Cédula".')
            if self.passport_type_photo == 'y' and not self.passport_type_photo_binary:
                raise ValidationError('Debe adjuntar un archivo PNG o JPEG para el campo "Foto Tipo Carnet".')
            if self.birth_certificate == 'y' and not self.birth_certificate_binary:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Acta de Nacimiento".')
            if self.high_school_diploma == 'y' and not self.high_school_diploma_binary:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Título de Bachiller".')
            if self.certificate_note == 'y' and not self.certificate_note_binary:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Notas Certificadas".')
            if self.opsu == 'y' and not self.opsu_binary:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Certificado de Participación OPSU".')
            if self.rif == 'y' and not self.rif_binary:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "RIF".')
            
    """la línea de código for record in self: se utiliza en el método write de un modelo personalizado de Odoo para iterar sobre todos los registros que se están actualizando
    y realizar acciones específicas para cada uno de ellos antes de guardar los cambios en la base de datos"""
    def write(self, vals):
        for record in self:
            if 'id_number_pdf' in vals and vals['id_number_pdf'] == 'y' and 'id_number_pdf_binary' in vals and not vals['id_number_pdf_binary']:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Cédula".')
            if 'passport_type_photo' in vals and vals['passport_type_photo'] == 'y' and 'passport_type_photo_binary' in vals and not vals['passport_type_photo_binary']:
                raise ValidationError('Debe adjuntar un archivo PNG o JPEG para el campo "Foto Tipo Carnet".')
            if 'birth_certificate' in vals and vals['birth_certificate'] == 'y' and 'birth_certificate_binary' in vals and not vals['birth_certificate_binary']:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Acta de Nacimiento".')
            if 'high_school_diploma' in vals and vals['high_school_diploma'] == 'y' and 'high_school_diploma_binary' in vals and not vals['high_school_diploma_binary']:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Título de Bachiller".')
            if 'certificate_note' in vals and vals['certificate_note'] == 'y' and 'certificate_note_binary' in vals and not vals['certificate_note_binary']:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Notas Certificadas".')
            if 'opsu' in vals and vals['opsu'] == 'y' and 'opsu_binary' in vals and not vals['opsu_binary']:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "Certificado de Participación OPSU".')
            if 'rif' in vals and vals['rif'] == 'y' and 'rif_binary' in vals and not vals['rif_binary']:
                raise ValidationError('Debe adjuntar un archivo PDF para el campo "RIF".')
        return super(OpStudent, self).write(vals)

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
