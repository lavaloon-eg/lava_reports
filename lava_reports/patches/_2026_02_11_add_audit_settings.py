import frappe


def execute():
    role_prefixes = ['Lavaloon']
    users = ['Administrator']
    doctypes_to_track = [
        'Quotation',
        'Sales Order',
        'Delivery Note',
        'Sales Invoice',
        'POS Invoice',
        'Sales Return',
        'Supplier Quotation',
        'Request For Quotation',
        'Purchase Order',
        'Purchase Receipt',
        'Purchase Invoice',
        'Purchase Return',
        'Material Request',
        'Stock Entry',
        'Stock Reconciliation',
        'Stock Ledger Entry',
        'Serial No',
        'Batch',
        'Journal Entry',
        'Payment Entry',
        'Payment Request',
        'GL Entry',
        'Dunning',
        'Work Order',
        'Job Card',
        'Production Plan',
        'BOM',
        'Lead',
        'Opportunity',
        'Customer',
        'Supplier',
        'User',
        'Role',
        'Item',
        'Item Group',
        'Warehouse',
        'Company',
        'Account',
        'Cost Center',
        'Project',
    ]

    roles = set()
    for role_prefix in role_prefixes:
        matched_roles = frappe.get_all(
            'Role',
            filters={'role_name': ['like', f'%{role_prefix}%']},
            pluck='name',
        )
        roles.update(matched_roles)

    settings = frappe.get_single('Lava Audit Settings')

    existing_tracked = {row.document_type for row in settings.tracked_doctypes}
    for doctype in doctypes_to_track:
        if frappe.db.exists('DocType', doctype):
            if doctype not in existing_tracked:
                settings.append('tracked_doctypes', {'document_type': doctype})

    existing_trackers = {(row.document_type, row.document_name) for row in settings.trackers}

    for user in users:
        if ('User', user) not in existing_trackers:
            settings.append('trackers', {'document_type': 'User', 'document_name': user})

    for role in roles:
        if ('Role', role) not in existing_trackers:
            settings.append('trackers', {'document_type': 'Role', 'document_name': role})

    settings.save(ignore_permissions=True)
