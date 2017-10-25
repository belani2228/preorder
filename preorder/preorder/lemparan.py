from __future__ import unicode_literals
import frappe, json
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def reset_rate(doc):
    #msgprint(_(doc{"customer"}))
    pass

@frappe.whitelist()
def get_items_selling_quotation(source_name, target_doc=None):
    cek = frappe.db.get_value("Inquiry", source_name, "status")
    if cek != "Lost":
        if target_doc:
            if isinstance(target_doc, basestring):
                import json
                target_doc = frappe.get_doc(json.loads(target_doc))
            target_doc.set("items", [])

        def update_item(source, target, source_parent):
            target.item_code = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'default_item_for_inquiry'""")[0][0]
            target.item_name = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'inquiry_item_name'""")[0][0]
            target.description = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'inquiry_item_descrition'""")[0][0]

        def update_assembly_item(source, target, source_parent):
            pa = frappe.db.get_value("Product Assembly", source.product_assembly, ["parent_item", "product_bundle"], as_dict=1)
#            pa = frappe.db.sql("""select parent_item, product_bundle from `tabProduct Assembly` where `name` = %s""", source.product_assembly, as_dict=1)
            target.parent_item = pa.parent_item
            target.product_bundle = pa.product_bundle

        doc = get_mapped_doc("Inquiry", source_name, {
    		"Inquiry": {
    			"doctype": "Quotation",
    			"validation": {
    				"docstatus": ["=", 1],
    			},
    		},
    		"Inquiry Item": {
    			"doctype": "Quotation Item",
    			"field_map":{
    				"parent": "inquiry",
    				"name": "inquiry_item",
    			},
                "postprocess": update_item
    		},
    		"Inquiry All Item": {
    			"doctype": "Quotation Assembly Item",
                "condition":lambda doc: doc.is_product_assembly == 1,
                "postprocess": update_assembly_item
    		},
    	}, target_doc)
        return doc

@frappe.whitelist()
def get_items_from_sales_order(source_name, target_doc=None):
    doc = get_mapped_doc("Sales Order", source_name, {
    	"Sales Order": {
    		"doctype": "Purchase Order",
    		"validation": {
    			"docstatus": ["=", 1],
    		},
            "field_no_map": [
                "contact_person", "contact_display"
            ],
    	},
    	"Sales Order Item": {
    		"doctype": "Purchase Order Item",
    		"field_map":{
    			"name": "sales_order_item"
    		},
            "field_no_map": [
                "price_list_rate", "rate", "amount"
            ],
			"add_if_empty": True
    	},
    }, target_doc)

    return doc

@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
	pi = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Sales Order Item": {
			"doctype": "Purchase Order Item",
			"field_map": {
				"parent": "sales_order"
			},
            "field_no_map": [
                "price_list_rate", "rate"
            ],
			"add_if_empty": True
		}
	}, target_doc)

	return pi

@frappe.whitelist()
def get_items_tampungan(source_name, target_doc=None):
    tipe,related_doc,persen,inquiry_id = source_name.split("|")
    if target_doc:
        if isinstance(target_doc, basestring):
            import json
            target_doc = frappe.get_doc(json.loads(target_doc))
        target_doc.set("items", [])

    def update_item(source, target, source_parent):
        item_dp = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'default_item_for_dp'""")[0][0]
        target.item_code = item_dp
        item = frappe.db.get_value("Item", item_dp, ["item_name", "description", "stock_uom", "income_account", "expense_account"], as_dict=1)
        target.item_name = item.item_name
        target.description = item.description
        target.uom = item.stock_uom
        target.income_account = item.income_account
        target.expense_account = item.expense_account
        target.qty = "1"
        if tipe == "SO":
            so = frappe.db.get_value("Sales Order", related_doc, ["net_total"], as_dict=1)
        elif tipe == "DN":
            so = frappe.db.get_value("Delivery Note", related_doc, ["net_total"], as_dict=1)
        rate = (flt(persen)/100) * flt(so.net_total)
        target.rate = rate
        target.amount = rate
        target.net_rate = rate
        target.net_amount = rate

    doc = get_mapped_doc("Inquiry", inquiry_id, {
    	"Inquiry": {
    		"doctype": "Sales Invoice",
    		"validation": {
    			"docstatus": ["=", 1],
    		},
    	},
    	"Inquiry Item": {
    		"doctype": "Sales Invoice Item",
    		"field_map":{
    			"parent": "inquiry",
    			"name": "inquiry_item",
    		},
            "condition":lambda doc: doc.idx == 1,
            "postprocess": update_item
    	},
    }, target_doc)
    return doc

