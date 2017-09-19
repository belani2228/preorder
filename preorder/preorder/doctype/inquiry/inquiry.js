// Copyright (c) 2017, ridhosribumi and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inquiry', {
	refresh: function(frm) {
		frm.set_df_property("inquiry_type", "read_only", frm.doc.__islocal ? 0 : 1);
		if(frm.doc.docstatus == 1 && frm.doc.status == "Submitted") {
			cur_frm.add_custom_button(__('Request for Supplier Quotation'), cur_frm.cscript['Request for Supplier Quotation'], __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
		if(frm.doc.status == "Submitted") {
			cur_frm.add_custom_button(__('Set as Lost'), cur_frm.cscript['Declare Order Lost']);
		}
	}
});
cur_frm.cscript['Request for Supplier Quotation'] = function() {
	frappe.model.open_mapped_doc({
		method: "preorder.preorder.doctype.inquiry.inquiry.make_rfsq",
		frm: cur_frm
	})
}
cur_frm.cscript['Declare Order Lost'] = function(){
	var dialog = new frappe.ui.Dialog({
		title: "Set as Lost",
		fields: [
			{"fieldtype": "Text", "label": __("Reason for losing"), "fieldname": "reason",
				"reqd": 1 },
			{"fieldtype": "Button", "label": __("Update"), "fieldname": "update"},
		]
	});

	dialog.fields_dict.update.$input.click(function() {
		var args = dialog.get_values();
		if(!args) return;
		return cur_frm.call({
			method: "declare_order_lost",
			doc: cur_frm.doc,
			args: args.reason,
			callback: function(r) {
				if(r.exc) {
					frappe.msgprint(__("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
}

cur_frm.set_query("contact_person",  function (frm) {
		return {
        filters: [
            ['customer', '=', cur_frm.doc.customer]
        ],
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
