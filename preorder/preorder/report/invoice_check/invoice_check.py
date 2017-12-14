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
		count_1 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Full Payment'""", cl.name)[0][0]
		count_2 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Down Payment'""", cl.name)[0][0]
		count_3 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Non Project Payment'""", cl.name)[0][0]
		count_4 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Progress Payment'""", cl.name)[0][0]
		count_5 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Termin Payment'""", cl.name)[0][0]
		count_6 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Retention Payment'""", cl.name)[0][0]
		if count_1 == 0 and count_2 == 0 and count_3 == 0 and count_4 == 0 and count_5 == 0 and count_6 == 0:
			count = 1
		else:
			if count_1 >= count_2 and count_1 >= count_3 and count_1 >= count_4 and count_1 >= count_5 and count_1 >= count_6:
				count = count_1
			elif count_2 >= count_1 and count_2 >= count_3 and count_2 >= count_4 and count_2 >= count_5 and count_2 >= count_6:
				count = count_2
			elif count_3 >= count_1 and count_3 >= count_2 and count_3 >= count_4 and count_3 >= count_5 and count_3 >= count_6:
				count = count_3
			elif count_4 >= count_1 and count_4 >= count_2 and count_4 >= count_3 and count_4 >= count_5 and count_4 >= count_6:
				count = count_4
			elif count_5 >= count_1 and count_5 >= count_2 and count_5 >= count_3 and count_5 >= count_4 and count_5 >= count_6:
				count = count_5
			else:
				count = count_6
		for q in range(0,count):
			i = flt(q)+1
			count_si_1 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Full Payment' order by si.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
			if count_si_1 == 1:
				si_1 = frappe.db.sql("""select distinct(si.`name`) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Full Payment' order by si.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
			else:
				si_1 = ""
			count_si_2 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Down Payment' order by si.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
			if count_si_2 == 1:
				si_2 = frappe.db.sql("""select distinct(si.`name`) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Down Payment' order by si.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
			else:
				si_2 = ""
			count_si_3 = frappe.db.sql("""select count(distinct(si.`name`)) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Non Project Payment' order by si.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
			if count_si_3 == 1:
				si_3 = frappe.db.sql("""select distinct(si.`name`) from `tabSales Invoice Item` sii inner join `tabSales Invoice` si on si.`name` = sii.parent where si.docstatus != '2' and sii.sales_order = %s and si.type_of_invoice = 'Non Project Payment' order by si.idx asc limit %s,%s""", (cl.name, q, i))[0][0]
			else:
				si_3 = ""
			data.append([cl.transaction_date, cl.name, cl.status, si_1, si_2, si_3])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("SO Date")+":Date:90",
		_("Sales Order")+":Link/Sales Order:110",
		_("Status")+":Data:130",
		_("Full Payment")+":Link/Sales Invoice:110",
		_("Down Payment")+":Link/Sales Invoice:110",
		_("Non Project Payment")+":Link/Sales Invoice:110",
	]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and so.transaction_date >= '%s'" % frappe.db.escape(filters["from_date"])
	if filters.get("to_date"):
		conditions += " and so.transaction_date <= '%s'" % frappe.db.escape(filters["to_date"])

	return conditions
