from odoo import http
from datetime import datetime
from io import BytesIO
import xlsxwriter
import logging

_logger = logging.getLogger(__name__)


class BasicControllerXlsxReport(http.Controller):
    def _prepare_data_table(self, data, kw):
        pass

    def _prepare_header_report(self, wb, ws, kw, req):
        pass

    def _prepare_table_headers(self, type, wb):
        pass

    def _prepare_table(self, ws, data, kw, wb):
        ws.add_table(
            f"B16:C{len(data) + 16}",
            {
                "columns": self._prepare_table_headers(kw.get("type"), wb=wb),
                "data": self._prepare_data_table(data=data, kw=kw),
            },
        )

    def _prepare_footer_report(self, req, kw, wb, ws):
        pass

    def get_report(self, kw, request, data):
        report = BytesIO()
        workbook = xlsxwriter.Workbook(report, {"in_memory": True})
        worksheet = workbook.add_worksheet()

        self._prepare_header_report(wb=workbook, ws=worksheet, kw=kw, req=request)
        self._prepare_table(ws=worksheet, data=data, kw=kw, wb=workbook)
        self._prepare_footer_report(wb=workbook, ws=worksheet, kw=kw, req=request)

        # worksheet.autofit()
        workbook.close()

        return report.getvalue()
