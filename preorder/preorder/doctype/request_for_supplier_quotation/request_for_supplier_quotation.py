# -*- coding: utf-8 -*-
# Copyright (c) 2017, ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class RequestforSupplierQuotation(Document):
	def validate(self):
		self.update_rfsq_inquiry()

	def on_update(self):
		self.update_rfsq_inquiry()

	def update_rfsq_inquiry(self):
		tampung = []
		for row in self.items:
			inquiry_id = frappe.db.get_value("Inquiry Item", row.inquiry_detail, "parent")
			if inquiry_id not in tampung:
				tampung.append(inquiry_id)
				cek_inquiry_id = frappe.db.get_value("Request for Supplier Quotation Inquiry", {"parent": self.name, "inquiry": inquiry_id}, "name")
				if not cek_inquiry_id:
					inq = frappe.db.get_value("Inquiry", inquiry_id, ["customer", "customer_name"], as_dict=1)
					doc = frappe.get_doc({
						"doctype": "Request for Supplier Quotation Inquiry",
						"parent": self.name,
						"parentfield": "inquiry_tbl",
						"parenttype": "Request for Supplier Quotation",
						"inquiry": inquiry_id,
						"customer": inq.customer,
						"customer_name": inq.customer_name,
						"transaction_date": self.transaction_date
					}).insert()

	def get_items(self):
#		tampung = []
		self.set('items', [])
		for row in self.inquiry_tbl:
			komponen = frappe.db.sql("""SELECT b.item_description, b.qty, b.uom, b.`name`
				FROM `tabInquiry` a, `tabInquiry Item` b
				WHERE a.`name` = b.parent AND a.docstatus = '1' AND a.`name` = %s
				ORDER by b.idx ASC""", row.inquiry, as_dict=1)

			for d in komponen:
				nl = self.append('items', {})
				nl.item_description = d.item_description
				nl.qty = d.qty
				nl.uom = d.uom
				nl.inquiry_detail = d.name
#			tampung.append(row.inquiry)
#		temp = ', '.join(tampung)
#		frappe.throw(temp)

	def refresh_tbl_inquiry(self):
		pass

@frappe.whitelist()
def make_supplier_quotation(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")

	def update_item(source, target, source_parent):
		target.item_code = "Tampungan"
		target.conversion_factor = 1

	sq = get_mapped_doc("Request for Supplier Quotation", source_name, {
		"Request for Supplier Quotation": {
			"doctype": "Supplier Quotation",
			"field_no_map": [
				"naming_series"
			],
		},
		"Request for Supplier Quotation Item":{
			"doctype": "Supplier Quotation Item",
			"field_map": {
				"uom": "stock_uom",
				"name": "request_for_supplier_quotation_item"
			},
			"postprocess": update_item
		}
	}, target_doc, set_missing_values)
	return sq
