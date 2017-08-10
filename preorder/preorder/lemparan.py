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

	query = frappe.db.sql_list("""select distinct(sq.`name`) from `tabSupplier Quotation` sq, `tabSupplier Quotation Item` sqi
    where sq.`name` = sqi.parent and sq.docstatus = '1' and sqi.inquiry = %s and sqi.quotation_detail is null order by sq.`name` asc""", source_name)
    if query:
        for row in query:
        	doclist = get_mapped_doc("Supplier Quotation", row, {
        		"Supplier Quotation": {
        			"doctype": "Quotation",
        			"field_no_map":["customer", "posting_date", "due_date", "items"]
        		},
        		"Supplier Quotation Item": {
        			"doctype": "Quotation Item",
        			"field_map":{
        				"name": "supplier_quotation_item"
        			},
                    "condition":lambda doc: doc.quotation_detail is None
        		},
        	}, target_doc)
        return doclist
    else:
        frappe.throw(_("No Items Found"))
