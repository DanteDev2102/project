from odoo import models, fields, _
from odoo import http
from odoo.http import requests
from odoo.exceptions import UserError, ValidationError


class SessionWizard(models.TransientModel):
    _name = "op.session.wizard"
    _description = "wizard to create xlsx report"

    session_id = fields.Many2one(
        "op.session",
        required=True,
        default=lambda self: self.env.context.get("active_id"),
    )

    def send_data(self):
        data = {
            "session_id": self.session_id.id,
            # Otros datos aquí
        }
        url = "/send_data"
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Levanta una excepción si la solicitud falla
        except requests.exceptions.RequestException as e:
            # Maneja los errores
            raise UserError(_("Error sending data: %s") % e)
        return {"type": "ir.actions.act_window_close"}
