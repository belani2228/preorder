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
		data.append([ri.name, ri.net_total, ri.hpp])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("No DN")+":Link/Delivery Note:100",
		_("Nilai DN")+":Currency:100",
		_("HPP")+":Currency:100",
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
	return frappe.db.sql("""select dn.`name`, dn.net_total, (select sum(valuation_rate) from `tabStock Ledger Entry` WHERE voucher_no = dn.`name`) as hpp FROM `tabDelivery Note` dn where dn.docstatus = '1' %s order by `name` asc""" % conditions, as_dict=1)
