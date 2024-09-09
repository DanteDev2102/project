from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Inscription(models.Model):
    _name = "sigu.inscription"
    # _rec_name = ""
    # _order = ""
    _description = """Inscripción"""

    student_id = fields.Many2one("op.student", "Estudiante", required=True)
    course_id = fields.Many2one("op.course", "PNF", required=True)
    academic_year_id = fields.Many2one("op.academic.year", "Periodo académico", required=True)
    line_ids = fields.One2many("sigu.inscription.line", "inscription_id", "Líneas")

    @api.constrains("line_ids")
    def constrains_line(self):
        for rec in self:
            if rec.line_ids:
                semanal_hour = sum(rec.line_ids.mapped("semanal_hour"))
                if semanal_hour > 30:
                    raise ValidationError(_("No puede inscribir más de 30 horas semanales"))

    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.student_id.name} {rec.course_id.name}"
            result.append((rec.id, '%s' % (name)))
        return result


class InscriptionLine(models.Model):
    _name = "sigu.inscription.line"
    _description = """Líneas de Inscripción"""

    name = fields.Many2one("op.subject", "UC", required=True)
    semanal_hour = fields.Integer('Hora semanales', related="name.semanal_hour", store=True)
    inscription_id = fields.Many2one("sigu.inscription", "Inscripción", ondelete="cascade")
    faculty_id = fields.Many2one("op.faculty", "Profesor", required=False)
    subject_id = fields.Many2one('op.timetable', 'Subject', required=True)