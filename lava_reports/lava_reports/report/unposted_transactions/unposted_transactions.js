// Copyright (c) 2025, lavaloon and contributors
// For license information, please see license.txt

frappe.query_reports["Unposted Transactions"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 0
		},
		{
			"fieldname": "doctype",
			"label": __("Transaction Type"),
			"fieldtype": "Select",
			"options": [
				"",
				"Quotation",
				"Sales Order",
				"Delivery Note",
				"Sales Invoice",
				"Purchase Order",
				"Purchase Receipt",
				"Purchase Invoice",
				"Payment Entry"
			],
			"reqd": 0
		}
	],
	"formatter": (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "id" && data.type) {
			const doc_type_slug = frappe.router.slug(data.type)

			value = `<a href="/app/${doc_type_slug}/${data.id}" 
						data-doctype="${data.type}" 
						data-name="${data.id}" 
						data-value="${data.id}">
						${data.id}
					</a>`;
		}

		if (column.fieldname === "full_name" && data.full_name && data.created_by) {
			value = `<a href="/app/user/${data.created_by}" 
						data-doctype="User" 
						data-name="${data.created_by}" 
						data-value="${data.created_by}">
						${data.full_name}
					</a>`;
		}

		return value;
	}
};
