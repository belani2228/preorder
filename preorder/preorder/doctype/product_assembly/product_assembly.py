# -*- coding: utf-8 -*-
# Copyright (c) 2017, ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ProductAssembly(Document):
	def on_submit(self):
		self.check_item()
		self.insert_item_to_inquiry()
		self.check_finish_assembly()
		frappe.db.set(self, 'status', 'Submitted')

	def on_cancel(self):
		self.cancel_item_in_inquiry()
		frappe.db.set(self, 'status', 'Cancelled')

	def check_item(self):
		if not self.items:
			frappe.throw(_("Item must be filled"))

	def insert_item_to_inquiry(self):
		count = frappe.db.sql("""select idx from `tabInquiry All Item` where parent = %s order by idx desc limit 1""", self.inquiry)[0][0]
		for row in self.items:
			count = count+1
			total_qty = flt(row.qty) * flt(self.quantity)
			items = frappe.get_doc({
				"doctype": "Inquiry All Item",
				"parent": self.inquiry,
				"parentfield": "item_all",
				"parenttype": "Inquiry",
				"idx": count,
				"item_description": row.item_description,
				"qty": total_qty,
				"uom": row.uom,
				"is_product_assembly": 1,
				"product_assembly": self.name,
				"product_assembly_item": row.name
			})
			items.insert()

	def cancel_item_in_inquiry(self):
		frappe.db.sql("""delete from `tabInquiry All Item` where product_assembly = %s""", self.name)

	def check_finish_assembly(self):
		count = frappe.db.sql("""select count(idx) from `tabProduct Assembly` where inquiry = %s and docstatus = '0'""", self.inquiry)[0][0]
		if count == 0:
			frappe.db.sql("""update `tabInquiry` set complete_assembly = 'Yes' where `name` = %s""", self.inquiry)

@frappe.whitelist()
def make_product_bundle(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method("set_missing_values")

	pa = get_mapped_doc("Product Assembly", source_name, {
		"Product Assembly": {
			"doctype": "Product Bundle",
			"field_no_map": [
				"parent_item"
			],
			"field_map": {
				"parent_item":"item_description",
				"name": "product_assembly"
			},
		},
		"Product Assembly Item":{
			"doctype": "Product Bundle Item",
			"field_map": {
				"name":"product_assembly_detail"
			},
		}
	}, target_doc, set_missing_values)
	return pa
