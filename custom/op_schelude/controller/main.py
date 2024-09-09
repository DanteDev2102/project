import logging

from odoo import http, fields
from odoo.http import request
from datetime import datetime

_logger = logging.getLogger(__name__)


class ServiceRequest(http.Controller):

    @http.route(
        ["/student-inscription"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def service_request(self):
        user = request.env.user.id
        student = (
            request.env["op.student"]
            .sudo()
            .search_read(
                [("user_id", "=", user)],
                [
                    "id",
                    "name",
                    "turn",
                    "pnf",
                    "course_detail_ids",
                    "headquarters",
                ],
            )
        )
        academic_year = (
            request.env["op.academic.year"]
            .sudo()
            .search_read(
                [], ["id", "name", "term_structure", "academic_term_ids"], limit=1
            )
        )
        terms = (
            request.env["op.academic.term"]
            .sudo()
            .search_read(
                [
                    ("academic_year_id", "=", academic_year[0]["id"]),
                ],
                [],
            )
        )
        current_term = fields.Date.context_today(request)
        select_term = {}
        for term in terms:
            if (
                current_term == fields.Date.context_today(request)
            ) and current_term < term["term_start_date"]:
                select_term = term

        headquarters = student[0]["headquarters"].lower()
        pnf = student[0]["pnf"]
        course = (
            request.env["op.course"]
            .sudo()
            .search_read([("code", "=", pnf)], ["subject_ids", "name", "id"])
        )
        _logger.warning(course)
        student_uc = []  # student subject from pnf
        ucs = (
            request.env["op.subject"]
            .sudo()
            .search_read(
                [],
                [],
            )
        )
        for uc in ucs:
            for cs in uc["course_ids"]:
                if cs == course[0]["id"]:
                    student_uc.append(uc)
        pnf = pnf.lower()
        scheludes_uc = []
        for u in student_uc:
            _logger.warning(u)
            scheludes = (
                request.env["op.schelude"]
                .sudo()
                .search_read([("subject_id", "=", u["id"])], [])
            )
            _logger.warning(scheludes)

        return request.render(
            "openeducat_student_inscription.student_inscription_form",
            {
                "student": student,
                "academic_year": academic_year,
                "term": select_term,
                "schelude": scheludes_uc,
            },
        )

    @http.route(
        ["/student-register"],
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
        csrf=False,
    )
    def service_post(self, **kw):
        # {
        #     "course": "Calculo",
        #     "batch_id": "2",
        #     "teacher_id": "6",
        #     "name-1": "Calculo",
        #     "batch-1": "6",
        #     "teacher-1": "2",
        #     "name-2": "Programacion2",
        #     "batch-2": "6",
        #     "teacher-2": "12",
        # }
        # _logger.warning(kw["len"])
        values = [
            {
                "name": kw[f"name-{i+1}"],
                "batch_id": kw[f"batch-{i+1}"],
                "teacher_id": kw[f"teacher-{i+1}"],
            }
            for i in range(0, int(kw["len"]))
        ]
        # [
        #     {"name": "Calculo", "batch_id": "2", "teacher_id": "6"},
        #     {"name": "Programacion2", "batch_id": "12", "teacher_id": "6"},
        #     {"name": "ABP", "batch_id": "7", "teacher_id": "6"},
        # ]
        user = request.env.user.id
        student = (
            request.env["op.student"]
            .sudo()
            .search_read(
                [("user_id", "=", user)],
                [
                    "id",
                    "pnf",
                ],
            )
        )
        # _logger.warning(student)

        academic_year = (
            request.env["op.academic.year"].sudo().search_read([], ["id"], limit=1)
        )
        terms = (
            request.env["op.academic.term"]
            .sudo()
            .search_read(
                [
                    ("academic_year_id", "=", academic_year[0]["id"]),
                ],
                [],
            )
        )
        current_term = fields.Date.context_today(request)
        select_term = {}
        for term in terms:
            # _logger.warning(term)
            if (
                current_term == fields.Date.context_today(request)
            ) and current_term < term["term_start_date"]:
                # _logger.warning(term["term_start_date"])
                select_term = term
        inscription = (
            request.env["sigu.student.inscription"]
            .sudo()
            .create(
                {
                    "student_id": student[0]["id"],
                    "academic_years_id": academic_year[0]["id"],
                    "academic_term_id": select_term["id"],
                }
            )
        )
        pnf = student[0]["pnf"]
        course = (
            request.env["op.course"]
            .sudo()
            .search_read([("code", "=", pnf)], ["subject_ids", "name", "id"])
        )
        # _logger.warning(inscription["id"])
        _logger.warning(values)
        for opsubject in values:
            _logger.warning(opsubject)
            subject = (
                request.env["op.subject"]
                .sudo()
                .search_read(
                    [
                        ("name", "=", opsubject["name"]),
                    ],
                    ["course_ids", "name", "id"],
                )
            )
            _logger.warning(subject)
            student_course = (
                request.env["sigu.student.inscription.line"]
                .sudo()
                .create(
                    {
                        "inscription_id": inscription["id"],
                        "subject_id": subject[0]["id"],
                        "course_id": course[0]["id"],
                        "batch_id": opsubject["batch_id"],
                        "teacher_id": opsubject["teacher_id"],
                    }
                )
            )
