from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def submit_quotation(doc, method):
    sq = []
    items = frappe.db.sql("""select * from `tabQuotation Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        if row.supplier_quotation_item != None:
            frappe.db.sql("""update `tabSupplier Quotation Item` set quotation_detail = %s where `name` = %s""", (row.name, row.supplier_quotation_item))
            if row.supplier_quotation not in sq:
                sq.append(row.supplier_quotation)
    if sq:
        update_supplier_quotation(sq)

def update_supplier_quotation(sq):
    ada = []
    for i in sq:
        count1 = frappe.db.sql("""select count(*) from `tabSupplier Quotation Item` where parent = %s and quotation_detail is not null""", i)[0][0]
        count2 = frappe.db.sql("""select count(*) from `tabSupplier Quotation Item` where parent = %s""", i)[0][0]
        if cstr(count1) == cstr(count2):
            frappe.db.sql("""update `tabSupplier Quotation` set terpakai = 'Full' where `name` = %s""", i)
        else:
            frappe.db.sql("""update `tabSupplier Quotation` set terpakai = null where `name` = %s""", i)

def cancel_quotation(doc, method):
    sq = []
    items = frappe.db.sql("""select * from `tabQuotation Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        if row.supplier_quotation_item != None:
            frappe.db.sql("""update `tabSupplier Quotation Item` set quotation_detail = null where `name` = %s""", row.supplier_quotation_item)
            if row.supplier_quotation not in sq:
                sq.append(row.supplier_quotation)
    if sq:
        update_supplier_quotation(sq)

def submit_supplier_quotation(doc, method):
    items = frappe.db.sql("""select * from `tabSupplier Quotation Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        frappe.db.sql("""update `tabInquiry` set sq = 'Yes' where `name` = %s""", row.inquiry)

def cancel_supplier_quotation(doc, method):
    tampung = []
    items = frappe.db.sql("""select * from `tabSupplier Quotation Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        if row.inquiry not in tampung:
            tampung.append(row.inquiry)
    if tampung:
        for i in tampung:
            a = frappe.db.sql("""select count(*) from `tabSupplier Quotation Item` where docstatus = '1' and inquiry = %s and parent != %s""", (i, doc.name))[0][0]
            if cstr(a) <= 1:
                frappe.db.sql("""update `tabInquiry` set sq = 'Yes' where `name` = %s""", i)
            else:
                frappe.db.sql("""update `tabInquiry` set sq = 'No' where `name` = %s""", i)
