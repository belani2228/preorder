
from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import msgprint, _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def get_items_selling_quotation(source_name, target_doc=None):
    if target_doc:
        if isinstance(target_doc, basestring):
            import json
            target_doc = frappe.get_doc(json.loads(target_doc))
        target_doc.set("items", [])

	query = frappe.db.sql_list("""select distinct(sq.`name`) from `tabSupplier Quotation` sq, `tabSupplier Quotation Item` sqi where sq.`name` = sqi.parent and sqi.inquiry = %s order by sq.`name` asc""", source_name)
    tampung = []
    for row in query:
#        tampung.append(row)
#    temp = ", ".join(tampung)
#    frappe.throw(temp)
    	doclist = get_mapped_doc("Supplier Quotation", row, {
    		"Supplier Quotation": {
    			"doctype": "Quotation",
    			"field_no_map":["customer", "posting_date", "due_date", "items"]
    		},
    		"Supplier Quotation Item": {
    			"doctype": "Quotation Item",
    			"field_map":{
    				"amount": "amount_siq"
    			}
    		},
    	}, target_doc)
    return doclist
