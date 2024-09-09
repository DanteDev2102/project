from odoo import fields, models, _


class PartnerDiverseGender(models.Model):
    _name = 'partner.diverse.gender'
    _description = 'Diverse Gender'

    name = fields.Char('Diverse gender', translate=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', _('Gender must be unique.')),
    ]
