// Copyright (c) 2017, ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request for Supplier Quotation', {
	refresh: function(frm) {
		if(cur_frm.doc.docstatus == 1) {
			cur_frm.add_custom_button(__('Supplier Quotation'), cur_frm.cscript['Supplier Quotation'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
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
frappe.ui.form.on("Request for Supplier Quotation Inquiry", "onload", function(frm) {
   frm.refresh();
});
frappe.ui.form.on("Request for Supplier Quotation", {
	refresh: function() {
		if(cur_frm.doc.docstatus == 0 || cur_frm.doc.__islocal){
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
		}
	},
});
cur_frm.cscript['Supplier Quotation'] = function() {
	frappe.model.open_mapped_doc({
		method: "preorder.preorder.doctype.request_for_supplier_quotation.request_for_supplier_quotation.make_supplier_quotation",
		frm: cur_frm
	})
}
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
