// Copyright (c) 2026, lavaloon and contributors
// For license information, please see license.txt

frappe.query_reports['Lava Audit Report'] = {
    'filters': [
        {
            'fieldname': 'from_date',
            'label': __('From Date'),
            'fieldtype': 'Date',
            'reqd': 1,
            'default': frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            'fieldname': 'to_date',
            'label': __('To Date'),
            'fieldtype': 'Date',
            'reqd': 1,
            'default': frappe.datetime.get_today()
        },
        {
            'fieldname': 'users',
            'label': __('User'),
            'fieldtype': 'MultiSelectList',
			get_data: function(txt) {
				return frappe.db.get_link_options("User", txt);
			}
        }
    ],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "full_name" && data && data.creator) {
			value = `<a href="/app/user/${data.creator}"
				data-doctype="User"
				data-name="${data.creator}"
				data-value="${data.full_name}">${value}</a>`;
		}

		if (column.fieldname === "document_type" && data && data.document_reference) {
            const doctype_slug = data.document_type.toLowerCase().replace(/ /g, "-");
			value = `<a href="/app/${doctype_slug}/${data.document_reference}"
				data-doctype="${data.document_type}"
				data-name="${data.document_reference}"
				data-value="${data.document_reference}">${value}</a>`;
		}

		return value;
	}
};
