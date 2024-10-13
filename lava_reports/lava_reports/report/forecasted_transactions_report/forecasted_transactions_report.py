# Copyright (c) 2024, lavaloon and contributors
# For license information, please see license.txt

import frappe
from erpnext.controllers.stock_controller import get_accounting_ledger_preview


def execute(filters=None):
    data = []
    columns = create_columns()
    frappe.db.begin()
    show_accounting_ledger_preview_bulk(filters=filters)

    sql = f"""
            SELECT (CASE WHEN gl.name LIKE %(status_id_key)s THEN 'Submitted'
                        ELSE 'Draft' END) as voucher_status,
                gl.posting_date,
                gl.account,
                gl.debit,
                gl.credit,
                gl.voucher_type,
                gl.party_type,
                gl.party,
                gl.against,
                gl.against_voucher_type,
                gl.against_voucher as against_voucher_id,
                gl.project,
                gl.cost_center,
                gl.voucher_no as voucher_id,
                gl.remarks as remark,
                gl.voucher_subtype
                FROM `tabGL Entry` AS gl
                WHERE gl.company=%(filter_company)s
                """
    if filters['filter_include_submitted'] == 'No':
        sql += F""" AND gl.name NOT LIKE %(status_id_key)s """

    if filters['filter_accounts']:
        sql += f""" AND gl.account IN %(filter_accounts)s
                """

    sql += f""" AND gl.voucher_type IN ("Purchase Invoice", "Payment Entry", "Journal Entry")
                AND gl.posting_date BETWEEN %(filter_from_date)s AND %(filter_to_date)s
                ORDER BY gl.posting_date DESC, gl.creation DESC
            """
    data = frappe.db.sql(sql, values={
        "filter_company": filters['filter_company'],
        "filter_from_date": filters['filter_from_date'],
        "filter_to_date": filters['filter_to_date'],
        "filter_accounts": filters['filter_accounts'],
        "status_id_key": "ACC-%"
    }, as_dict=1)
    frappe.db.rollback()
    return columns, data


def show_accounting_ledger_preview_bulk(filters):
    filters['include_dimensions'] = 1
    filters['company'] = filters['filter_company']
    doctypes = ["Purchase Invoice", "Payment Entry", "Journal Entry"]
    gl_columns, gl_data = [], []
    docs_filters = {
        'company': filters['filter_company'],
        'posting_date': ['between', (filters['filter_from_date'],
                                     filters['filter_to_date'])]
    }

    docs_filters['docstatus'] = ["=", 0]

    for doctype in doctypes:
        docs = frappe.db.get_list(doctype,
                                  filters=docs_filters,
                                  order_by='posting_date')
        for doc in docs:
            result = show_accounting_ledger_preview_per_transaction(filters=filters,
                                                                    doctype=doctype,
                                                                    docname=doc.name)
            if not gl_columns:
                gl_columns = result['gl_columns']
            gl_data.extend(result['gl_data'])

    return {"gl_columns": gl_columns, "gl_data": gl_data}


def show_accounting_ledger_preview_per_transaction(filters, doctype, docname):
    doc = frappe.get_doc(doctype, docname)
    doc.run_method("before_gl_preview")
    gl_columns, gl_data = get_accounting_ledger_preview(doc, filters)
    return {"gl_columns": gl_columns, "gl_data": gl_data}


def get_column_index(gl_columns, column_name):
    index = -1
    for column in gl_columns:
        index += 1
        if column_name.lower() in ("debit", "credit"):
            if column_name.lower() in column.get("name").lower():
                return index
        else:
            if column.get("name").lower() == column_name.lower():
                return index
    return None


def add_mapped_gl_record(gl_record, gl_columns):
    # TODO: remove this function; not used
    if not gl_record:
        return None
    else:
        return {
            "posting_date": gl_record[get_column_index(gl_columns, 'Posting Date')],
            "account": gl_record[get_column_index(gl_columns, 'Account')],
            "debit": gl_record[get_column_index(gl_columns, 'debit')],
            "credit": gl_record[get_column_index(gl_columns, 'credit')],
            "against_account": gl_record[get_column_index(gl_columns, 'Against Account')],
            "party_type": gl_record[get_column_index(gl_columns, 'Party Type')],
            "party": gl_record[get_column_index(gl_columns, 'Party')],
            "cost_center": gl_record[get_column_index(gl_columns, 'Cost Center')],
            "voucher_type": gl_record[get_column_index(gl_columns, 'Against Voucher Type')],
            "voucher_id": gl_record[get_column_index(gl_columns, 'Against Voucher')],
        }


def create_columns():
    return [
        {"fieldname": "voucher_status",
         "fieldtype": "Data",
         "label": "Status",
         "width": 100
         },
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
        },
        {
            "fieldname": "voucher_subtype",
            "fieldtype": "Data",
            "label": "Voucher Subtype",
            "width": 100
        },
        {
            "fieldname": "against",
            "fieldtype": "Data",
            "label": "Against",
            "width": 100
        },
        {
            "fieldname": "against_voucher_type",
            "fieldtype": "Data",
            "label": "Against Voucher Type",
            "width": 100
        },
        {
            "fieldname": "against_voucher_id",
            "fieldtype": "Data",
            "label": "Against Voucher ID",
            "width": 100
        }
    ]
