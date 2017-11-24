# Copyright (c) 2013, ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	columns = get_columns()
	sl_entries = get_entries(filters)
	data = []

	for cl in sl_entries:
		data.append([cl.inquiry, cl.inquiry_status, cl.inquiry_date, cl.quotation, cl.quotation_status, cl.quotation_date, cl.sales_order, cl.so_status, cl.so_date, cl.delivery, cl.dn_status, cl.delivery_date, cl.invoice, cl.invoice_status, cl.si_date])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Inquiry")+":Link/Inquiry:120",
		_("Inquiry Status")+"::100",
		_("Inquiry Date")+":Date:100",
		_("Quotation")+":Link/Quotation:120",
		_("Quotation Status")+"::100",
		_("Quotation Date")+":Date:100",
		_("Sales Order")+":Link/Sales Order:120",
		_("Sales Order Status")+"::100",
		_("Sales Order Date")+":Date:100",
		_("Delivery Note")+":Link/Delivery Note:120",
		_("Delivery Note Status")+"::100",
		_("Delivery Note Date")+":Date:100",
		_("Sales Invoice")+":Link/Sales Invoice:120",
		_("Sales Invoice Status")+"::100",
		_("Sales Invoice Date")+":Date:100",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and iq.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and iq.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		select
			distinct(iq.`name`) as inquiry,
			iq.`status` as inquiry_status,
			iq.transaction_date as inquiry_date,
			qu.`name` as quotation,
			qu.so_status as quotation_status,
			qu.transaction_date as quotation_date,
			so.`name` as sales_order,
			so.`status` as so_status,
			so.transaction_date as so_date,
			dn.`name` as delivery,
			dn.`status` as dn_status,
			dn.posting_date as delivery_date,
			si.`name` as invoice,
			si.`status` as invoice_status,
			si.posting_date as si_date
		from `tabInquiry` iq
		left join `tabQuotation Item` qi on iq.`name` = qi.inquiry and qi.docstatus != '2'
		left join `tabQuotation` qu on qi.parent = qu.`name` and qu.docstatus != '2'
		left join `tabSales Order Item` soi on iq.`name` = soi.inquiry and soi.docstatus != '2'
		left join `tabSales Order` so on so.`name` = soi.parent and so.docstatus != '2'
		left join `tabDelivery Note Item` dni on dni.inquiry = iq.`name` and dni.docstatus != '2'
		left join `tabDelivery Note` dn on dn.`name` = dni.parent and dn.docstatus != '2'
		left join `tabSales Invoice Item` sii on sii.inquiry = iq.`name` and sii.docstatus != '2'
		left join `tabSales Invoice` si on si.`name` = sii.parent and si.docstatus != '2'
		where iq.docstatus != '2' %s order by iq.transaction_date asc""" % conditions, as_dict=1)
