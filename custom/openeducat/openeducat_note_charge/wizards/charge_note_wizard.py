import binascii
import tempfile
import xlrd

from odoo import fields, models, _
from odoo.exceptions import UserError


class WizardChargeNoteImport(models.Model):
    _name = "wizard.charge.note.import"
    _description = "Asistente para importacion de notas"

    file = fields.Binary(required=True)
    company_id = fields.Many2one("res.company", "Núcleo", default=lambda self: self.env.user.company_id)
    faculty_id = fields.Many2one("op.faculty", "Profesor", required=True)
    course_id = fields.Many2one("op.course", "PNF", required=True)
    subject_id = fields.Many2one("op.subject", "UC", required=True)
    turn = fields.Selection([
        ("morning", "Matutino"),
        ("afternoon", "Vespertino"),
        ("night", "Nocturno"),
    ], "Turno", required=True)
    academic_years_id = fields.Many2one('op.academic.year', 'Periodo', required=True)

    def import_charge_note_data(self):
        try:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file))
            fp.seek(0)
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            row_count = sheet.nrows
            # col_count = sheet.ncols
            note_id = self.env["note.charge"]
            percentage_1 = sheet.cell(0, 16).value
            percentage_2 = sheet.cell(0, 18).value
            percentage_3 = sheet.cell(0, 20).value
            percentage_4 = sheet.cell(0, 22).value
            percentage_5 = sheet.cell(0, 24).value
            percentage_6 = sheet.cell(0, 26).value
            percentage_7 = sheet.cell(0, 28).value
            percentage_8 = sheet.cell(0, 30).value
            percentage_9 = sheet.cell(0, 32).value
            percentage_10 = sheet.cell(0, 34).value

            for cur_row in range(1, row_count):
                id_number = sheet.cell(cur_row, 1).value
                last_name = sheet.cell(cur_row, 2).value
                name = sheet.cell(cur_row, 3).value
                code = sheet.cell(cur_row, 4).value
                subject_code = sheet.cell(cur_row, 8).value
                id_number_faculty = sheet.cell(cur_row, 11).value
                batch_name = sheet.cell(cur_row, 10).value
                study_plan = sheet.cell(cur_row, 13).value

                # Notas
                note_1 = sheet.cell(cur_row, 15).value
                note_2 = sheet.cell(cur_row, 17).value
                note_3 = sheet.cell(cur_row, 19).value
                note_4 = sheet.cell(cur_row, 21).value
                note_5 = sheet.cell(cur_row, 23).value
                note_6 = sheet.cell(cur_row, 25).value
                note_7 = sheet.cell(cur_row, 27).value
                note_8 = sheet.cell(cur_row, 29).value
                note_9 = sheet.cell(cur_row, 31).value
                note_10 = sheet.cell(cur_row, 33).value

                id_number = str(id_number).replace(".0", "")
                student_id = self.env["op.student"].search([
                    ("id_number", "=", id_number)
                ], limit=1)
                if not student_id:
                    raise UserError(_(f"El estudiante con cédula {id_number} no existe."))

                batch_name = str(batch_name).replace(".0", "")
                batch_id = self.env["op.batch"].search([
                    ("name", "=", batch_name)
                ], limit=1)
                if not batch_id:
                    raise UserError(_(f"La sección {batch_name} no existe."))

                line_ids = []

                if note_1:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 1",
                        "note_qty": note_1,
                        "note_percentage": percentage_1 * 100,
                    }))
                if note_2:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 2",
                        "note_qty": note_2,
                        "note_percentage": percentage_2 * 100,
                    }))
                if note_3:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 3",
                        "note_qty": note_3,
                        "note_percentage": percentage_3 * 100,
                    }))
                if note_4:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 4",
                        "note_qty": note_4,
                        "note_percentage": percentage_4 * 100,
                    }))
                if note_5:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 5",
                        "note_qty": note_5,
                        "note_percentage": percentage_5 * 100,
                    }))
                if note_6:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 6",
                        "note_qty": note_6,
                        "note_percentage": percentage_6 * 100,
                    }))
                if note_7:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 7",
                        "note_qty": note_7,
                        "note_percentage": percentage_7 * 100,
                    }))
                if note_8:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 8",
                        "note_qty": note_8,
                        "note_percentage": percentage_8 * 100,
                    }))
                if note_9:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 9",
                        "note_qty": note_9,
                        "note_percentage": percentage_9 * 100,
                    }))
                if note_10:
                    line_ids.append((0, 0, {
                        "name": "Evaluación 10",
                        "note_qty": note_10,
                        "note_percentage": percentage_10 * 100,
                    }))

                note_id.create({
                    "faculty_id": self.faculty_id.id,
                    "student_id": student_id.id,
                    "course_id": self.course_id.id,
                    "subject_id": self.subject_id.id,
                    "code": code,
                    "company_id": self.company_id.id,
                    "turn": self.turn,
                    "academic_years_id": self.academic_years_id.id,
                    "code_subject": subject_code,
                    "study_plan": study_plan,
                    "batch_id": batch_id.id,
                    "line_ids": line_ids,
                })
        except Exception as e:
            raise UserError(_(f"Error de archivo:\n{e}"))
