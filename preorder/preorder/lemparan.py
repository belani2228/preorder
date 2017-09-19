from __future__ import unicode_literals
import frappe
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
            target.item_code = "Tampungan"
            target.item_name = "Tampungan"
            target.description = "Tampungan"

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
    	}, target_doc)
        return doc

@frappe.whitelist()
def get_items_from_sales_order(source_name, target_doc=None):
    if target_doc:
        if isinstance(target_doc, basestring):
            import json
            target_doc = frappe.get_doc(json.loads(target_doc))
        target_doc.set("items", [])

    komponen = frappe.db.sql_list("""select distinct(so.`name`) from `tabSales Order Item` soi inner join `tabSales Order` so on soi.parent = so.`name` where so.docstatus = '1' and soi.selected_supplier = %s""", source_name)
    if komponen:
        for d in komponen:
        	si = get_mapped_doc("Sales Order", d, {
        		"Sales Order": {
        			"doctype": "Purchase Order",
        			"validation": {
        				"docstatus": ["=", 1],
                    },
                    "field_no_map": [
                        "customer", "customer_name", "address_display", "shipping_address", "total", "grand_total"
                    ],
        		},
        		"Sales Order Item": {
        			"doctype": "Purchase Order Item",
                    "field_map": {
                        "item_description": "description",
                        "parent": "sales_order",
                        "name": "sales_order_item",
                        "approved_price": "rate"
                    },
                    "condition":lambda doc: doc.po_no is None and doc.selected_supplier == source_name
        		},
        	}, target_doc)
        return si
    else:
        msgprint(_("No Inquiry found for this supplier"))

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