@frappe.whitelist()
def get_delivery_note(inquiry):
    if inquiry:
        dn_list = []
        invoice_list = frappe.db.sql("""select `name`, posting_date, net_total from `tabDelivery Note` where docstatus = '1' and inquiry = %s and sales_invoice is null""", inquiry, as_dict=True)
        for d in invoice_list:
            dn_list.append(frappe._dict({
                'delivery_note': d.name,
                'posting_date': d.posting_date,
                'net_total': d.net_total
            }))

        return dn_list

@frappe.whitelist()
def get_items_from_pelunasan(source_name, target_doc=None):
    nominal,persen,inquiry_id = source_name.split("|")
    if target_doc:
        if isinstance(target_doc, basestring):
            import json
            target_doc = frappe.get_doc(json.loads(target_doc))
        target_doc.set("items", [])

    def update_item(source, target, source_parent):
        item_dp = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'default_item_for_dp'""")[0][0]
        target.item_code = item_dp
        item = frappe.db.get_value("Item", item_dp, ["item_name", "description", "stock_uom", "income_account", "expense_account"], as_dict=1)
        target.item_name = item.item_name
        target.description = item.description
        target.uom = item.stock_uom
        target.income_account = item.income_account
        target.expense_account = item.expense_account
        target.qty = "1"
        rate = (flt(persen)/100) * flt(nominal)
        target.rate = rate
        target.amount = rate
        target.net_rate = rate
        target.net_amount = rate

    doc = get_mapped_doc("Inquiry", inquiry_id, {
    	"Inquiry": {
    		"doctype": "Sales Invoice",
    		"validation": {
    			"docstatus": ["=", 1],
    		},
    	},
    	"Inquiry Item": {
    		"doctype": "Sales Invoice Item",
    		"field_map":{
    			"parent": "inquiry",
    			"name": "inquiry_item",
    		},
            "condition":lambda doc: doc.idx == 1,
            "postprocess": update_item
    	},
    }, target_doc)
    return doc

@frappe.whitelist()
def get_sales_invoice(inquiry, tipe, net_total):
    si_list = []
    if tipe == 'Non Project Payment':
        invoice_list = frappe.db.sql("""select `name`, posting_date, net_total from `tabSales Invoice` where docstatus = '1' and type_of_invoice = 'Down Payment' and inquiry = %s""", inquiry, as_dict=True)
    else:
        invoice_list = frappe.db.sql("""select `name`, posting_date, net_total from `tabSales Invoice` where docstatus = '1' and inquiry = %s""", inquiry, as_dict=True)
    for d in invoice_list:
        total_so = frappe.db.sql("""select net_total from `tabSales Order` where docstatus = '1' and inquiry = %s""", inquiry)[0][0]
        alokasi = (flt(net_total) / flt(total_so)) * flt(d.net_total)
        if alokasi >= 1:
            si_list.append(frappe._dict({
                'sales_invoice': d.name,
                'posting_date': d.posting_date,
                'net_total': alokasi
            }))

    return si_list

@frappe.whitelist()
def make_journal_entry(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.run_method("set_missing_values")

	jv = get_mapped_doc("Delivery Note", source_name, {
		"Delivery Note": {
			"doctype": "Journal Entry",
    		"field_map":{
    			"posting_date": "posting_date"
    		},
		},
	}, target_doc, set_missing_values)
	return jv

@frappe.whitelist()
def make_reverse_journal(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.reversing_entry = 1
		target.run_method("set_missing_values")

	jv = get_mapped_doc("Journal Entry", source_name, {
		"Journal Entry": {
			"doctype": "Journal Entry",
    		"field_map":{
    			"posting_date": "posting_date"
    		},
		},
		"Journal Entry Account": {
			"doctype": "Journal Entry Account",
    		"field_map":{
				"credit_in_account_currency": "debit_in_account_currency",
                "debit_in_account_currency": "credit_in_account_currency",
    		},
		},
	}, target_doc, set_missing_values)
	return jv

@frappe.whitelist()
def get_amount(dn):
    dn_list = []
    list1 = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) as debit from `tabStock Ledger Entry` where voucher_no = %s""", dn, as_dict=True)
    for d in list1:
        dn_list.append(frappe._dict({
            'party_type': 'Customer',
            'debit': d.debit,
            'credit': ''
        }))
    list2 = frappe.db.sql("""select sum((actual_qty * -1) * valuation_rate) as credit from `tabStock Ledger Entry` where voucher_no = %s""", dn, as_dict=True)
    for d in list2:
        dn_list.append(frappe._dict({
            'party_type': 'Customer',
            'debit': '',
            'credit': d.credit
        }))
    return dn_list
