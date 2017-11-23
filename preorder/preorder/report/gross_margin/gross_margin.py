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
		data.append([cl.invoice, cl.customer_name, cl.customer_group, cl.posting_date, cl.item_code, cl.item_name, cl.item_group, cl.warehouse, cl.qty, cl.selling_amount, cl.cogs, cl.gross_profit, cl.persen, cl.currency])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Sales Invoice")+":Link/Sales Invoice:120",
		_("Customer Name")+"::100",
		_("Customer Group")+":Link/Customer Group:120",
		_("Posting Date")+":Date:90",
		_("Item Code")+":Link/Item:120",
		_("Item Name")+"::120",
		_("Item Group")+":Link/Item Group:120",
		_("Warehouse")+":Link/Warehouse:120",
		_("Qty")+":Float:50",
		_("Selling Amount")+":Currency:110",
		_("COGS")+":Currency:110",
		_("Gross Profit")+":Currency:110",
		_("Gross Profit %")+":Float:110",
		_("Currency")+":Link/Currency:110",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("company"):
		conditions += " and si.company = '%s'" % frappe.db.escape(filters["company"])
	if filters.get("from_date"):
		conditions += " and si.posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and si.posting_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select si.`name` as invoice, si.customer_name, si.customer_group, si.posting_date,
	sii.item_code, sii.item_name, sii.item_group, sii.warehouse, dni.qty,
	(dni.qty * dni.rate) as selling_amount,
	(dni.qty * sle.valuation_rate) as cogs,
	((dni.qty * dni.rate) - (dni.qty * sle.valuation_rate)) as gross_profit,
	((((dni.qty * dni.rate) - (dni.qty * sle.valuation_rate)) / (dni.qty * dni.rate)) * 100) as persen,
	si.currency
	from `tabSales Invoice Item` sii
	inner join `tabSales Invoice` si on sii.parent = si.`name`
	inner join `tabDelivery Note Item` dni on sii.so_detail = dni.so_detail
	inner join `tabStock Ledger Entry` sle on dni.`name` = sle.voucher_detail_no
	where si.docstatus = '1' and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Standard') and dni.docstatus = '1' %s""" % conditions, as_dict=1)
