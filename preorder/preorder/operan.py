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
            frappe.throw(_("Inquiry {0} has been used in other Quotation").format(doc.inquiry))

def submit_quotation_2(doc, method):
    hitung = 0
    for row in doc.items:
        if row.alternative_item == 0:
            hitung = hitung+1
            frappe.db.sql("""update `tabQuotation Item` set count = %s where `name` = %s""", (hitung, row.name))

def submit_quotation(doc, method):
    if doc.inquiry != None:
        cek = frappe.db.get_value("Inquiry", doc.inquiry, "quotation")
        if cek != None:
            frappe.throw(_("Inquiry {0} has been used in other Quotation").format(doc.inquiry))
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

def validate_sales_order(doc, method):
    item_code = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'default_item_for_inquiry'""")[0][0]
    for i in doc.items:
        if i.item_code == item_code:
            frappe.throw(_("Please change the item to the actual item"))

def submit_sales_order(doc, method):
    if doc.inquiry:
        total_so = frappe.db.sql("""select sum(net_total) from `tabSales Order` where docstatus = '1' and inquiry = %s""", doc.inquiry)[0][0]
        frappe.db.sql("""update `tabInquiry` set nominal_sales_order = %s where `name` = %s""", (total_so, doc.inquiry))
#    if doc.assembly_item:
#        error = 0
#        for row in doc.assembly_item:
#            if not row.product_bundle:
#                error = 1
#        if error == 1:
#            frappe.throw(_("You must create <b>Product Bundle</b> before Submit this document"))

def submit_sales_order_2(doc, method):
    for row in doc.items:
        if row.quotation_item:
            cek_qty = frappe.db.sql("""select so_qty from `tabQuotation Item` where `name` = %s""", row.quotation_item)[0][0]
            add_qty = flt(cek_qty) + flt(row.qty)
            frappe.db.sql("""update `tabQuotation Item` set so_item = %s, so_qty = %s where `name` = %s""", (row.name, add_qty, row.quotation_item))

def cancel_sales_order(doc, method):
    if doc.inquiry:
        total_so = frappe.db.sql("""select sum(net_total) from `tabSales Order` where docstatus = '1' and inquiry = %s and `name` != %s""", (doc.inquiry, doc.name))[0][0]
        frappe.db.sql("""update `tabInquiry` set nominal_sales_order = %s where `name` = %s""", (total_so, doc.inquiry))

def cancel_sales_order_2(doc, method):
    for row in doc.items:
        if row.quotation_item:
            cek_qty = frappe.db.sql("""select so_qty from `tabQuotation Item` where `name` = %s""", row.quotation_item)[0][0]
            add_qty = flt(cek_qty) - flt(row.qty)
            frappe.db.sql("""update `tabQuotation Item` set so_item = %s, so_qty = %s where `name` = %s""", (row.name, add_qty, row.quotation_item))

def validate_delivery_note(doc, method):
    so_list = []
    error = 0
    for i in doc.items:
        if i.against_sales_order and i.against_sales_order not in so_list:
            so_list.append(i.against_sales_order)
            status_so = frappe.db.sql("""select `status` from `tabSales Order` where `name` = %s""", i.against_sales_order)[0][0]
            if doc.customer_group == 'Reseller' and status_so != 'To Deliver':
                error = 1
    if error == 1:
        frappe.msgprint(_("For customer <b>reseler</b>, the invoice must be paid off"))
    tampung = []
    for row in doc.items:
        item_group = frappe.db.get_value("Item", row.item_code, "item_group")
        default_item_group = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'default_item_group'""")[0][0]
        if item_group == default_item_group:
            pb = frappe.db.get_value("Product Bundle", {"new_item_code": row.item_code}, "name")
            if not pb:
                tampung.append(row.item_code)
    if tampung:
        descr = ', '.join(tampung)
        frappe.msgprint(_("Please create Product Bundle for item "+descr))

def submit_sales_invoice(doc, method):
    if doc.type_of_invoice == 'Standard':
        frappe.db.sql("""update `tabSales Invoice` set sales_order = null, delivery_note = null where `name` = %s""", doc.name)
    elif doc.type_of_invoice == 'Down Payment':
        frappe.db.sql("""update `tabSales Order` set down_payment = %s where `name` = %s""", (doc.name, doc.sales_order))
        frappe.db.sql("""update `tabSales Invoice` set delivery_note = null where `name` = %s""", doc.name)
    elif doc.type_of_invoice == 'Progress Payment':
        frappe.db.sql("""update `tabSales Invoice` set sales_order = null where `name` = %s""", doc.name)
    elif doc.type_of_invoice == 'Payment':
        dn = frappe.db.sql("""select * from `tabSales Invoice DN` where parent = %s""", doc.name, as_dict=1)
        for d in dn:
            frappe.db.sql("""update `tabDelivery Note` set sales_invoice = %s where `name` = %s""", (doc.name, d.delivery_note))
    if doc.inquiry:
        total_si = frappe.db.sql("""select sum(net_total)-sum(total_related_invoices) as nominal from `tabSales Invoice` where docstatus = '1' and inquiry = %s""", doc.inquiry)[0][0]
        frappe.db.sql("""update `tabInquiry` set nominal_sales_invoice = %s where `name` = %s""", (total_si, doc.inquiry))
        total_so = frappe.db.sql("""select nominal_sales_order from `tabInquiry` where docstatus = '1' and `name` = %s""", doc.inquiry)[0][0]
        if flt(total_so) == flt(total_si):
            frappe.db.sql("""update `tabInquiry` set status = 'Completed' where `name` = %s""", doc.inquiry)

