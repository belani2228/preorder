from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def update_quotation(doc, method):
    if doc.inquiry != None:
        cek = frappe.db.get_value("Inquiry", doc.inquiry, "quotation")
        if cek != None:
            frappe.throw(_("Inquiry "+doc.inquiry+" has been used in other Quotation"))

def submit_quotation(doc, method):
    if doc.inquiry != None:
        cek = frappe.db.get_value("Inquiry", doc.inquiry, "quotation")
        if cek != None:
            frappe.throw(_("Inquiry "+doc.inquiry+" has been used in other Quotation"))
        else:
            frappe.db.sql("""update `tabInquiry` set quotation = %s where `name` = %s""", (doc.name, doc.inquiry))

def cancel_quotation(doc, method):
    if doc.inquiry != None:
        frappe.db.sql("""update `tabInquiry` set quotation = null where `name` = %s""", doc.inquiry)

def update_supplier_quotation(sq):
    ada = []
    for i in sq:
        count1 = frappe.db.sql("""select count(*) from `tabSupplier Quotation Item` where parent = %s and quotation_detail is not null""", i)[0][0]
        count2 = frappe.db.sql("""select count(*) from `tabSupplier Quotation Item` where parent = %s""", i)[0][0]
        if cstr(count1) == cstr(count2):
            frappe.db.sql("""update `tabSupplier Quotation` set terpakai = 'Full' where `name` = %s""", i)
        else:
            frappe.db.sql("""update `tabSupplier Quotation` set terpakai = null where `name` = %s""", i)

