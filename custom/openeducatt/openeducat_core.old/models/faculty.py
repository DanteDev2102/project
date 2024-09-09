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

#This is a Python code that imports three Odoo modules: models, fields and api, as well as two other Python modules, ValidationError and timedelta (to handle date and time objects) and relativedelta (to calculate differences between dates). These modules are necessary to define custom models in Odoo and to define certain behaviors within Odoo.
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta

YES_NOT = [
    ('y', 'Yes'),
    ('n', 'No')
]

#This code refers to a new entity being defined in OpenEduCat called "op.faculty". In this statement, it is indicated that this entity inherits from two models, "mail.thread" and "mail.activity.mixin", which means that the records created in this entity will be able to be tracked and thus increase the email notification capability for these records. In addition to that, "_inherits" is used to define the parent model that will be inherited. In this case, the parent model is "res.partner".
class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "OpenEduCat Faculty"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    #_set_default_country_id() is called as a default function to set the default value for country_id field, which refers to the employee's country of origin.
    def _set_default_country_id(self):
        return self.env.ref('base.ve').id
    #country_id: dropdown selection field for employee's country of origin.
    country_id = fields.Many2one('res.country', default=_set_default_country_id)
    #partner_id: reference many2one field for res.partner model that holds additional partner data like email, phone, address, etc.
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    #first_name, middle_name, last_name, and second_last_name: text fields for employee name.
    first_name = fields.Char(size=128, translate=True)
    middle_name = fields.Char(size=128)
    last_name = fields.Char(size=128,)    
    second_last_name = fields.Char(size=128,)
    #birth_date: date field for employee's birthdate.
    birth_date = fields.Date(required=False)
    #entry_date: date field for employee's company entry date.
    entry_date = fields.Date(required=True)
    #year_service: char field for the year when employee started their service.
    year_service = fields.Char(size=2)
    #number_year_service: computed integer field that calculates the total number of years of employee service.
    number_year_service = fields.Integer(compute='_compute_number_year_service')
    #pnfa, pnfc, pnfd, pnfe, pnfi, pnft, flr, alt, urb, and gcy: These are boolean fields representing different administrative departments to which the employee can belong.
    pnfa = fields.Boolean(string="Administración", default=False)
    pnfc = fields.Boolean(string="Contaduría Pública", default=False)
    pnfd = fields.Boolean(string="Distribución y Lógistica", default=False)
    pnfe = fields.Boolean(string="Educacion Especial", default=False)
    pnfi = fields.Boolean(string="Ingeniería Informática", default=False)
    pnft = fields.Boolean(string="Turismo", default=False)
    flr = fields.Boolean(string="La Floresta", default=False)
    alt = fields.Boolean(string="Altagracia", default=False)
    urb = fields.Boolean(string="La Urbina", default=False)
    gcy = fields.Boolean(string="La Guaira - Carayaca", default=False)
    #This is a selection field definition in Odoo. The field named "blood_group" is created with type "Selection". It has 8 options (blood types) to be displayed in the user interface and their respective response value (labels and values). The field label is set as "Blood Group". Users can select their blood type from the available options using this field.
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
    #This is defining a field named gender. It has Selection type widget, which indicates that it can have a value from a pre-defined list of options. Here, the available options are 'Male', 'Female', and 'Hermaphrodite'. These options are represented internally by their acronym or shorthand: 'm' for male, 'f' for female, and 'h' for hermaphrodite. The field is set to be required, so every employee record must have a value for gender.
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('h', 'Hermaphrodite')
    ], 'Gender', required=True)
    #This is a field definition code in Odoo that defines a dropdown field named "Dedication" with 4 choices for the user to select. The choices are "Conventional", "Part Time", "Full Time", and "Exclusive Dedication". Each choice is represented by a code letter inside parentheses. The required=False parameter means that this field may be left empty when creating or editing an object where it belongs.
    dedication = fields.Selection([
        ('c', 'Conventional'),
        ('m', 'Part Time'),
        ('t', 'Full Time'),
        ('d', 'Exclusive Dedication')
    ], 'Dedication', required=False)
    #This is a field "shift" with the Selection type that allows selecting shift timings like Morning, Evening, Night, and combinations of these. It has optional field attribute because it is not marked as mandatory since some employees may not work in shifts.
    shift = fields.Selection([
        ('m', 'Morning'),
        ('e', 'Evening'),
        ('n', 'Night'),
        ('me', 'Morning - Evening'),
        ('mn', 'Morning - Night'),
        ('en', 'Evening - Night'),
        ('men', 'Morning - Evening - Night')
    ], 'Shift', required=False)
    #This is a field definition for a selection type field named ladder with some options such as 'Instructor', 'Contracted', 'Assistant', 'Associate' etc.
    #The field will be displayed as a drop-down list on the view and user can select only one option from the list. The selected value will be stored in the database and could be used in different operations such as record filtering or calculation later.
    ladder = fields.Selection([
        ('I', 'Instructor'),    
        ('C', 'Contracted'),
        ('AS', 'assistant'),
        ('AD', 'added'),
        ('AS', 'associate'),
        ('H', 'headline')
    ], 'Ladder', required=False)
    #This is a field definition for a selection field named status_active. It allows the user to select whether the record is active or not by choosing one of the two options: "Yes" or "No". The values are stored in the database as either 'Y' or 'N', respectively. This field expects a required value to be selected at the time of creation of new records.
    status_active = fields.Selection(YES_NOT, 'Status_active', required=True)
    #This is a field definition for a selection field called disability. It allows the user to select whether the record is active or not by choosing one of two options: "Yes" or "No". The values are stored in the database as "Y" or "N", respectively. This field expects a mandatory value to be selected when creating new records.
    disability = fields.Selection(YES_NOT, 'Disability', required=True)
    #The code is defining multiple fields for the employee record.
    #nationality represents the country of citizenship of the employee.
    nationality = fields.Many2one('res.country', 'Nationality')
    #emergency_contact represents the emergency contact person for the employee.
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    #visa_info represents the visa information of the employee.
    visa_info = fields.Char('Visa Info', size=64)
    #id_number represents the ID card number of the employee.
    id_number = fields.Char('ID Card Number', size=64)
    #login represents the login name of the corresponding user in the system.
    login = fields.Char(
        'Login', related='partner_id.user_id.login', readonly=1)
    #last_login represents the date-time when the user last logged into the system.
    last_login = fields.Datetime('Latest Connection', readonly=1,
                                 related='partner_id.user_id.login_date')
    #faculty_subject_ids is a many-to-many field which associates an employee with one or more academic subjects so that the employee can teach those subjects. op.subject represents an academic subject in this case.
    faculty_subject_ids = fields.Many2many('op.subject', string='Subject(s)',
                                           tracking=True)
    #emp_id is a field of type Many2one used to create a relation between the current model record and an instance of the hr.employee model defined in the Odoo system. It allows the op.department records to be linked with hr.employee records.
    #main_department_id is another field of type Many2one which creates a relationship between the current model and the op.department model. It is used to store the main department to which an employee belongs to. The default value for this field is set to the id of the department to which the user belongs to.
    emp_id = fields.Many2one('hr.employee', 'HR Employee')
    main_department_id = fields.Many2one(
        'op.department', 'Main Department',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)
    #allowed_department_ids is a field of type Many2many which corresponds to one or multiple records of the model op.department. This field allows selecting one or more departments that the current user is allowed to access.
    #active is a field of type Boolean used to activate or deactivate a record. It defines whether the record is visible in views or not. If the value of this field is True, the record is active otherwise not visible.
    allowed_department_ids = fields.Many2many(
        'op.department', string='Allowed Department',
        default=lambda self:
        self.env.user.department_ids and self.env.user.department_ids.ids or False)
    active = fields.Boolean(default=True)
    #This is an @api.constrains decorator that is used in the Odoo model to define a constraint on the birth_date field. This constraint checks if the birth date is greater than the current date. If it is met, an exception with a custom message is created using the ValidationError class.
    #In short, this function is used to prevent someone from entering an incorrect or future birth date in the form.
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))
    #This is an @api.constrains() constraint decorator in Odoo that is used to define a constraint on the fields in the model. Here, the field in this model is year_service. This function is called every time something is inserted or modified in the year_service field.
    #The _check_birthdate function validates if the service year is less than or equal to the current date. If it is greater than the current date, it throws a ValidationError Validation exception. The exception will display the error message to inform the user about the restriction that has occurred.
    @api.constrains('year_service')
    def _check_birthdate(self):
        for record in self:
            if record.year_service > fields.Integer():
                raise ValidationError(_(
                    "Year Service can't be greater than current date!"))
    #This is an API decorator that acts as a constraint (_check_birthdate) for a particular field (entry_date). The _check_birthdate function uses the current date to validate the entry_date field. Then, if entry_date is greater than the current date, a validation exception will be generated with a message indicating that you cannot enter a future birth date.
    @api.constrains('entry_date')
    def _check_birthdate(self):
        for record in self:
            if record.entry_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))
    #This API is an onchange method that sets the name of a record based on its first name, middle name, last name, and second last name fields. It concatenates the strings in various ways depending on which fields are filled out. If only first and last names are provided, it sets the name to "first_name last_name". If middle name is additionally provided, the name will be set to "first_name middle_name last_name", and if both middle and second last names are provided, the name will be set to "first_name middle_name last_name second_last_name". It triggers whenever any of these four fields are modified.
    @api.onchange('first_name', 'middle_name', 'last_name', 'second_last_name')
    def _onchange_name(self):
        self.name = f'{self.first_name} {self.last_name}'
        if self.middle_name and not self.second_last_name:
            self.name = f'{self.first_name} {self.middle_name} {self.last_name}'
        elif self.second_last_name and not self.middle_name:
            self.name = f'{self.first_name} {self.last_name} {self.second_last_name}'
        elif self.second_last_name and self.middle_name:
            self.name = f'{self.first_name} {self.middle_name} {self.last_name} {self.second_last_name}'
    #This is a Python code that uses the Odoo framework's API to implement a trigger function that will be executed whenever the 'state_id' field of an object/record is modified. The primary functionality of this function ('clear_state') is to clear the values of two other fields named 'municipality_id' and 'parish_id'. Since any change in the state would naturally make the municipality and parish fields irrelevant, the 'clear_state' function ensures that these fields are reset to their original 'False' state. This helps to maintain data consistency and integrity by preventing any invalid or inconsistent logic/data related to the municipality and the parish from being saved when they are not applicable in a new state.
    @api.onchange('state_id')
    def clear_state(self):
        """Clear fields of municipality and parish when changing the state"""
        for rec in self:
            rec.municipality_id = False
            rec.parish_id = False
    #This is a decoration of the onchange() method in Odoo that is used to clear the parish field when the municipality field changes. That is, when there is a change in the municipality field this method will fire and set the value of the parish field to False.
    #The clear_municipality() method operates on records, as it makes use of the rec variable that stores the current record. This method can be used in any model in Odoo that has municipality and parish fields to clear the parish values after changing the municipality.
    @api.onchange('municipality_id')
    def clear_municipality(self):
        """Clear fields of parish when changing the municipality"""
        for rec in self:
            rec.parish_id = False
    #The create_employee API creates records from the hr.employee data model based on the values given in the current model.
    #First, it iterates through each record present in the active object (self). Then, a dictionary of values is created from the corresponding fields. Point syntax is used to obtain the values related to other models to which the fields are linked.
    #After creating the employee record using the call to create in the hr.employee object, the ID of the newly created employee is written to the emp_id field in the current record.
    #Finally, the partner_share and employee fields are also updated in the current record of the res.partner object.
    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'shift': record.shift,
                'dedication': record.dedication,
                'ladder': record.rank,
                'status_active': record.status_active,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})
    #This API is a method defined in an Odoo model and it is decorated with "@api.model". This method returns a list of dictionaries representing import templates for faculties.
    #The return value of this method is a list that contains one dictionary. The dictionary has two keys: "label" and "template". The value for the "label" key is a string that describes the import template. The value for the "template" key is a URL to a Microsoft Excel file that contains the import template data.
    #The purpose of this API is to provide an easy way to download import templates for faculties using a web interface.
    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Faculties'),
            'template': '/openeducat_core/static/xls/op_faculty.xls'
        }]
    #This API is a function that is executed when the value of the "entry_date" field changes. The function uses the Python library "relativedelta" to calculates This difference in years is then mapped to the corresponding "number_year_service" field in the record.
    #If the entry date is not defined, a value of zero is assigned to the "number_year_service" field.
    @api.depends('entry_date') #
    def _compute_number_year_service(self):
        today = fields.Date.today()
        for record in self:
            number_year_service = relativedelta(today, record.entry_date).years if record.entry_date else 0
            record.number_year_service = number_year_service 