def cancel_sales_invoice(doc, method):
    if doc.type_of_invoice == 'Down Payment':
        frappe.db.sql("""update `tabSales Order` set down_payment = null where `name` = %s""", doc.sales_order)
    elif doc.type_of_invoice == 'Payment':
        dn = frappe.db.sql("""select * from `tabSales Invoice DN` where parent = %s""", doc.name, as_dict=1)
        for d in dn:
            frappe.db.sql("""update `tabDelivery Note` set sales_invoice = null where `name` = %s""", d.delivery_note)
    if doc.inquiry:
        total_so = frappe.db.sql("""select sum(net_total)-sum(total_related_invoices) as nominal from `tabSales Invoice` where docstatus = '1' and inquiry = %s and `name` != %s""", (doc.inquiry, doc.name))[0][0]
        frappe.db.sql("""update `tabInquiry` set nominal_sales_invoice = %s where `name` = %s""", (total_so, doc.inquiry))
        total_so = frappe.db.sql("""select nominal_sales_order from `tabInquiry` where docstatus = '1' and `name` = %s""", doc.inquiry)[0][0]
        frappe.db.sql("""update `tabInquiry` set status = 'Submitted' where `name` = %s""", doc.inquiry)

def submit_purchase_order(doc, method):
    pass
#    items = frappe.db.sql("""select * from `tabPurchase Order Item` where parent = %s""", doc.name, as_dict=1)
#    for row in items:
#        if row.sales_order_item:
#            frappe.db.sql("""update `tabSales Order Item` set po_no = %s where `name` = %s""", (doc.name, row.sales_order_item))

def cancel_purchase_order(doc, method):
    pass
#    items = frappe.db.sql("""select * from `tabPurchase Order Item` where parent = %s""", doc.name, as_dict=1)
#    for row in items:
#        if row.sales_order_item:
#            frappe.db.sql("""update `tabSales Order Item` set po_no = null where `name` = %s""", row.sales_order_item)

def submit_purchase_receipt(doc, method):
    po = frappe.db.sql("""select purchase_order from `tabPurchase Receipt Item` where parent = %s and purchase_order is not null order by idx asc limit 1""", doc.name)[0][0]
    if po:
        frappe.db.sql("""update `tabPurchase Receipt` set purchase_order = %s where `name` = %s""", (po, doc.name))

def submit_purchase_invoice(doc, method):
    if doc.type_of_invoice == "Payment":
        pr = frappe.db.sql("""select purchase_receipt from `tabPurchase Invoice PR` where parent = %s""", doc.name, as_dict=1)
        for row in pr:
            frappe.db.sql("""update `tabPurchase Receipt` set invoice_payment = %s where `name` = %s""", (doc.name, row.purchase_receipt))

def cancel_purchase_invoice(doc, method):
    if doc.type_of_invoice == "Payment":
        pr = frappe.db.sql("""select purchase_receipt from `tabPurchase Invoice PR` where parent = %s""", doc.name, as_dict=1)
        for row in pr:
            frappe.db.sql("""update `tabPurchase Receipt` set invoice_payment = null where `name` = %s""", row.purchase_receipt)

def submit_journal_entry(doc, method):
    if doc.delivery_note:
        if doc.reversing_entry:
            frappe.db.sql("""update `tabDelivery Note` set reversing_entry = %s where `name` = %s""", (doc.name, doc.delivery_note))
        else:
            frappe.db.sql("""update `tabDelivery Note` set journal_entry = %s where `name` = %s""", (doc.name, doc.delivery_note))

def cancel_journal_entry(doc, method):
    if doc.delivery_note:
        if doc.reversing_entry:
            frappe.db.sql("""update `tabDelivery Note` set reversing_entry = null where `name` = %s""", doc.delivery_note)
        else:
            frappe.db.sql("""update `tabDelivery Note` set journal_entry = null where `name` = %s""", doc.delivery_note)

def update_product_bundle(doc, method):
    if doc.product_assembly:
        frappe.db.sql("""update `tabProduct Assembly` set product_bundle = %s, status = 'Completed' where `name` = %s""", (doc.name, doc.product_assembly))
        frappe.db.sql("""update `tabQuotation Assembly Item` set product_bundle = %s where docstatus != '2' and product_assembly = %s""", (doc.name, doc.product_assembly))
        for row in doc.items:
            if row.product_assembly_detail:
                frappe.db.sql("""update `tabProduct Assembly Item` set item_code = %s where `name` = %s""", (row.item_code, row.product_assembly_detail))
