// Copyright (c) 2017, ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inquiry', {
	refresh: function(frm) {
		frm.set_df_property("inquiry_type", "read_only", frm.doc.__islocal ? 0 : 1);
		if(frm.doc.docstatus == 1) {
			cur_frm.add_custom_button(__('Request for Sales Quotation'), cur_frm.cscript['Request for Sales Quotation'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	}
});
cur_frm.cscript['Request for Sales Quotation'] = function() {
	frappe.model.open_mapped_doc({
		method: "preorder.preorder.doctype.inquiry.inquiry.make_rfsq",
		frm: cur_frm
	})
}
cur_frm.set_query("contact_person",  function (frm) {
		return {
        filters: [
            ['customer', '=', cur_frm.doc.customer]
        ]
		}
});
frappe.ui.form.on("Inquiry", "validate", function(frm) {
	if(cur_frm.doc.inquiry_type == 'Request'){
		cur_frm.doc.naming_series = 'R.YY.-.####'
	}else if (cur_frm.doc.inquiry_type == 'Request Project') {
		cur_frm.doc.naming_series = 'RP.YY.-.####'
	}else if (cur_frm.doc.inquiry_type == 'Request Service') {
		cur_frm.doc.naming_series = 'RS.YY.-.####'
	}else if (cur_frm.doc.inquiry_type == 'Request BST') {
		cur_frm.doc.naming_series = 'RBST.YY.-.####'
	}else {
		cur_frm.doc.naming_series = 'RPBST.YY.-.####'
	}
})
