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
		frappe.db.set(self, 'status', 'Draft')

	def on_submit(self):
		frappe.db.set(self, 'status', 'Submitted')

	def on_cancel(self):
		frappe.db.set(self, 'status', 'Cancelled')

	def get_items(self):
#		tampung = []
		self.set('items', [])
		for row in self.inquiry_tbl:
			komponen = frappe.db.sql("""SELECT b.item_description, b.qty, b.uom, a.`name` as inq, b.`name` as inq_det
				FROM `tabInquiry` a, `tabInquiry All Item` b
				WHERE a.`name` = b.parent AND a.docstatus = '1' AND a.`name` = %s AND a.status != "Lost"
				ORDER by b.idx ASC""", row.inquiry, as_dict=1)

			for d in komponen:
				nl = self.append('items', {})
				nl.item_description = d.item_description
				nl.qty = d.qty
				nl.uom = d.uom
				nl.inquiry = d.inq
				nl.inquiry_detail = d.inq_det
#			tampung.append(row.inquiry)
#		temp = ', '.join(tampung)
#		frappe.throw(temp)

	def declare_order_lost(self, arg):
		frappe.db.set(self, 'status', 'Lost')
		frappe.db.set(self, 'order_lost_reason', arg)
