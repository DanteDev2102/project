from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class SessionWizard(models.TransientModel):
    _name = "op.session.wizard"
    _description = "wizard to create xlsx report"

    session_id = fields.Many2one(
        "op.session",
        required=True,
        default=lambda self: self.env.context.get("active_id"),
    )

    @api.depends("session_id")
    def print_session_report(self):
        return {
            "type": "ir.actions.act_url",
            "target": "new",
            "url": "/session/xls_report?id=%s" % self.session_id["id"],
        }
