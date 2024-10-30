from odoo import http, _
from odoo.http import request, content_disposition
from datetime import datetime
from io import BytesIO
import xlsxwriter
import logging
import base64

from .basic_controller import BasicControllerXlsxReport

_logger = logging.getLogger(__name__)


class MyController(BasicControllerXlsxReport):

    @http.route(
        ["/session/xls_report"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def send_data(self, **kw):
        # obtenemos el id de la session y hacemos unabusqueda de ella
        session_id = kw["id"]
        session = request.env["op.session"].sudo()
        data = session.search_read([("id", "=", session_id)])[0][
            "student_inscription_ids"
        ]
        # retornamos el archivo excel
        return request.make_response(
            self.get_report(kw, request, data),
            headers=[
                (
                    "Content-Type",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
                (
                    "Content-Disposition",
                    content_disposition(_("session_report.xlsx")),
                ),
            ],
        )

    # Aqui preparamos los datos de la cabecera
    def _prepare_header_report(self, wb, ws, kw, req):
        header_format = wb.add_format(
            {"bold": True, "align": "center", "bg_color": "#ffffff"}
        )
        image_data = BytesIO(base64.b64decode(req.env.company.logo))
        ws.merge_range("B2:E2", req.env.company.name, header_format)
        ws.insert_image(
            "F2",
            "image.png",
            {
                "image_data": image_data,
                "x_scale": 0.2,
                "y_scale": 0.2,
            },
        )
        result = (
            request.env["op.session"].sudo().search_read([("id", "=", kw["id"])])[0]
        )
        # cargamos la informacion por el registro a imprimir
        ws.write(5, 2, _("Faculty:"))
        ws.write(5, 3, _(result["faculty_id"][1]))
        ws.write(6, 2, _("Course"))
        ws.write(6, 3, _(result["course_id"][1]))
        ws.write(7, 2, _("Subject"))
        ws.write(7, 3, _(result["subject_id"][1]))
        ws.write(8, 2, _("Start Time"))
        ws.write(8, 3, _(result["start_hour"]))
        ws.write(9, 2, _("Day"))
        ws.write(9, 3, _(result["type"]))
        ws.write(10, 2, _("Grade weightage"))
        ws.write(10, 3, _(result["subject_credits"]))

        ws.write(5, 6, _("Timing"))
        ws.write(5, 7, _(result["timing_id"][1]))
        ws.write(6, 6, _("Batch"))
        ws.write(6, 7, _(result["batch_id"][1]))
        ws.write(7, 6, _("Classroom"))
        ws.write(7, 7, _(result["classroom_id"][1]))
        ws.write(8, 6, _("End Time"))
        ws.write(8, 7, _(result["end_hour"]))
        ws.write(9, 6, _("Headquarters"))
        ws.write(9, 7, _(result["headquarters"]))
        ws.write(10, 6, _("Students:"))
        ws.write(10, 7, _(result["n_student"]))

    # definimos la cabecera de nuestra "tabla" para mostrar los estudiantes
    def _prepare_table_headers(self, type, wb):

        table_header_format = wb.add_format({"bold": True})

        return [
            {
                "header": _("C.I."),
                "header_format": table_header_format,
            },
            {
                "header": _("Student Name"),
                "header_format": table_header_format,
            },
        ]

    # Pasamos los datos a la tabla
    def _prepare_data_table(self, data, kw):
        result = (
            request.env["op.session"].sudo().search_read([("id", "=", kw["id"])])[0]
        )
        students_ids = result["student_inscription_ids"]
        students_data = []
        for student_id in students_ids:
            student = (
                request.env["op.inscription"]
                .sudo()
                .search_read([("id", "=", student_id)])
            )
            # "display_name", "student_id_number"
            students_data.append(
                {
                    "name": student[0]["display_name"],
                    "student_id": student[0]["student_id_number"],
                }
            )

        return [
            [
                student["student_id"],
                student["name"],
            ]
            for student in students_data
        ]
