from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")
		target.run_method("get_schedule_dates")
		target.run_method("calculate_taxes_and_totals")

	def update_item(source, target, source_parent):
		target.stock_qty = flt(source.qty) * flt(source.conversion_factor)
		target.price_list_rate = 0
		target.rate = 0

	def update_item_assembly(source, target, source_parent):
		target.item_code = frappe.db.sql("""select item_code from `tabProduct Bundle Item` where product_assembly_detail = %s""", source.product_assembly_item)[0][0]

	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Sales Order Item": {
			"doctype": "Purchase Order Item",
			"field_map": [
				["name", "sales_order_item"],
				["parent", "sales_order"],
			],
			"field_no_map":["price_list_rate", "rate", "amount", "net_rate", "net_amount"],
			"condition":lambda doc: doc.is_product_assembly == 0,
			"postprocess": update_item
		},
		"Quotation Assembly Item": {
			"doctype": "Purchase Order Item",
			"postprocess": update_item_assembly
		},
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def get_po_items(source_name, target_doc=None):
    invoice_type,related_doc,percent = source_name.split("|")
    if target_doc:
        if isinstance(target_doc, basestring):
            import json
            target_doc = frappe.get_doc(json.loads(target_doc))
        target_doc.set("items", [])
        target_doc.set("taxes", [])

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
        if invoice_type == "Down Payment":
            po = frappe.db.get_value("Purchase Order", related_doc, ["net_total"], as_dict=1)
        elif invoice_type == "Progress Payment":
            po = frappe.db.get_value("Purchase Receipt", related_doc, ["net_total"], as_dict=1)
        rate = (flt(percent)/100) * flt(po.net_total)
        target.rate = rate
        target.amount = rate
        target.net_rate = rate
        target.net_amount = rate

    if invoice_type == "Down Payment":
        doc = get_mapped_doc("Purchase Order", related_doc, {
        	"Purchase Order": {
        		"doctype": "Purchase Invoice",
        		"validation": {
        			"docstatus": ["=", 1],
        		},
        	},
        	"Purchase Order Item": {
        		"doctype": "Purchase Invoice Item",
        		"field_map":{
        			"parent": "purchase_order",
        			"name": "puerchase_order_item",
        		},
                "condition":lambda doc: doc.idx == 1,
                "postprocess": update_item
        	},
        }, target_doc)
        return doc
    elif invoice_type == "Progress Payment":
        doc = get_mapped_doc("Purchase Receipt", related_doc, {
        	"Purchase Receipt": {
        		"doctype": "Purchase Invoice",
        		"validation": {
        			"docstatus": ["=", 1],
        		},
        	},
        	"Purchase Receipt Item": {
        		"doctype": "Purchase Invoice Item",
        		"field_map":{
        			"parent": "purchase_receipt",
        			"name": "puerchase_receipt_item",
        		},
                "condition":lambda doc: doc.idx == 1,
                "postprocess": update_item
        	},
        }, target_doc)
        return doc

@frappe.whitelist()
def get_purchase_receipt(supplier, po):
    if supplier and po:
        pr_list = []
        invoice_list = frappe.db.sql("""select `name`, posting_date, net_total from `tabPurchase Receipt` where docstatus = '1' and status = 'To Bill' and supplier = %s and invoice_payment is null and purchase_order = %s""", (supplier, po), as_dict=True)
        for d in invoice_list:
            pr_list.append(frappe._dict({
                'purchase_receipt': d.name,
                'posting_date': d.posting_date,
                'net_total': d.net_total
            }))

        return pr_list

@frappe.whitelist()
def get_items_payment(supplier):
    if supplier:
        pr_list = []
        item = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'default_item_for_dp'""")[0][0]
        item_detail = frappe.db.get_value("Item", item, ["item_name", "description", "stock_uom", "income_account", "expense_account"], as_dict=1)
        pr_list.append(frappe._dict({
            'item_code': item,
            'item_name': item_detail.item_name,
            'description': item_detail.item_description,
            'uom': item_detail.stock_uom,
            'stock_uom': item_detail.stock_uom,
            'qty': '1',
            'expense_account': item_detail.expense_account
        }))

        return pr_list

@frappe.whitelist()
def get_purchase_invoice(supplier, po, invoice_type, net_total):
    pi_list = []
    if invoice_type == 'Non Project Payment':
        invoice_list = frappe.db.sql("""select `name`, posting_date, net_total from `tabPurchase Invoice` where docstatus = '1' and type_of_invoice = 'Down Payment' and purchase_order = %s""", po, as_dict=True)
    else:
        invoice_list = frappe.db.sql("""select `name`, posting_date, net_total from `tabPurchase Invoice` where docstatus = '1' and purchase_order = %s""", po, as_dict=True)
    for d in invoice_list:
        total_po = frappe.db.sql("""select net_total from `tabPurchase Order` where docstatus = '1' and `name` = %s""", po)[0][0]
        alokasi = (flt(net_total) / flt(total_po)) * flt(d.net_total)
        if alokasi >= 1:
            pi_list.append(frappe._dict({
                'purchase_invoice': d.name,
                'posting_date': d.posting_date,
                'net_total': alokasi
            }))
    return pi_list
