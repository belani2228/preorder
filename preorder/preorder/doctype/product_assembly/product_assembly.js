// Copyright (c) 2017, ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Product Assembly', {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && frm.doc.status == "Submitted") {
			cur_frm.add_custom_button(__('Product Bundle'), cur_frm.cscript['Product Bundle'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	}
});
cur_frm.cscript['Product Bundle'] = function() {
	frappe.model.open_mapped_doc({
		method: "preorder.preorder.doctype.product_assembly.product_assembly.make_product_bundle",
		frm: cur_frm
	})
}
