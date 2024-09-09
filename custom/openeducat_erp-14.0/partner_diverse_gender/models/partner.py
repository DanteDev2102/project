from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    diverse_gender_id = fields.Many2one('partner.diverse.gender', 'Diverse gender')
