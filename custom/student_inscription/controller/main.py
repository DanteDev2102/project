import logging

from odoo import http, fields
from odoo.http import request
from datetime import datetime

_logger = logging.getLogger(__name__)
# comentar


class StudentRequest(http.Controller):
    @http.route(["/student-inscription"], type="http", auth="user", website=True)
    def student_enroll(self):
        user = request.env.user.id
        # headquarters, eliminarlo y que se muestre cualquiera
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
                    "traject",
                ],
            )
        )
        pnf = student[0]["pnf"]
        traject = student[0]["traject"]
        course = (
            request.env["op.course"]
            .sudo()
            .search_read([("code", "=", pnf)], ["subject_ids", "name", "id"])
        )
        student_uc = []
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

        sessions = (
            request.env["op.session"]
            .sudo()
            .search_read(
                [
                    ("course_id", "=", course[0]["id"]),
                    ("subject_traject", "=", traject),
                    ("n_student", "<", 30),
                ],
                [],
            )
        )
        session_per_term = []
        for session in sessions:
            if select_term["name"] == "Semester 1":
                if session["subject_semester"] == "one":
                    session_per_term.append(session)
            else:
                if (
                    session["subject_semester"] == "one"
                    and session["subject_duration_semester"] == "two"
                ):
                    session_per_term.append(session)
                if session["subject_semester"] == "two":
                    session_per_term.append(session)

        search_inscription = (
            request.env["op.inscription"]
            .sudo()
            .search_read(
                [
                    ("student_id", "=", student[0]["id"]),
                    ("academic_year_id", "=", academic_year[0]["id"]),
                    ("academic_term_id", "=", select_term["id"]),
                ],
                [],
            )
        )
        if search_inscription == []:
            session_group = []
            for uc in student_uc:
                name = uc["name"]
                academic_uc = int()
                uc_session = []
                for session in session_per_term:
                    if session["subject_id"][1] == uc["name"]:
                        uc_session.append(session)
                        academic_uc = session["subject_credits"]
                if uc_session != []:
                    session_group.append(
                        {
                            "name": name,
                            "values": uc_session,
                            "uc": academic_uc,
                        }
                    )

            return request.render(
                "student_inscription.student_inscription_form",
                {
                    "student": student[0],
                    "academic_year": academic_year[0],
                    "academic_term": select_term,
                    "sessions": session_group,
                },
            )
        else:
            return request.render(
                "student_inscription.student_inscription_already_registered"
            )

    @http.route(
        ["/student-register"],
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
        csrf=False,
    )
    def servuce_post(self, **kw):

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
                    "traject",
                ],
            )
        )
        academic_year = (
            request.env["op.academic.year"]
            .sudo()
            .search_read(
                [],
                [
                    "id",
                ],
                limit=1,
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

        # se comienza el proceso de registro
        values = [kw[f"id-{i+1}"] for i in range(0, int(kw["len"]))]

        # creamos la inscripcion del studiante
        create_enroll = (
            request.env["op.inscription"]
            .sudo()
            .create(
                {
                    "student_id": student[0]["id"],
                    "academic_year_id": academic_year[0]["id"],
                    "academic_term_id": select_term["id"],
                }
            )
        )
        # buscamos la innscipcion creada y le asignamos las materias del estudiante ya que la asignacion del
        # campo m2m no se puede hacer en el create
        inscription = request.env["op.inscription"].sudo()
        inscription.browse(create_enroll["id"])["session_ids"] = [
            (4, value, 0) for value in values
        ]

        return request.render("student_inscription.student_inscription_completed")
