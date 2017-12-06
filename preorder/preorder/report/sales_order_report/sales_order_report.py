# Copyright (c) 2013, ridhosribumi and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	columns = get_columns()
	data = []

	conditions = get_conditions(filters)
	sl_entries = frappe.db.sql("""select `name`, transaction_date from `tabSales Order` so where so.docstatus = '1' and so.status in ('To Deliver and Bill', 'To Deliver')""", as_dict=1)
	for cl in sl_entries:
		count_so = frappe.db.sql("""select count(*) from `tabSales Order Item` where parent = %s""", cl.name)[0][0]
		for q in range(0,count_so):
			i = flt(q)+1
			items = frappe.db.sql("""select `name` from `tabSales Order Item` where parent = %s order by idx asc limit %s,%s """, (cl.name, q, i))[0][0]
			det = frappe.db.get_value("Sales Order Item", items, ["item_code", "description", "qty"], as_dict=1)
			po = frappe.db.get_value("Purchase Order Item", {"item_code": det.item_code, "sales_order": cl.name, "docstatus": ["!=", 2]}, "parent")
			po_date = frappe.db.get_value("Purchase Order", po, "transaction_date")
			po_status = frappe.db.get_value("Purchase Order", po, "status")
			actual_qty = det.item_code
#			actual_qty = frappe.db.sql("""select qty_after_transaction from `tabStock Ledger Entry` where item_code = %s order by `name` desc limit 1""", det.item_code)[0][0]
			if flt(q) == 0:
				data.append([cl.transaction_date, cl.name, det.item_code, det.description, det.qty, po, po_date, po_status, actual_qty])
			else:
				data.append(['', '', det.item_code, det.description, det.qty, po, po_date, po_status, actual_qty])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("SO Date")+":Date:150",
		_("Sales Order")+":Link/Sales Order:110",
		_("Item Code")+":Link/Item:150",
		_("Description")+":Data:150",
		_("Qty")+":Float:70",
		_("Purchase Order")+":Link/Purchase Order:110",
		_("PO Date")+":Date:100",
		_("PO Status")+":Data:100",
		_("Actual Qty")+":Data:70",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " and soi.warehouse >= '%s'" % frappe.db.escape(filters["company"])

	return conditions
