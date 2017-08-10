from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def submit_quotation(doc, method):
    items = frappe.db.sql("""select * from `tabQuotation Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        if row.supplier_quotation_item != None:
            frappe.db.sql("""update `tabSupplier Quotation Item` set quotation_detail = %s where `name` = %s""", (row.name, row.supplier_quotation_item))

def cancel_quotation(doc, method):
    items = frappe.db.sql("""select * from `tabQuotation Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        if row.supplier_quotation_item != None:
            frappe.db.sql("""update `tabSupplier Quotation Item` set quotation_detail = null where `name` = %s""", row.supplier_quotation_item)
