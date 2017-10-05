from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def get_po_items(source_name, target_doc=None):
    invoice_type,related_doc,percent = source_name.split("|")
    if target_doc:
        if isinstance(target_doc, basestring):
            import json
            target_doc = frappe.get_doc(json.loads(target_doc))
        target_doc.set("items", [])

    def update_item(source, target, source_parent):
        item_dp = frappe.db.sql("""select `value` from `tabSingles` where doctype = 'Item Settings' and field = 'default_item_for_dp'""")[0][0]
        target.item_code = item_dp
        item = frappe.db.get_value("Item", item_dp, ["item_name", "description", "stock_uom", "income_account", expense_account"], as_dict=1)
        target.item_name = item.item_name
        target.description = item.description
        target.uom = item.stock_uom
        target.income_account = item.income_account
        target.expense_account = item.expense_account
        target.qty = "1"
        if invoice_type == "PO":
            po = frappe.db.get_value("Purchase Order", related_doc, ["net_total"], as_dict=1)
        elif invoice_type == "PR":
            po = frappe.db.get_value("Purchase Receipt", related_doc, ["net_total"], as_dict=1)
        rate = (flt(percent)/100) * flt(po.net_total)
        target.rate = rate
        target.amount = rate
        target.net_rate = rate
        target.net_amount = rate

    if invoice_type == "PO":
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