def submit_supplier_quotation(doc, method):
    sq = doc.name
    items = frappe.db.sql("""select * from `tabSupplier Quotation Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        frappe.db.sql("""update `tabInquiry` set sq = 'Yes' where `name` = %s""", row.inquiry)
        frappe.db.sql("""update `tabInquiry Item` set item_description = %s, rate_1 = '0', rate_2 = '0', rate_3 = '0', supplier_1 = null, supplier_2 = null, supplier_3 = null, supplier_name_1 = null, supplier_name_2 = null, supplier_name_3 = null where `name` = %s""", (row.item_description, row.inquiry_detail))
        frappe.db.sql("""update `tabRequest for Supplier Quotation` set status = 'Completed' where `name` = %s""", row.request_for_supplier_quotation)

    update_inquiry_items(sq)

def update_inquiry_items(sq):
    items = frappe.db.sql("""select * from `tabSupplier Quotation Item` where parent = %s""", sq, as_dict=1)
    for row in items:
        sqi1 = frappe.db.sql("""select a.rate, b.supplier, b.supplier_name from `tabSupplier Quotation Item` a inner join `tabSupplier Quotation` b on a.parent = b.`name` where b.docstatus = '1' and a.inquiry_detail = %s order by b.`name` asc limit 0,1""", row.inquiry_detail, as_dict=1)
        for a1 in sqi1:
            frappe.db.sql("""update `tabInquiry Item` set rate_1 = %s, supplier_1 = %s, supplier_name_1 = %s where `name` = %s""", (a1.rate, a1.supplier, a1.supplier_name, row.inquiry_detail))
        sqi2 = frappe.db.sql("""select a.rate, b.supplier, b.supplier_name from `tabSupplier Quotation Item` a inner join `tabSupplier Quotation` b on a.parent = b.`name` where b.docstatus = '1' and a.inquiry_detail = %s order by b.`name` asc limit 1,1""", row.inquiry_detail, as_dict=1)
        for a2 in sqi2:
            frappe.db.sql("""update `tabInquiry Item` set rate_2 = %s, supplier_2 = %s, supplier_name_2 = %s where `name` = %s""", (a2.rate, a2.supplier, a2.supplier_name, row.inquiry_detail))
        sqi3 = frappe.db.sql("""select a.rate, b.supplier, b.supplier_name from `tabSupplier Quotation Item` a inner join `tabSupplier Quotation` b on a.parent = b.`name` where b.docstatus = '1' and a.inquiry_detail = %s order by b.`name` asc limit 2,1""", row.inquiry_detail, as_dict=1)
        for a3 in sqi3:
            frappe.db.sql("""update `tabInquiry Item` set rate_3 = %s, supplier_3 = %s, supplier_name_3 = %s where `name` = %s""", (a3.rate, a3.supplier, a3.supplier_name, row.inquiry_detail))

def cancel_supplier_quotation(doc, method):
    sq = doc.name
    tampung = []
    items = frappe.db.sql("""select * from `tabSupplier Quotation Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        frappe.db.sql("""update `tabInquiry Item` set rate_1 = '0', rate_2 = 0, rate_3 = 0, supplier_1 = null, supplier_2 = null, supplier_3 = null, supplier_name_1 = null, supplier_name_2 = null, supplier_name_3 = null where `name` = %s""", row.inquiry_detail)
        frappe.db.sql("""update `tabRequest for Supplier Quotation` set status = 'Submitted' where `name` = %s""", row.request_for_supplier_quotation)
        sqi1 = frappe.db.sql("""select a.rate, b.supplier, b.supplier_name from `tabSupplier Quotation Item` a inner join `tabSupplier Quotation` b on a.parent = b.`name` where b.docstatus = '1' and a.inquiry_detail = %s and b.`name` != %s order by b.`name` asc limit 0,1""", (row.inquiry_detail, sq), as_dict=1)
        for a1 in sqi1:
            frappe.db.sql("""update `tabInquiry Item` set rate_1 = %s, supplier_1 = %s, supplier_name_1 = %s where `name` = %s""", (a1.rate, a1.supplier, a1.supplier_name, row.inquiry_detail))
        sqi2 = frappe.db.sql("""select a.rate, b.supplier, b.supplier_name from `tabSupplier Quotation Item` a inner join `tabSupplier Quotation` b on a.parent = b.`name` where b.docstatus = '1' and a.inquiry_detail = %s and b.`name` != %s order by b.`name` asc limit 1,1""", (row.inquiry_detail, sq), as_dict=1)
        for a2 in sqi2:
            frappe.db.sql("""update `tabInquiry Item` set rate_2 = %s, supplier_2 = %s, supplier_name_2 = %s where `name` = %s""", (a2.rate, a2.supplier, a1.supplier_name, row.inquiry_detail))
        sqi3 = frappe.db.sql("""select a.rate, b.supplier, b.supplier_name from `tabSupplier Quotation Item` a inner join `tabSupplier Quotation` b on a.parent = b.`name` where b.docstatus = '1' and a.inquiry_detail = %s and b.`name` != %s order by b.`name` asc limit 2,1""", (row.inquiry_detail, sq), as_dict=1)
        for a3 in sqi3:
            frappe.db.sql("""update `tabInquiry Item` set rate_3 = %s, supplier_3 = %s, supplier_name_3 = %s where `name` = %s""", (a3.rate, a3.supplier, a1.supplier_name, row.inquiry_detail))
        if row.inquiry not in tampung:
            tampung.append(row.inquiry)
    if tampung:
        for i in tampung:
            a = frappe.db.sql("""select count(*) from `tabSupplier Quotation Item` where docstatus = '1' and inquiry = %s and parent != %s""", (i, doc.name))[0][0]
            if cstr(a) >= 1:
                frappe.db.sql("""update `tabInquiry` set sq = 'Yes' where `name` = %s""", i)
            else:
                frappe.db.sql("""update `tabInquiry` set sq = 'No' where `name` = %s""", i)

def submit_sales_order(doc, method):
    items = frappe.db.sql("""select * from `tabSales Order Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        if row.gunakan_1:
            frappe.db.sql("""update `tabSales Order Item` set selected_supplier = %s, approved_price = %s where `name` = %s""", (row.supplier_1, row.rate_1, row.name))
        if row.gunakan_2:
            frappe.db.sql("""update `tabSales Order Item` set selected_supplier = %s, approved_price = %s where `name` = %s""", (row.supplier_2, row.rate_2, row.name))
        if row.gunakan_3:
            frappe.db.sql("""update `tabSales Order Item` set selected_supplier = %s, approved_price = %s where `name` = %s""", (row.supplier_3, row.rate_3, row.name))

def submit_purchase_order(doc, method):
    items = frappe.db.sql("""select * from `tabPurchase Order Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        if row.sales_order_item:
            frappe.db.sql("""update `tabSales Order Item` set po_no = %s where `name` = %s""", (doc.name, row.sales_order_item))

def cancel_purchase_order(doc, method):
    items = frappe.db.sql("""select * from `tabPurchase Order Item` where parent = %s""", doc.name, as_dict=1)
    for row in items:
        if row.sales_order_item:
            frappe.db.sql("""update `tabSales Order Item` set po_no = null where `name` = %s""", row.sales_order_item)
