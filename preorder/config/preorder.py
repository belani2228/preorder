from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"items": [
				{
					"type": "doctype",
					"name": "Inquiry",
					"description": _("Inquiry")
				},
				{
					"type": "doctype",
					"name": "Request for Supplier Quotation",
					"description": _("Request for Supplier Quotation")
				},
			]
		},
		{
			"label": _("Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "Item Settings",
					"description": _("Item Settings")
				},
			]
		}
	]
