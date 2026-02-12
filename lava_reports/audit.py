from typing import cast

import frappe
from frappe.utils import nowdate

from lava_reports.lava_reports.doctype.lava_audit_settings.lava_audit_settings import LavaAuditSettings
from lava_reports.lava_reports.doctype.lava_audit_log.lava_audit_log import LavaAuditLog


def log_document_activity(doc, method):
    """
    Hook entry point for auditing document activity.

    This function determines whether the current document and user
    should be audited based on Lava Audit Settings. If the doctype
    is enabled and the current user (or their role) is tracked,
    an audit log entry is created.
    """

    audit_settings = cast(
        LavaAuditSettings,
        frappe.get_cached_doc("Lava Audit Settings")
    )

    is_doctype_audited = any(
        tracked_doctype.document_type == doc.doctype
        for tracked_doctype in audit_settings.tracked_doctypes
    )

    if not is_doctype_audited:
        return

    if not audit_settings.trackers:
        create_audit_log(doc, method)
        return

    current_user = frappe.session.user
    current_user_roles = frappe.get_roles()

    tracked_user_names = [
        tracker.document_name
        for tracker in audit_settings.trackers
        if tracker.document_type == "User"
    ]

    tracked_role_names = [
        tracker.document_name
        for tracker in audit_settings.trackers
        if tracker.document_type == "Role"
    ]

    is_user_tracked = current_user in tracked_user_names
    has_tracked_role = bool(set(current_user_roles).intersection(tracked_role_names))

    if not is_user_tracked and not has_tracked_role:
        return

    create_audit_log(doc, method)


def create_audit_log(doc, method):
    """
    Create a Lava Audit Log entry for the given document action.

    The action type is inferred from the document lifecycle hook:
    - Create: New document
    - Update: Existing document modified
    - Delete: Document removed
    """

    if method == "on_trash":
        action = "Delete"
    elif doc.get_doc_before_save():
        action = "Update"
    else:
        action = "Create"

    if frappe.db.exists('Lava Audit Log', {
        'date': nowdate(),
        'user': frappe.session.user,
        'document_type': doc.doctype,
        'document_name': doc.name,
        'action': action
    }):
        return

    audit_log = cast(LavaAuditLog, frappe.new_doc("Lava Audit Log"))
    audit_log.date = nowdate()
    audit_log.user = frappe.session.user
    audit_log.document_type = doc.doctype
    audit_log.document_name = doc.name
    audit_log.action = action
    audit_log.save(ignore_permissions=True)
