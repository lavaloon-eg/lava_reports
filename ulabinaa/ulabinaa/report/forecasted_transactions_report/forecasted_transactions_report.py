# Copyright (c) 2024, lavaloon and contributors
# For license information, please see license.txt

import frappe
from erpnext.controllers.stock_controller import get_accounting_ledger_preview


def execute(filters=None):
    columns, data = [], []
    columns = create_columns()
    sql = f"""
            select je.posting_date,
                jea.account,
                jea.debit,
                jea.credit,
                je.voucher_type,
                jea.party_type,
                jea.party,
                jea.project,
                jea.cost_center,
                je.name as voucher_id,
                je.remark
                from `tabJournal Entry` as je
                join `tabJournal Entry Account` as jea
                    on je.name = jea.parent
                WHERE je.`posting_date` BETWEEN %(filter_from_date)s and %(filter_to_date)s
                AND je.company=%(filter_company)s
                ORDER BY je.posting_date
        """
    show_accounting_ledger_preview_bulk(filters=filters)
    data = frappe.db.sql(sql, values={
        "filter_company": filters['filter_company'],
        "filter_from_date": filters['filter_from_date'],
        "filter_to_date": filters['filter_to_date'],
    }, as_dict=1)
    frappe.db.rollback()
    return columns, data


def show_accounting_ledger_preview_bulk(filters):
    filters['include_dimensions'] = 1
    filters['company'] = filters['filter_company']
    doctypes = ["Purchase Invoice", "Payment Entry"]
    gl_columns, gl_data = [], []
    for doctype in doctypes:
        docs_filters = {
            'company': filters['filter_company'],
            'posting_date': ['between', filters['filter_from_date'],
                             filters['filter_to_date']]
        }
        if filters['filter_include_submitted'] == 0:
            docs_filters['docstatus'] = 0
        else:
            docs_filters['docstatus'] = ["<", 2]

        docs = frappe.db.get_list(doctype,
                                  filters=docs_filters,
                                  order_by='posting_date')
        for doc in docs:
            result = show_accounting_ledger_preview_per_transaction(filters=filters,
                                                                    doctype=doctype,
                                                                    docname=doc.name)
            if not gl_columns:
                gl_columns = result.gl_columns
            gl_data.append(result.gl_data)

    return {"gl_columns": gl_columns, "gl_data": gl_data}


def show_accounting_ledger_preview_per_transaction(filters, doctype, docname):
    doc = frappe.get_doc(doctype, docname)
    doc.run_method("before_gl_preview")
    gl_columns, gl_data = get_accounting_ledger_preview(doc, filters)
    return {"gl_columns": gl_columns, "gl_data": gl_data}


def create_columns():
    return [

        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": "Posting Date",
            "width": 100
        },
        {
            "fieldname": "account",
            "fieldtype": "Data",
            "label": "Account Name",
            "width": 100
        },
        {
            "fieldname": "debit",
            "fieldtype": "Float",
            "label": "Debit",
            "width": 100
        },
        {
            "fieldname": "credit",
            "fieldtype": "Float",
            "label": "Credit",
            "width": 100
        },
        {
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "label": "Voucher Type",
            "width": 100
        },
        {
            "fieldname": "party_type",
            "fieldtype": "Data",
            "label": "Party Type",
            "width": 100
        },
        {
            "fieldname": "party",
            "fieldtype": "Data",
            "label": "Party",
            "width": 100
        },
        {
            "fieldname": "cost_center",
            "fieldtype": "Link",
            "label": "Cost Center",
            "options": "Cost Center",
            "width": 100
        },
        {
            "fieldname": "project",
            "fieldtype": "Link",
            "label": "Project",
            "options": "Project",
            "width": 100
        },
        {
            "fieldname": "voucher_id",
            "fieldtype": "Data",
            "label": "Voucher ID",
            "width": 100
        },
        {
            "fieldname": "remark",
            "fieldtype": "Data",
            "label": "Remarks",
            "width": 100
        }
    ]
