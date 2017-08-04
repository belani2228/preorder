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

	def update_rfsq_inquiry(self):
		tampung = []
		ada = []
		for row in self.items:
			inquiry_id = frappe.db.sql("""select parent from `tabInquiry Item` where `name` = %s""", row.inquiry_detail)[0][0]
			if inquiry_id not in tampung:
				tampung.append(inquiry_id)
				cek_inquiry_id = frappe.db.get_value("Request for Supplier Quotation Inquiry", {"parent": self.name, "inquiry": inquiry_id}, "name")
				if not cek_inquiry_id:
					ada.append("tidak ada")
					aa = frappe.get_doc({
						"doctype": "Request for Supplier Quotation Inquiry",
						"parent": self.name,
						"parentfield": "inquiry",
						"parenttype": "Request for Supplier Quotation",
						"inquiry": inquiry_id,
						"customer": "CUSTOMER 01",
						"customer_name": "CUSTOMER 01",
						"transaction_date": self.date
					}).insert()
				else:
					ada.append("ada")
		temp = ', '.join(ada)
		frappe.throw(temp)

	def get_items(self):
#		tampung = []
		self.set('items', [])
		for row in self.inquiry:
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
