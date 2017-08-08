// Copyright (c) 2017, ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request for Supplier Quotation', {
	refresh: function(frm) {
	},
	get_items: function(frm) {
		return frappe.call({
			method: "get_items",
			doc: frm.doc,
			callback: function(r, rt) {
				frm.refresh()
			}
		});
	},
});
frappe.ui.form.on("Request for Supplier Quotation", "onload", function(frm) {
   frm.refresh();
});
frappe.ui.form.on("Request for Supplier Quotation", {
	refresh: function() {
		cur_frm.add_custom_button(__("Inquiry"), function() {
			erpnext.utils.map_current_doc({
				method: "preorder.preorder.doctype.inquiry.inquiry.make_rfsq",
				source_doctype: "Inquiry",
				target: cur_frm,
				setters:  {
					company: cur_frm.doc.company || undefined,
				},
				get_query_filters: {
					docstatus: 1,
				}
			})
		}, __("Get items from"));
	},
});
cur_frm.set_query("inquiry", "inquiry",  function (doc, cdt, cdn) {
	var c_doc= locals[cdt][cdn];
    return {
        filters: {
            'docstatus': 1
        }
    }
});
frappe.ui.form.on("Request for Supplier Quotation Inquiry", "inquiry", function(frm, cdt, cdn) {
    row = locals[cdt][cdn];
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Inquiry",
						name: row.inquiry
        },
        callback: function (data) {
            frappe.model.set_value(cdt, cdn, "transaction_date", data.message.transaction_date);
						frappe.model.set_value(cdt, cdn, "customer", data.message.customer);
						frappe.model.set_value(cdt, cdn, "customer_name", data.message.customer_name);
				}
    })
});
