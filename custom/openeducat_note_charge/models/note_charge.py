from odoo import api, fields, models


class NoteCharge(models.Model):
    _name = "note.charge"
    # _rec_name = ""
    # _order = ""
    _description = """Carga de Notas"""

    faculty_id = fields.Many2one("op.faculty", "Profesor", required=True)
    student_id = fields.Many2one("op.student", "Estudiante", required=True)
    course_id = fields.Many2one("op.course", "PNF", required=True)
    subject_id = fields.Many2one("op.subject", "UC", required=True)
    note = fields.Float("Nota final", compute="_compute_note", store=True)
    line_ids = fields.One2many("note.charge.line", "charge_id", "Notas")
    vat_student = fields.Char("Cédula estudiante", related="student_id.id_number", store=True)
    vat_faculty = fields.Char("Cedula docente", related="faculty_id.id_number", store=True)
    code = fields.Char("Codigo relacional")
    company_id = fields.Many2one("res.company", "Núcleo", default=lambda self: self.env.user.company_id)
    turn = fields.Selection([
        ("morning", "Matutino"),
        ("afternoon", "Vespertino"),
        ("night", "Nocturno"),
    ], "Turno")
    academic_years_id = fields.Many2one('op.academic.year', 'Periodo')
    code_subject = fields.Char("Código UC")
    study_plan = fields.Integer("Año plan de estudios")
    batch_id = fields.Many2one('op.batch', 'Sección')

    @api.depends("line_ids")
    def _compute_note(self):
        for rec in self:
            rec.note = round(sum(rec.line_ids.mapped("note")), 0)

    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.student_id.name} {rec.course_id.name} {rec.subject_id.name} {rec.note}"
            result.append((rec.id, '%s' % (name)))
        return result


class NoteChargeLine(models.Model):
    _name = "note.charge.line"
    # _rec_name = ""
    # _order = ""
    _description = """Líneas de Carga de Notas"""

    sequence = fields.Integer()
    charge_id = fields.Many2one("note.charge", "Carga", required=True, ondelete="cascade")
    name = fields.Char("Evaluación", required=True)
    note = fields.Float("Nota F", compute="_compute_note", store=True)
    note_qty = fields.Float("Nota")
    note_percentage = fields.Float("%")

    @api.depends("note_qty", "note_percentage")
    def _compute_note(self):
        for rec in self:
            rec.note = 0
            if rec.note_qty and rec.note_percentage:
                rec.note = (rec.note_qty * rec.note_percentage) / 100
