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

	for ri in sl_entries:
		data.append([ri.dn_date, ri.delivery, ri.dn_total, ri.hpp, ri.si_date, ri.no_si, ri.si_total])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Tgl DN")+":Date:100",
		_("No DN")+":Link/Delivery Note:100",
		_("Nilai DN")+":Currency:100",
		_("HPP")+":Currency:100",
		_("Tgl SI")+":Date:100",
		_("No SI")+":Link/Sales Invoice:100",
		_("Nilai SI")+":Currency:100",
	]

	return columns

def get_conditions(filters):
	conditions = ""
#	if filters.get("customer"):
#		conditions += " and customer = '%s'" % frappe.db.escape(filters["customer"])
#	if filters.get("from_date"):
#		conditions += " and date >= '%s'" % frappe.db.escape(filters["from_date"])
#	if filters.get("to_date"):
#		conditions += " and date <= '%s'" % frappe.db.escape(filters["to_date"])
	return conditions

def get_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select dn.posting_date as dn_date, dn.`name` as delivery, dn.net_total as dn_total, (select sum(valuation_rate) from `tabStock Ledger Entry` where voucher_no = dn.`name`) as hpp, si.posting_date as si_date, si.`name` as no_si, si.net_total as si_total from `tabDelivery Note` dn left join `tabSales Invoice` si on dn.inquiry = si.inquiry and si.docstatus = '1' and si.type_of_invoice in ('Retention', 'Non Project Payment') where dn.docstatus = '1' %s order by dn.`name` asc""" % conditions, as_dict=1)
