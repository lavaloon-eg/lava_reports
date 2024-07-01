# Copyright (c) 2024, lavaloon and contributors
# For license information, please see license.txt

import frappe
from erpnext.controllers.stock_controller import get_accounting_ledger_preview


def execute(filters=None):
    columns, data = [], []
    columns = create_columns()
    # TODO: remove the sql query code
    '''
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
                WHERE je.company=%(filter_company)s
                    AND je.`posting_date` BETWEEN %(filter_from_date)s and %(filter_to_date)s
                ORDER BY je.posting_date
        """
    data = frappe.db.sql(sql, values={
        "filter_company": filters['filter_company'],
        "filter_from_date": filters['filter_from_date'],
        "filter_to_date": filters['filter_to_date'],
    }, as_dict=1)
    '''
    result = show_accounting_ledger_preview_bulk(filters=filters)
    frappe.db.rollback()
    for record in result['gl_data']:
        data.append(add_mapped_gl_record(record, result['gl_columns']))

    # data.sort(key=lambda x: x[get_column_index(result['gl_columns'], 'Posting Date')], reverse=False)

    return columns, data


def show_accounting_ledger_preview_bulk(filters):
    filters['include_dimensions'] = 1
    filters['company'] = filters['filter_company']
    doctypes = ["Purchase Invoice", "Payment Entry", "Journal Entry"]
    gl_columns, gl_data = [], []
    for doctype in doctypes:
        docs_filters = {
            'company': filters['filter_company'],
            'posting_date': ['between', (filters['filter_from_date'],
                                         filters['filter_to_date'])]
        }
        if filters['filter_include_submitted'] == 'No':
            docs_filters['docstatus'] = ["=", 0]
        else:
            docs_filters['docstatus'] = ["<", 2]

        docs = frappe.db.get_list(doctype,
                                  filters=docs_filters,
                                  order_by='posting_date')
        for doc in docs:
            result = show_accounting_ledger_preview_per_transaction(filters=filters,
                                                                    doctype=doctype,
                                                                    docname=doc.name)
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
            "project": None,  # TODO: drop the field because not available in the preview method's columns
            "remark": None  # TODO: drop the field because not available in the preview method's columns
        }


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
