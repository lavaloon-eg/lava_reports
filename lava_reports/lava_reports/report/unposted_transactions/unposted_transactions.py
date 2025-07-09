# Copyright (c) 2025, lavaloon and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType, Order
from frappe.query_builder.custom import ConstantColumn
from collections import defaultdict

DOC_TYPES = [
    "Quotation",
    "Sales Order",
    "Delivery Note",
    "Sales Invoice",
    "Purchase Order",
    "Purchase Receipt",
    "Purchase Invoice",
    "Payment Entry"
]

def execute(filters=None):
    columns, data, message, chart, report_summary = None, None, None, None, None

    columns = get_columns()
    data = get_data(filters)
    summary = get_summary(data)

    message = _(
        "This report shows all draft transactions across Sales, Purchase, and Payment cycles to help monitor pending business activities."
    )
    return columns, data, message, chart, summary


def get_data(filters=None):
    filters = filters or {}

    doc_types = DOC_TYPES

    if filters.get("doctype"):
        doc_types = [filters.get("doctype")]

    union_query = None

    for dt in doc_types:
        table = DocType(dt)
        user_table = DocType('User')

        query = (
            frappe.qb
            .from_(table)
            .select(
                table.name.as_("id"),
                ConstantColumn(dt).as_("type"),
                table.owner.as_("created_by"),
                user_table.full_name.as_("full_name"),
                table.creation.as_("creation_date"),
                table.modified.as_('modified'),
                table.company.as_("company")
            )
            .inner_join(user_table)
            .on(table.owner == user_table.name)
            .where(table.docstatus == 0)
        )

        if filters.get("company"):
            query = query.where(table.company == filters.get("company"))

        if union_query is None:
            union_query = query
        else:
            union_query += query

    union_query = union_query.orderby('modified', order=Order.asc)

    return union_query.run(as_dict=True) if union_query else []

def get_columns():
    return [
        {
            "label": _("Transaction ID"),
            "fieldname": "id",
            "fieldtype": "Link",
            "options": "DocType",
            "width": 250
        },
        {
            "label": _("Transaction Type"),
            "fieldname": "type",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Created By"),
            "fieldname": "full_name",
            "fieldtype": "Link",
            "options": "User",
            "width": 200
        },
        {
            "label": _("Creation Date"),
            "fieldname": "creation_date",
            "fieldtype": "Datetime",
            "width": 200
        },
        {
            "label": _("Company"),
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 200
        },
    ]

def get_summary(data):
    summary = defaultdict(int)

    for row in data:
        summary[row.get("type")] += 1

    summary_rows = []

    for transaction_type in DOC_TYPES:
        summary_rows.append({
            "label": _("Total {0}").format(transaction_type),
            "value": summary[transaction_type],
        })

    return summary_rows
