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
			"label": __("Document Type"),
			"fieldtype": "Select",
			"options": [
				"",
				"Sales Invoice",
				"Quotation",
				"Sales Order",
				"Payment Entry"
			],
			"reqd": 0
		}
	],
	"formatter": (value, row, column, data, default_formatter) => {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "id" && data.type) {
			const doc_type_slug = data.type.toLowerCase().replace(/\s+/g, '-');

			value = `<a href="/app/${doc_type_slug}/${data.id}" 
						data-doctype="${data.type}" 
						data-name="${data.id}" 
						data-value="${data.id}">
						${data.id}
					</a>`;
		}

		return value;
	}
};
