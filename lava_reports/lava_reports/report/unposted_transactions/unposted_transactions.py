# Copyright (c) 2025, lavaloon and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType
from frappe.query_builder.custom import ConstantColumn


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_data(filters=None):
	filters = filters or {}

	doc_types = [
		"Sales Invoice",
		"Quotation",
		"Sales Order",
		"Payment Entry"
	]

	if filters.get("doctype"):
		doc_types = [filters.get("doctype")]

	union_query = None

	for dt in doc_types:
		table = DocType(dt)

		query = (
			frappe.qb
			.from_(table)
			.select(
				table.name.as_("id"),
				ConstantColumn(dt).as_("type"),
				table.owner.as_("created_by"),
				table.creation.as_("creation_date"),
				table.company.as_("company")
			)
			.where(table.docstatus == 0)
		)

		if filters.get("company"):
			query = query.where(table.company == filters.get("company"))

		if union_query is None:
			union_query = query
		else:
			union_query += query 

	return union_query.run(as_dict=True) if union_query else []


def get_columns():
	return [
		{
			"label": _("ID"),
			"fieldname": "id",
			"fieldtype": "Link",
			"options": "DocType",
			"width": 250
		},
		{
			"label": _("Type"),
			"fieldname": "type",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Created By"),
			"fieldname": "created_by",
			"fieldtype": "Data",
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
