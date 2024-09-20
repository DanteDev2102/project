from odoo import http, _
from odoo.http import request, content_disposition

from datetime import datetime
from io import BytesIO

import logging
import base64


from .basic_controller import BasicControllerXlsxReport

logger = logging.getLogger(__name__)


class SaleStatisticsReport(BasicControllerXlsxReport):
    @http.route(["/xlsx/sale/statistics"], auth="user", csrf=False, type="http")
    def generate_sale_statistics_report(self, **kw):
        return request.make_response(
            self.get_report(
                kw,
                request,
                getattr(self, f"prepare_data{kw.get('type')}")(
                    request,
                    bool(int(kw.get("can_select_all"))),
                    kw.get("ids"),
                    kw.get("date_from"),
                    kw.get("date_end"),
                ),
            ),
            headers=[
                (
                    "Content-Type",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
                (
                    "Content-Disposition",
                    content_disposition(_("sale_statistics.xlsx")),
                ),
            ],
        )

    def get_category_name(self, category):
        if not category.parent_id:
            return category.name

        return f"{category.name}-{self.get_category_name(category=category.parent_id)}"

    def _prepare_data_table(self, data, kw):
        days = self._count_days_in_period(
            date_from=kw.get("date_from"), date_end=kw.get("date_end")
        )

        return [
            [
                record["name"],
                record["description"],
                record["qty_on_hand"],
                record["count_sales"],
                record["qty_sale"],
                round(record["qty_sale"] / days, 2),
            ]
            for record in data
        ]

    def _basic_domain(self, date_from, date_end):
        return [
            ("order_id.date_order", ">=", date_from),
            ("order_id.date_order", "<=", date_end),
            ("order_id.state", "in", ["sent", "sale"]),
            ("invoice_status", "=", "invoiced"),
            ("product_id", "!=", False),
        ]

    def _count_days_in_period(self, date_from, date_end):
        return (
            datetime.strptime(date_end, "%Y-%m-%d")
            - datetime.strptime(date_from, "%Y-%m-%d")
        ).days

    def _prepare_data_category(self, request, can_select_all, ids, date_from, date_end):
        domain = [
            *self._basic_domain(date_from, date_end),
            ("product_id.categ_id", "!=", False),
        ]

        if not can_select_all and len(ids) > 0:
            domain.append(
                (
                    "product_id.categ_id",
                    "in",
                    [int(id) for id in ids.split(",")],
                )
            )

        lines = request.env["sale.order.line"].sudo().search(domain)
        group_by_category_data = dict()

        for line in lines:
            category = line.product_id.categ_id

            category_name = "/".join(
                self.get_category_name(category=category).split("-")[::-1]
            )

            group = group_by_category_data.get(category_name)

            if not group:
                group_by_category_data.update(
                    {
                        category_name: {
                            "sales": [line.order_id.id],
                            "description": category.name,
                            "qty_sale": line.qty_invoiced,
                            "count_sales": 1,
                            "name": category_name,
                        }
                    }
                )

                continue

            if line.order_id.id not in group.get("sales"):
                group["sales"].append(line.order_id.id)
                group["count_sales"] += 1

            group["qty_sale"] += line.qty_invoiced

        return [
            {
                **data,
                "qty_on_hand": sum(
                    [
                        product.qty_available
                        for product in request.env["product.product"].search(
                            [("categ_id.name", "=", data["description"])]
                        )
                    ]
                ),
            }
            for data in group_by_category_data.values()
        ]

    def _prepare_data_product(self, request, can_select_all, ids, date_from, date_end):
        domain = self._basic_domain(date_from, date_end)

        if not can_select_all and len(ids) > 0:
            domain.append(
                (
                    "product_id",
                    "in",
                    [int(id) for id in ids.split(",")],
                )
            )

        lines = request.env["sale.order.line"].sudo().search(domain)
        group_by_product_data = dict()

        for line in lines:
            product = line.product_id
            product_id = str(product.id)
            group = group_by_product_data.get(product_id)

            if not group:
                group_by_product_data.update(
                    {
                        product_id: {
                            "qty_on_hand": product.qty_available,
                            "name": product.name,
                            "description": product.name,
                            "qty_sale": line.qty_invoiced,
                            "count_sales": 1,
                            "sales": [line.order_id.id],
                        }
                    }
                )

                continue

            if line.order_id.id not in group.get("sales"):
                group["sales"].append(line.order_id.id)
                group["count_sales"] += 1

            group["qty_sale"] += line.qty_invoiced

        return [value for value in group_by_product_data.values()]

    def _prepare_table_headers(self, type, wb):
        name_header = _("Category") if type == "category" else _("Product")

        table_header_format = wb.add_format({"bold": True})

        return [
            {
                "header": name_header,
                "header_format": table_header_format,
            },
            {
                "header": _("Description"),
                "header_format": table_header_format,
            },
            {
                "header": _("Qty On Hand"),
                "header_format": table_header_format,
            },
            {
                "header": _("Sales"),
                "header_format": table_header_format,
            },
            {
                "header": _("Qty Sale"),
                "header_format": table_header_format,
            },
            {
                "header": _("Prom Sales"),
                "header_format": table_header_format,
            },
        ]

    def _prepare_header_report(self, wb, ws, kw, req):
        header_format = wb.add_format(
            {"bold": True, "align": "center", "bg_color": "#ffffff"}
        )

        filter = _("Category") if kw.get("type") == "category" else _("Product")

        image_data = BytesIO(base64.b64decode(req.env.company.logo))

        ws.merge_range("B2:E2", req.env.company.name, header_format)

        ws.merge_range(
            "B3:E3",
            f"{self._format_date_str(kw.get('date_from'))} - {self._format_date_str(kw.get('date_end'))}",
            header_format,
        )

        ws.merge_range("B4:E4", _("Filter by: %s") % filter, header_format)

        ws.insert_image(
            "F2",
            "image.png",
            {
                "image_data": image_data,
                "x_scale": 0.2,
                "y_scale": 0.2,
            },
        )
