# -*- coding: utf-8 -*-
# Copyright (c) 2017, ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Inquiry(Document):
	pass

@frappe.whitelist()
def make_rfsq(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method("set_missing_values")

	si = get_mapped_doc("Inquiry", source_name, {
		"Inquiry": {
			"doctype": "Request for Supplier Quotation",
			"field_no_map": [
				"naming_series"
			],
			"field_map": {
				"transaction_date":"date"
			},
		},
		"Inquiry Item":{
			"doctype": "Request for Supplier Quotation Item",
			"field_map": {
				"name":"inquiry_detail"
			},
		}
	}, target_doc, set_missing_values)
	return si
