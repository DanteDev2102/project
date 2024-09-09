from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    municipality_id = fields.Many2one("res.country.state.municipality", "Municipality")
    parish_id = fields.Many2one("res.country.state.municipality.parish", "Parish")

    @api.model
    def _address_fields(self):
        address_fields = set(super()._address_fields())
        address_fields.add("municipality_id")
        address_fields.add("parish_id")
        return list(address_fields)

    @api.onchange("state_id")
    def clear_state(self):
        """Clear fields of municipality and parish when changing the state"""
        for rec in self:
            rec.municipality_id = False
            rec.parish_id = False

    @api.onchange("municipality_id")
    def clear_municipality(self):
        """Clear fields of parish when changing the municipality"""
        for rec in self:
            rec.parish_id = False
