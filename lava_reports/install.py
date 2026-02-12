from lava_reports.patches._2026_02_11_add_audit_settings import execute as add_audit_settings


def after_install():
    add_audit_settings()
