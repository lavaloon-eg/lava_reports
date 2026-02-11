# Copyright (c) 2026, lavaloon and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LavaAuditLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action: DF.Literal["Create", "Update", "Delete"]
		date: DF.Date | None
		document_name: DF.Data | None
		document_type: DF.Data | None
		user: DF.Link | None
	# end: auto-generated types
	pass
