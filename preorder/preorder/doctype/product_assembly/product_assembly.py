# -*- coding: utf-8 -*-
# Copyright (c) 2017, ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class ProductAssembly(Document):
	def on_submit(self):
		self.check_item()
		self.insert_item_to_inquiry()

	def on_cancel(self):
		self.cancel_item_in_inquiry()

	def check_item(self):
		if not self.items:
			frappe.throw(_("Item must be filled"))

	def insert_item_to_inquiry(self):
		count = frappe.db.sql("""select idx from `tabInquiry All Item` where parent = %s order by idx desc limit 1""", self.inquiry)[0][0]
		for row in self.items:
			count = count+1
			items = frappe.get_doc({
				"doctype": "Inquiry All Item",
				"parent": self.inquiry,
				"parentfield": "item_all",
				"parenttype": "Inquiry",
				"idx": count,
				"item_description": row.item_description,
				"qty": row.qty,
				"uom": row.uom,
				"is_product_assembly": 1,
				"product_assembly": self.name,
				"product_assembly_item": row.name
			})
			items.insert()

	def cancel_item_in_inquiry(self):
		frappe.db.sql("""delete from `tabInquiry All Item` where product_assembly = %s""", self.name)
