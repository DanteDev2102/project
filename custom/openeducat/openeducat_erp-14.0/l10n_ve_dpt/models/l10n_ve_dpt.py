##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# Generated by the Odoo plugin for Dia !

from odoo import fields, models


class CountryState(models.Model):
    _inherit = 'res.country.state'

    municipality_id = fields.One2many('res.country.state.municipality', 'state_id', 'Municipalities in this state')


class StateMunicipality(models.Model):
    """States Municipalities"""
    _name = 'res.country.state.municipality'
    _description = "State municipalities"

    state_id = fields.Many2one('res.country.state', 'State', required=True, help='Name of the State to which the municipality belongs')
    name = fields.Char('Municipality', required=True, help='Municipality name')
    code = fields.Char('Code', size=3, required=True, help='Municipality code in max. three chars.')
    parish_ids = fields.One2many('res.country.state.municipality.parish', 'municipality_id', 'Parishes in this municipality')


class MunicipalityParish(models.Model):
    """States Parishes"""
    _name = 'res.country.state.municipality.parish'
    _description = "Municipality parishes"

    municipality_id = fields.Many2one('res.country.state.municipality', 'Municipality', help='Name of the Municipality to which the parish belongs')
    name = fields.Char('Parish', required=True, help='Parish name')
    code = fields.Char('Name', size=3, required=True, help='Parish Code in max. three chars.')
