{
    "name": "OpenEducat Student Inscription",
    "version": "1.0",
    "depends": [
        "base",
        "openeducat_core",
        "website",
        "openeducat_timetable",
        "openeducat_attendance",
    ],
    "author": "DanteDev",
    "category": "",
    "description": """
    Inscription of student
    """,
    "data": [
        "security/ir.model.access.csv",
        "report/report.xml",
        "report/student_session_template.xml",
        "wizards/session_wizard.xml",
        "views/inscription_view.xml",
        "views/student_inscription_assets.xml",
        "views/session_view.xml",
        "views/student_view.xml",
        "static/src/xml/menu.xml",
        "static/src/xml/student_inscription.xml",
    ],
    "auto_install": False,
    "application": True,
    "qweb": [],
}
