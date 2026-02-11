# Copyright (c) 2026, lavaloon and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LavaAuditSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from lava_reports.lava_reports.doctype.lava_tracked_doctype.lava_tracked_doctype import LavaTrackedDoctype
		from lava_reports.lava_reports.doctype.lava_tracker.lava_tracker import LavaTracker

		tracked_doctypes: DF.Table[LavaTrackedDoctype]
		trackers: DF.Table[LavaTracker]
	# end: auto-generated types
	pass
