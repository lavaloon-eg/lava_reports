import frappe
from frappe import _
from frappe.utils import get_datetime
from frappe.query_builder.functions import DateFormat



def execute(filters=None):
    filters = filters or {}

    from_date = filters.get('from_date')
    to_date = filters.get('to_date')

    if not from_date or not to_date:
        frappe.throw(_('From Date and To Date are required'))

    from_date = get_datetime(from_date).date()
    to_date = get_datetime(to_date).date()

    if from_date > to_date:
        frappe.throw(_("From Date can't be greater than To Date"))

    columns = get_columns()
    data = get_data(filters, from_date, to_date)

    return columns, data


def get_data(filters, from_date, to_date):
    log = frappe.qb.DocType('Lava Audit Log')
    user = frappe.qb.DocType('User')

    users_filter = filters.get('users')

    query = (
        frappe.qb.from_(log)
        .select(
            log.name.as_('id'),
            DateFormat(log.date, '%a, %d %b %Y').as_('date'),
            log.user,
            user.full_name,
            log.document_type,
            log.document_name.as_('document_reference'),
            log.action
        )
        .left_join(user)
        .on(log.user == user.name)
        .where(log.date >= from_date)
        .where(log.date <= to_date)
    )

    if users_filter:
        query = query.where(log.user.isin(users_filter))

    return query.run(as_dict=True)

def get_columns():
    return [
        {
            'label': _('Audit ID'),
            'fieldname': 'id',
            'fieldtype': 'Link',
            'options': 'Lava Audit Log',
            'width': 150,
        },
        {
            'label': _('Date'),
            'fieldname': 'date',
            'fieldtype': 'Data',
            'width': 220,
        },
        {
            'label': _('User'),
            'fieldname': 'full_name',
            'fieldtype': 'Data',
            'width': 200,
        },
        {
            'label': _('Action'),
            'fieldname': 'action',
            'fieldtype': 'Data',
            'width': 120,
        },
        {
            'label': _('Document Type'),
            'fieldname': 'document_type',
            'fieldtype': 'Data',
            'width': 200,
        }
    ]
