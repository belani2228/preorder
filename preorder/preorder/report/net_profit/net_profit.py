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
		data.append([cl.inquiry, cl.inquiry_date, cl.selling_amount, cl.payment, cl.payment_date, cl.cogs, cl.expenses, cl.net_profit])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Inquiry")+":Link/Inquiry:120",
		_("Posting Date")+":Date:100",
		_("Selling Amount")+":Currency:120",
		_("Payment")+":Link/Payment Entry:120",
		_("Payment Date")+":Date:100",
		_("HPP")+":Currency:120",
		_("Expenses")+":Currency:120",
		_("Net Profit")+":Currency:120",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and pe.posting_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and pe.posting_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select distinct(iq.`name`)as inquiry, iq.transaction_date as inquiry_date,
	(select sum(aa.net_amount) from `tabSales Invoice Item` aa where aa.inquiry = iq.`name`) as selling_amount,
	pe.`name` as payment, pe.posting_date as payment_date,
	(select sum((sle.actual_qty * -1) * sle.valuation_rate) from `tabDelivery Note Item` dni
	inner join `tabStock Ledger Entry` sle on dni.`name` = sle.voucher_detail_no where inquiry = iq.`name`) as cogs,
	(select total_debit from `tabJournal Entry` where inquiry = iq.`name`) as expenses,
	((select sum(aa.net_amount) from `tabSales Invoice Item` aa where aa.inquiry = iq.`name`) -
	(select sum((sle.actual_qty * -1) * sle.valuation_rate) from `tabDelivery Note Item` dni
	inner join `tabStock Ledger Entry` sle on dni.`name` = sle.voucher_detail_no where inquiry = iq.`name`) -
	(select total_debit from `tabJournal Entry` where inquiry = iq.`name`)) as net_profit
	from `tabInquiry` iq
	inner join `tabSales Invoice Item` sii on sii.inquiry = iq.`name`
	inner join `tabSales Invoice` si on si.`name` = sii.parent and si.type_of_invoice in ('Retention', 'Non Project Payment', 'Standard') and si.`status` = 'Paid'
	inner join `tabPayment Entry Reference` per on sii.parent = per.reference_name
	inner join `tabPayment Entry` pe on per.parent = pe.`name`
	where iq.docstatus = '1' %s order by iq.`name` asc""" % conditions, as_dict=1)
