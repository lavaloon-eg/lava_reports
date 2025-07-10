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
				{ "label": "All", "value": "" },
				{ "label": "Quotation", "value": "Quotation" },
				{ "label": "Sales Order", "value": "Sales Order" },
				{ "label": "Delivery Note", "value": "Delivery Note" },
				{ "label": "Sales Invoice", "value": "Sales Invoice" },
				{ "label": "Purchase Order", "value": "Purchase Order" },
				{ "label": "Purchase Receipt", "value": "Purchase Receipt" },
				{ "label": "Purchase Invoice", "value": "Purchase Invoice" },
				{ "label": "Payment Entry", "value": "Payment Entry" },
				{ "label": "Journal Entry", "value": "Journal Entry" },
				{ "label": "Exchange Rate Revaluation", "value": "Exchange Rate Revaluation" }
			],
			"reqd": 0
		}
	],
	"onload": function (report) {
		const summary_elm = document.getElementById('message-summary');
		if (!summary_elm) {
			const page_container = report.$page[0];
			const filters_section = page_container.querySelector(".page-form");
			const message = __("This report shows all draft transactions across Sales, Purchase, and Payment cycles to help monitor pending business activities.");

			const message_summary_elm = document.createElement('div');
			message_summary_elm.classList.add('my-3', 'mx-auto');
			message_summary_elm.id = 'message-summary';
			message_summary_elm.style.width = '95%';

			const message_title = document.createElement('h5');
			message_title.innerText = 'Summary';

			const message_content = document.createElement('span');
			message_content.innerText = message;

			message_summary_elm.append(document.createElement('hr'), message_title, message_content);
			filters_section.appendChild(message_summary_elm);
		}
	},

	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (!data) return value;

		if (column.fieldname === "id" && data.type && data.id) {
			const doc_type_slug = frappe.router.slug(data.type);
			const id = frappe.utils.escape_html(data.id);
			const type = frappe.utils.escape_html(data.type);

			value = `
				<a href="/app/${doc_type_slug}/${id}" 
				data-doctype="${type}" 
				data-name="${id}" 
				data-value="${id}">
				${id}
				</a>`;
		}

		if (column.fieldname === "full_name" && data.full_name && data.created_by) {
			const full_name = frappe.utils.escape_html(data.full_name);
			const user_id = frappe.utils.escape_html(data.created_by);

			value = `
				<a href="/app/user/${user_id}" 
				data-doctype="User" 
				data-name="${user_id}" 
				data-value="${user_id}">
				${full_name}
				</a>`;
		}

		return value;
	}
};
