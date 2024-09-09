{
    "name": "Openeducat Student Inscription",
    "version": "1.0",
    "depends": ["base", "openeducat_core", "website", "openeducat_timetable"],
    "author": "Author Name",
    "category": "Category",
    "description": """
    Inscription of student
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/student_inscription_view.xml",
        "views/student_inscription_line_view.xml",
        "views/student_inscription_assets.xml",
        "static/src/xml/menu.xml",
        "static/src/xml/student_inscription_form.xml",
    ],
    "demo": [],
    "qweb": [],
}