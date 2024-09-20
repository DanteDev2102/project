from odoo import http, _
from odoo.http import request, content_disposition

from datetime import datetime
from io import BytesIO

import logging
import base64


from .basic_controller import BasicControllerXlsxReport

_logger = logging.getLogger(__name__)


class MyController(http.Controller):
    @http.route("/my_module/send_data", type="json", auth="user", csrf=False)
    def send_data(self, **kw):
        # Procesar los datos recibidos
        session_id = kw.get("session_id")
        # ... otros datos ...

        # Obtener el registro de la sesión
        session = request.env["op.session"].browse(int(session_id))

        # Imprimir los datos por consola

        _logger.warning("AAAAAAAAAAAAAAAAAAAAAHHHHHH")
        _logger.warning(session.name)  # Ajusta según los campos de tu modelo

        return {"result": "OK"}
