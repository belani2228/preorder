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
	sl_entries = frappe.db.sql("""select `name`, transaction_date, `status` from `tabSales Order` so where so.docstatus = '1' %s""" % conditions, as_dict=1)
	for cl in sl_entries:
		data.append([cl.transaction_date, cl.name, cl.status])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("SO Date")+":Date:90",
		_("Sales Order")+":Link/Sales Order:110",
		_("Status")+":Data:130",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and so.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and so.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions
